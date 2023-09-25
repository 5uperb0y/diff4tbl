import pandas as pd
import numpy as np
class Proc():
	def __init__(self, df1, df2, params):
		self.df1 = df1
		self.df2 = df2
		self.common_fields = params.get("common_fields", False)
		self.common_index = params.get("common_index", False)
		self.index = params.get("index", None)
		self.fields = params.get("fields", None)
		self.exclude_fields = params.get("exclude_fields", [])
	def _select_by_fields(self, df):
		if self.fields:
			df.columns = df.columns.astype(str)
			return df[self.fields]
		else:
			return df
	def _exclude_by_fields(self, df):
		df.columns = df.columns.astype(str)
		return df.drop(self.exclude_fields, axis = 1)
	def _intersect_by_fields(self, df1, df2):
		common_fields = df1.columns.intersection(df2.columns)
		return df1[common_fields], df2[common_fields]
	def _intersect_by_index(self, df1, df2):
		if self.index:
			df1_indices = df1[self.index]
			df2_indices = df2[self.index]
			common_positions = df1_indices[df1_indices.isin(df2_indices)].index.to_list()
		else:
			df1_indices = df1.index
			df2_indices = df2.index
			common_positions = df1_indices[df1_indices.isin(df2_indices)].to_list()
		return df1.iloc[common_positions], df2.iloc[common_positions]
	def _get_all_indexes(self, df1, df2, index = None):
		if not index:
			return sorted(set(df1.index) | set(df2.index))
		return sorted(set(df1[index]) | set(df2[index]))
	def _union_columns(self, df1, df2, index = None):
		df2_extra_cols = [col for col in df2.columns if col not in df1.columns and col != index]
		return list(df1.columns) + df2_extra_cols
	def _get_aligned_data(self, df, all_indexes, all_columns, index):
		df_aligned = pd.DataFrame(columns = all_columns, index = all_indexes).fillna("")
		if index:
			df.set_index(index, inplace = True, drop = False)
		for col in all_columns:
			if col in df.columns:
				df_aligned[col].update(df[col])
		return df_aligned
	def _align_dataframes(self, df1, df2, index = None):
		all_indexes = self._get_all_indexes(df1, df2, index)
		all_columns = self._union_columns(df1, df2, index)
		df1_aligned = self._get_aligned_data(df1, all_indexes, all_columns, index)
		df2_aligned = self._get_aligned_data(df2, all_indexes, all_columns, index)
		return df1_aligned, df2_aligned
	def process(self):
		df1, df2 = self.df1.copy(), self.df2.copy() 		
		df1, df2 = self._select_by_fields(df1), self._select_by_fields(df2)
		df1, df2 = self._exclude_by_fields(df1), self._exclude_by_fields(df2)
		if self.common_fields:
			df1, df2 = self._intersect_by_fields(df1, df2)
		if self.common_index:
			df1, df2 = self._intersect_by_index(df1, df2)
		return self._align_dataframes(df1, df2, self.index)