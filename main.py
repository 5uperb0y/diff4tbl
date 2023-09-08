import argparse
import pandas as pd
def load_data(f_path, index = None, column = None):
	df = pd.read_csv(f_path, sep = "\t", keep_default_na = False, dtype = str)
	if index:
		df = df.set_index(index, drop = False)
	return df
def select_columns(df, columns_str, index=None):
    selected_columns = columns_str.split(",") if columns_str else df.columns.tolist()
    if index and index not in selected_columns:
        selected_columns.insert(0, index)  # Ensure index is always in the selected columns
    return df[selected_columns]
def select_columns(df, column, index = None):
	kept_columns = column.split(",")
	if index and index not in kept_columns:
		kept_columns.insert(0, index)
	return df[kept_columns]
def row_to_header(df, row_index: int = 0):
	new_header = df.iloc[row_index]
	df = df.drop(df.index[row_index])
	df.columns = new_header
	return df
def header_to_row(df):
	return pd.concat([df.columns.to_frame().T, df]).reset_index(drop = True)
def compare_df(df1, df2):
	return df1.combine(df2, compare_series)
def compare_series(s1, s2):
	return s1.combine(s2, combine_cells)
def combine_cells(c1, c2):
	c1 = "" if pd.isna(c1) else str(c1)
	c2 = "" if pd.isna(c2) else str(c2)
	if c1 == c2:
		return c1
	else:
		return c1 + "{" + c2 + "}"
class DiffMode():
	def compare(self, df1, df2):
		pass
class DefaultMode(DiffMode):
	def compare(self, df1, df2):
		df1 = header_to_row(df1)
		df2 = header_to_row(df2)
		return compare_df(df1, df2)
class IndexMode(DiffMode):
	def compare(self, df1, df2):
		shared_ids = df1.index.intersection(df2.index)
		common_df1 = header_to_row(df1.loc[shared_ids].sort_index())
		common_df2 = header_to_row(df2.loc[shared_ids].sort_index())
		return compare_df(common_df1, common_df2)
def parse_arguments():
	parser = argparse.ArgumentParser(description = "A table comparison tool, inspired by GNU diff.")
	parser.add_argument("file1", type = str, help = "Path to the first file to compare.")
	parser.add_argument("file2", type = str, help = "Path to the second file to compare.")
	parser.add_argument("-i", "--index", type = str, help = "Name of index column, focusing comparison based on shared indices")
	parser.add_argument("-c", "--column", type = str, help = "Only compare the specified columns across the two tables. If not provided, all columns will be compared.")
	return parser.parse_args()
def main():
	args = parse_arguments()
	df1 = load_data(args.file1, args.index, args.column)
	df2 = load_data(args.file2, args.index, args.column)
	if args.column:
		df1 = select_columns(df1, args.column, args.index)
		df2 = select_columns(df2, args.column, args.index)
	if args.index:
		mode = IndexMode()
	else:
		mode = DefaultMode()
	diff_df = mode.compare(df1, df2)
	print(diff_df.to_csv(sep = "\t", index = None, header = None))
main()