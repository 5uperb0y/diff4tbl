import argparse
import pandas as pd
# ARGUMENT PARSING
def parse_arguments():
	parser = argparse.ArgumentParser(description = "A table comparison tool, inspired by GNU diff.")
	parser.add_argument("file1", type = str, help = "Path to the first file to compare.")
	parser.add_argument("file2", type = str, help = "Path to the second file to compare.")
	parser.add_argument("-i", "--index", type = str, help = "Name of index column, focusing comparison based on shared indices")
	parser.add_argument("-c", "--column", type = str, help = "Only compare the specified columns across the two tables. If not provided, all columns will be compared.")
	parser.add_argument("-C", "--common-columns", action = "store_true", help = "Only compare columns that exist in both tables.")
	parser.add_argument("-U", "--show-unique", action = "store_true", help = "Show unique rows or columns between two tables.")
	parser.add_argument("-y", "--side-by-side", action = "store_true", help = "Display cell differences in a side-by-side tabular format.")
	parser.add_argument("-S", "--suppress-common", action = "store_true", help = "Only show differences, suppress common lines.")
	return parser.parse_args()
# DATA LOADING
def detect_separator(f_path):
	with open(f_path, "r") as file:
		content = file.read(1024)
	if "\t" in content:
		return "\t"
	elif "," in content:
		return ","
	elif "\s" in content:
		return "\s"
	else:
		raise ValueError("Could not determine the separator!")
def load_data(f_path, index = None, column = None):
	df = pd.read_csv(f_path, sep = detect_separator(f_path), keep_default_na = False, dtype = str)
	if index:
		df = df.set_index(index, drop = False)
	if column:
		df = select_columns(df, index, column)
	return df
def select_columns(df, index = None, column = None):
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
	df = pd.concat([df.columns.to_frame().T, df]).reset_index(drop = True)
	df.columns = range(df.shape[1])
	return df
def grep_df(df, pattern, skip = None):
	skip = skip or []
	return df[df.index.isin(skip) | df.apply(lambda x: x.astype(str).str.contains(pattern)).any(axis = 1)]
# PREPROCESSING
def dehead(df1, df2):
	df1 = header_to_row(df1)
	df2 = header_to_row(df2)
	return df1, df2
def intersect_by_ids(df1, df2):
	shared_ids = df1.index.intersection(df2.index)
	df1 = df1.loc[shared_ids].sort_index()
	df2 = df2.loc[shared_ids].sort_index()
	return df1, df2
def intersect_by_columns(df1, df2):
	common_columns = df1.columns.intersection(df2.columns)
	df1 = df1[common_columns]
	df2 = df2[common_columns]
	return df1, df2
def show_unique_rows(df1, df2):
	df1_only = df1.index.difference(df2.index)
	df2_only = df2.index.difference(df1.index)
	print("Row comparison:")
	for id in df1_only:
		print("- " + str(id))
	for id in df2_only:
		print("+ " + str(id))
def show_unique_columns(df1, df2):
	df1_only = df1.columns.difference(df2.columns)
	df2_only = df2.columns.difference(df1.columns)
	print("Column comparison:")
	for name in df1_only:
		print("- " + name)
	for name in df2_only:
		print("+ " + name)
def diff_type(str1, str2):
	if str1 == str2:
		return ""
	elif pd.isna(str1) or str1 == "":
		return "<"
	elif pd.isna(str2) or str2 == "":
		return ">"
	else:
		return "|"
# COMPARING
def compare_side_by_side(df1, df2):
	if not df1.index.name:
		df1["index"] = df1.index
		df2["index"] = df2.index
	index = df1.index.name or "index"
	df1 = pd.melt(df1, id_vars = [index])
	df2 = pd.melt(df2, id_vars = [index])
	merged = df1.merge(df2, on = [index, "variable"], how = "outer")
	def diff_type_for_row(row):
		return diff_type(row["value_x"], row["value_y"])
	merged["Comparison"] = merged.apply(diff_type_for_row, axis = 1)
	return merged[[index, "variable", "value_x", "Comparison", "value_y"]]
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
def main():
	args = parse_arguments()
	df1 = load_data(args.file1, args.index, args.column)
	df2 = load_data(args.file2, args.index, args.column)
	if args.show_unique:
		show_unique_columns(df1, df2)
		show_unique_rows(df1, df2)
		return
	if args.common_columns:
		df1, df2 = intersect_by_columns(df1, df2)
	if args.index:
		df1, df2 = intersect_by_ids(df1, df2)
	if args.side_by_side:
		diff_df = compare_side_by_side(df1, df2)
		if args.suppress_common:
			diff_df = diff_df[diff_df["Comparison"] != ""]
		print(diff_df.to_csv(sep = "\t", index = None, header = None))
		return
	df1, df2 = dehead(df1, df2)
	diff_df = compare_df(df1, df2)
	if args.suppress_common:
		diff_df = grep_df(diff_df, "{", skip = [0])
	print(diff_df.to_csv(sep = "\t", index = None, header = False))
main()