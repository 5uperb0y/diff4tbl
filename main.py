import argparse
import pandas as pd
def combine_cells(c1, c2):
	c1 = "" if pd.isna(c1) else str(c1)
	c2 = "" if pd.isna(c2) else str(c2)
	if c1 == c2:
		return c1
	else:
		return c1 + "{" + c2 + "}"
def read_table_as_str(f_path):
	return pd.read_csv(f_path, sep = "\t", keep_default_na = False, dtype = str, header = None)
def compare_series(s1, s2):
	return s1.combine(s2, combine_cells)
def compare_df(df1, df2):
	return df1.combine(df2, compare_series)
def parse_arguments():
    parser = argparse.ArgumentParser(description="A table comparison tool, inspired by GNU diff.")
    parser.add_argument("file1", type = str, help="Path to the first file to compare.")
    parser.add_argument("file2", type = str, help="Path to the second file to compare.")
    return parser.parse_args()
def main():
	args = parse_arguments()
	df1 = read_table_as_str(args.file1)
	df2 = read_table_as_str(args.file2)
	diff_df = compare_df(df1, df2)
	print(diff_df.to_csv(sep="\t", index = False, header = False))
main()