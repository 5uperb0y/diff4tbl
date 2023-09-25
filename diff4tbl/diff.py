import pandas as pd
import numpy as np
import sys
from abc import ABC, abstractmethod
class Layout(ABC):
	def __init__(self, df1, df2, params):
		self.df1 = df1
		self.df2 = df2
		self.suppress_method = params.get("suppress")
		self.suppress_methods = {
			"suppress_commons": lambda: self._suppress_commons(),
			"suppress_common_lines": lambda: self._suppress_common_lines(),
			"suppress_common_fields": lambda: self._suppress_common_fields(),
			"no_suppress": lambda: None
		}
		self.separator = params.get("separator", "\t")
		self.style = params.get("style", "bracket")
		self.highlight_styles = {
			"bracket": lambda x, y: f"{x}{{{y}}}",
			"arrow": lambda x, y: f"{x}->{y}",
			"color": lambda x, y: self._colored_text(x, ["229", "192", "123"]) + self._colored_text(y, ["97", "175", "239"]),
		}
	@abstractmethod
	def suppress(self):
		pass
	@abstractmethod
	def compare(self):
		pass
	@abstractmethod
	def parse(self):
		pass
	@abstractmethod
	def show(self, result):
		pass
	def _suppress_commons(self):
		self._suppress_common_lines()	
		self._suppress_common_fields()
	def _suppress_common_lines(self):
		mask = (self.df1 == self.df2).all(axis = 1)
		self.df1, self.df2 = self.df1.loc[~mask], self.df2[~mask]
	def _suppress_common_fields(self):
		mask = (self.df1 == self.df2).all(axis = 0)
		self.df1, self.df2 = self.df1.loc[:, ~mask], self.df2.loc[:, ~mask]
	def _highlight_difference(self, style, str1, str2):
		return self.highlight_styles[style](str1, str2)
	def _colored_text(self, str, rgb):
		return f"\033[38;2;{';'.join(rgb)}m{str}\033[0m"
	def _compare_cell(self, df1, df2):
		return pd.DataFrame(
			{
				col: [
					c1 if c1 == c2 else self._highlight_difference(self.style, str(c1), str(c2))
					for c1, c2 in zip(df1[col], df2[col])
				]
				for col in df1.columns
			}
		)
class Context(Layout):
	def suppress(self):
		self.suppress_methods[self.suppress_method]()
	def compare(self):
		return self._compare_cell(self.df1, self.df2)
	def parse(self):
		self.suppress()
		result = self.compare().to_csv(sep = self.separator, index = False, header = True)
		return result
	def show(self):
		sys.stdout.write(self.parse())
class Normal(Layout):
	def suppress(self):
		self.suppress_methods[self.suppress_method]()
	def compare(self):
		comparison = np.where(self.df1 == self.df2, "",
						np.where(self.df1 == "", ">",
							np.where(self.df2 == "", "<", "|")))
		return pd.DataFrame(
			[
				{
					"row": row_name,
					"column": col_name,
					"value_df1": self.df1.loc[row_name, col_name],
					"comparison": comparison[row_idx, col_idx],
					"value_df2": self.df2.loc[row_name, col_name]
				}
				for row_idx, row_name in enumerate(self.df1.index)
				for col_idx, col_name in enumerate(self.df1.columns)
			]
		)
	def parse(self):
		self.suppress()
		result = self.compare()
		if self.suppress_method == "suppress_commons":
			result = result[result["comparison"] != ""]
		result = result.to_csv(sep = self.separator, index = False, header = None)
		return result
	def show(self):
		sys.stdout.write(self.parse())
class Lines(Layout):
	def suppress(self):
		self.suppress_methods[self.suppress_method]()
	def compare(self):
		common_mask = (self.df1 == self.df2).all(axis = 1)
		addition_mask = self.df1.eq("").all(axis = 1)
		deletion_mask = self.df2.eq("").all(axis = 1)
		change_mask = ~(common_mask | addition_mask | deletion_mask)
		comparison = {
			"common": self.df1[common_mask],
			"addition": self.df2[addition_mask],
			"deletion": self.df1[deletion_mask],
			"change": self._compare_cell(self.df1[change_mask], self.df2[change_mask])
		}
		return comparison
	def parse(self):
		self.suppress()
		result = {}
		for key, df in self.compare().items():
			if not df.empty:
				result[key] = df.to_csv(sep = self.separator, index = False, header = None)
		return result
	def show(self):
		for key, value in self.parse().items():
			print(key)
			sys.stdout.write(value)
class Diff():
	def __init__(self, df1, df2, params = {}):
		self.layouts = {
			"context": Context(df1, df2, params),
			"normal": Normal(df1, df2, params),
			"lines": Lines(df1, df2, params)
		}
		self.layout = self.layouts[params.get("layout", "normal")]
	def show(self):
		self.layout.show()