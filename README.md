# diff4tbl: Table Comparison Tool
 
`diff4tbl` is a command-line table comparison tool developed in Python, leveraging the Pandas library. Inspired by GNU diff, it also offers functionalities such as data filtering, selective omission of common elements, and discrepancy metrics.


## Overview
`diff4tbl` is developed to aid in the comparison of tables often encountered in research scenarios like bioinformatics and statistical analysis. Given the nature of these tasks, the data might not always be large-scale but can come with complex formatting and various comparison needs. The tool offers:

- `File Format Detection`: recognizes CSV, TSV, and space-separated tables, simplifying the initial setup.
- `Flexible Field and Line Operations`: supports cell-by-cell comparison and advanced field-based operations to tailor the comparison to specific needs.
- `Multiple Layouts`: allows for different display options suitable for various research requirements, such as summarizing differences or preparing data for further analysis.
- `Focused Comparison`: enables the omission of common elements to concentrate on discrepancies.
- `Statistical Overview`: incorporates basic statistical methods to offer an overview of differences across fields.

The utility is designed as a command-line tool, making it easily integrable with other powerful data manipulation utilities.

## Installation and Requirements
`diff4tbli` is compatible with pip for easy installation. Below are the steps to get you started:
```bash
# Clone the repository
$ git clone https://github.com/5uperb0y/diff4tbl.git
# Navigate into the directory
$ cd diff4tbl
# Install the package using pip
$ pip install . 		# Alternatively, you can use `python setup.py install`
# Verify the installation
$ diff4tbl --help		 # This should display the help message
```
## Command-Line Interface (CLI)
Note: The list of options is rather extensive, providing complete control over the comparison task.
```
usage: __main__.py [-h] [--header] [--index INDEX] [--common-index] [--fields FIELDS] [--exclude-fields EXCLUDE_FIELDS]
                   [--common-fields] [--normal | --lines | --context | --stats] [--list-stats-methods]
                   [--suppress-commons | --suppress-common-lines | --suppress-common-fields]
                   [file1] [file2]

A table comparison tool, inspired by GNU diff.

positional arguments:
  file1                 Path to the first file to compare.
  file2                 Path to the second file to compare.

options:
  -h, --help            show this help message and exit
  --header              Include this flag to load tables with headers
  --index INDEX         Name of index fields, focusing comparison based on shared indices
  --common-index        Only compare lines with common indices between tables.
  --fields FIELDS       Specify the fields to be compared across the two tables. Fields should be separated by commas. If
                        not provided, all fields will be compared.
  --exclude-fields EXCLUDE_FIELDS
                        Specify the fields to be excluded from the output. Fields should be separated by commas.
  --common-fields       Only compare fields that exist in both tables.
  --normal              Display a cell-by-cell comparison table. The table includes fields such as line numbers, fields,      
                        values in both files, and their comparison results.
  --lines               Display a line-by-line summary of the common, changed, additional, and deleted lines between tables.  
  --context             Display differences between the tables within a unified table format, highlighting the discrepancies  
                        at the cell level.
  --stats        		Specify the stats method for columns. Format: --stats --column column1:method1,column2:method2,...    
                        Use `--list-stats-methods` to view available methods.
  --list-stats-methods  View available stats methods.
  --suppress-commons    Ignore common lines and fields when comparison. For `--normal` layout, ignore all common cells        
  --suppress-common-lines Ignore common lines when comparison.
  --suppress-common-fields Ignore common fields when comparison.
```

## User Guide
To help you get started, here are some straightforward examples. Consider two TSV files (CSV, space-separated format tables are also supports):

`file1.tsv`, a tsv with number (`N`), judgement (`TF`), and p value (`p`)
```
id	N	TF	p
a1	3	T	0.1
a2	5	F	0.5
a3	4	T	0.2
```
`file2.txv`, a similar TSV file but with addtion lines and some p value changed
```
id	N	TF	p
a1	3	T	0.1
a2	5	T	0.2
a4	2	F	0.6
```

### 1. Basic usage
Then, run the `python -m diff4tbl file1.tsv file2.tsv --context` we could get the comparison as floowing and highlight difference in context.

```
$ python -m diff4tbl file1.tsv file2.tsv --context
0       1       2       3
id      N       TF      p
a1      3       T       0.1
a2      5       F{T}    0.5{0.2}
a3{a4}  4{2}    T{F}    0.2{0.6}
```

By default, `diff4tbl` performs a straightforward positional comparison, which is ideal for tables that are already aligned in terms of index and fields.

This means that no additional or missing fields should be present, and the line numbers should intrinsically indicate the identity of each line in both tables.

If your tables are not pre-processed, as in the sample data provided, you can take advantage of the filtering and field options.
### 2. Filtering and Field Options
Enable the `--header` flag to designate the first row as the table header for subsequent field selection (default use field number as field name).

Then, you could customize your comparison by either including (`--fields`) or excluding (`--exclude-fields`) specific fields.

```
$python -m diff4tbl file1.tsv file2.tsv --context --header --field id,N
id      N
a1      3
a2      5
a3{a4}  4{2}
```

Additionally, use `--index` to set the index field, and employ `--common-index` and `--common-fields` to compare lines or fields that are common between tables, respectively.
```
$ python -m diff4tbl file1.tsv file2.tsv --context --header --index id --common-index
id      N       TF      p
a1      3       T       0.1
a2      5       F{T}    0.5{0.2}
```
### 3. Display Layouts
In addition to `--context` layout, `diff4tbl` offers several display options:

**Standard Comparison** (`--normal`)
provides a detailed, cell-by-cell comparison between tables, utilizing GNU diff-like notation (`""`, `>`, `<`, `|`) to highlight discrepancies.
```
$ python -m diff4tbl file1.tsv file2.tsv --normal --header --index id
a1      id      a1              a1
a1      N       3               3
a1      TF      T               T
a1      p       0.1             0.1
a2      id      a2              a2
a2      N       5               5
a2      TF      F       |       T
a2      p       0.5     |       0.2
a3      id      a3      <
a3      N       4       <
a3      TF      T       <
a3      p       0.2     <
a4      id              >       a4
a4      N               >       2
a4      TF              >       F
a4      p               >       0.6
```
**Line Summary** (`--lines`)
summarizes common, added, deleted, and changed lines for a quick overview of differences.
```
$ python -m diff4tbl file1.tsv file2.tsv --lines --header --index id
common
a1      3       T       0.1
addition
a4      2       F       0.6
deletion
a3      4       T       0.2
change
a2      5       F{T}    0.5{0.2}
```
**Context Display** (`--context`)
displays only the contextual regions around differences for an optimized, focused view. (see example above)

### 4. Selective ommision of common elements
To focus your comparison only on the discrepancies, you can use the `--suppress-common-lines` option that selectively omit common llines:
```
$ python -m diff4tbl file1.tsv file2.tsv --context --header --index id --suppress-common-lines       
id      N       TF      p
a2      5       F{T}    0.5{0.2}
a3{}    4{}     T{}     0.2{}
{a4}    {2}     {F}     {0.6}
```
Here are avaliable options that enable selective ommision of common elements, showing only the elements that require your attention.
- `--suppress-common-lines`: displays only the lines that differ.
- `--suppress-common-fields`: displays only the fields that differ.
- `--suppress-commons`: displays only the differing lines and fields. In `--normal` layout, it restricts the output to unique cells.


### 5. Difference Metrics
The `diff4tbl` tool offers a `--stats` option for generating key statistical data, such as absolute mean differences and correlation coefficients for each field. This function serves to quantify the variances between tables.
```
$ python -m diff4tbl file1.tsv file2.tsv --stats --header --index id --fields id:identity,N:md,TF:kappa,p:corr
id      identity        1.0
N       md      0.0
TF      kappa   0.0
p       corr    0.9999999999999998
```
Currently, the following statistical methods are supported. These can be viewed by using the `--list-stats-methods` option.
```
$ python -m diff4tbl --list-stats-methods
md: Mean absolute difference between columns
mad: Median absolute difference betweeen columns
kappa: Cohen's kappa coefficient between columns
identity: Identical cell ratio between columns
corr: Correlation between columns
```