# diff4tbl: Table Comparison Tool

`diff4tbl` is a table comparison tool inspired by the iconic GNU diff, developing with python and Pandas module.
## Features

- Performs cell-by-cell comparison.
- Automatically detects CSV, TSV, and space-separated table formats.
- Displays unique rows or columns between two tables.
- Supports comparison of only the common columns between two tables.
- Offers a side-by-side comparison mode for intuitive difference visualizationi.
- Summarize differences with various indices for identity evaluation

## Usage

```bash
usage: python -m diff4tbl [OPTION]... FILE1 FILE2

positional arguments:
	file1                 		Path to the first file to compare.
	file2                 		Path to the second file to compare.

optional arguments:
	--help                 		display this help and exit
	-i, --index=INDEX          	name of the index column, focusing comparison based on shared indices
	-c, --column=COLUMN        	compare only the specified columns across the two tables; compares all columns if not provided
	-C, --common-columns       	only compare columns that exist in both tables
	-U, --show-unique          	display unique rows or columns between two tables
	-y, --side-by-side         	display cell differences in a side-by-side tabular format
	-S, --suppress-common      	only show differences, suppress common lines
	-s, --stats					Specify the stats method for columns. Format: --stats --column column1:method1,column2:method2,... Use `--list-stats-methods` to view available methods.
	--list-stats-methods		View available stats methods.
```

## Installation

`diff4tbl` is currently available in source code form. Ensure you have Python and the pandas library installed.
```bash
git clone https://github.com/5uperb0y/diff4tbl.git
cd diff4tbl
python main.py [options]
```

