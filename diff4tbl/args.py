import argparse
import sys
def parse_arguments():
	parser = argparse.ArgumentParser(
		description = "A table comparison tool, inspired by GNU diff.")
	parser.add_argument(
		"file1",
		type = str,
		nargs = '?',
		default = None,
		help = "Path to the first file to compare.")
	parser.add_argument(
		"file2",
		type = str,
		nargs = '?',
		default = None,
		help = "Path to the second file to compare.")
	parser.add_argument(
		"--header",
		action = "store_const",
		const = 0,
		help = "Include this flag to load tables with headers")
	parser.add_argument(
		"--index",
		type = str,
		help = "Name of index fields, focusing comparison based on shared indices")
	parser.add_argument(
		"--common-index",
		action = "store_const",
		const = "common_index",
		help = "Only compare lines with common indices between tables.")
	parser.add_argument(
		"--fields",
		type = str,
		help = "Specify the fields to be compared across the two tables. Fields should be separated by commas. If not provided, all fields will be compared.")
	parser.add_argument(
		"--exclude-fields",
		type = str,
		help = "Specify the fields to be excluded from the output. Fields should be separated by commas.")
	parser.add_argument(
		"--common-fields",
		action = "store_const",
		const = "common_fields",
		help = "Only compare fields that exist in both tables.")
	layout_group = parser.add_mutually_exclusive_group()
	layout_group.add_argument(
		"--normal",
		action = "store_const",
		dest = "layout",
		const = "normal",
		help = "Display a cell-by-cell comparison table. The table includes fields such as line numbers, fields, values in both files, and their comparison results.")
	layout_group.add_argument(
		"--lines",
		action = "store_const",
		dest = "layout",
		const = "lines",
		help = "Display a line-by-line summary of the common, changed, additional, and deleted lines between tables.")
	layout_group.add_argument(
		"--context",
		action = "store_const",
		dest = "layout",
		const = "context",
		help = "Display differences between the tables within a unified table format, highlighting the discrepancies at the cell level.")
	layout_group.add_argument(
		"--stats",
		action = "store_true",
		help = "Specify the stats method for columns. Format: --stats --column column1:method1,column2:method2,... Use `--list-stats-methods` to view available methods.")
	parser.add_argument(
		"--list-stats-methods",
		action = "store_true",
		help = "View available stats methods.")
	suppress_group = parser.add_mutually_exclusive_group()
	suppress_group.add_argument(
		"--suppress-commons",
		action = "store_const",
		dest = "suppress",
		const = "suppress_commons",
		help = "Ignore common lines and fields when comparison. For `--normal` layout, ignore all common cells"
	)
	suppress_group.add_argument(
		"--suppress-common-lines",
		action = "store_const",
		dest = "suppress",
		const = "suppress_common_lines",
		help = "Ignore common lines when comparison."
	)
	suppress_group.add_argument(
		"--suppress-common-fields",
		action = "store_const",
		dest = "suppress",
		const = "suppress_common_fields",
		help = "Ignore common fields when comparison."
	)
	return parser.parse_args()
def check_arguments(args):
	if (not args.file1 or not args.file2) and not args.list_stats_methods:
		sys.exit("error: arguments file1 and file2 are required")
	if args.index and not args.index.isdigit() and args.header is None:
		sys.exit("error: if you're specifying a field as an index, the --header flag is required to properly identify it.")
	if args.index and args.exclude_fields and args.index in args.exclude_fields.split(","):
		sys.exit("error: if you're specifying a field as an index, you should not exlcude it with --exclude-field.")
	if args.fields and args.header is None and not all([x.split(":")[0].isdigit() for x in args.fields.split(",")]):
		sys.exit("error: if you're specifying a field in the table headers, the --header flag is required to properly identify it.")
	if args.exclude_fields and args.header is None and not all([x.isdigit() for x in args.exclude_fields.split(",")]):
		sys.exit("error: if you're specifying a field in the table headers, the --header flag is required to properly identify it.")
def apply_argument_rules(args):
	if args.index and args.fields and args.index not in [x.split(":")[0] for x in args.fields.split(",")]:
		args.fields = f"{args.index},{args.fields}"
	if args.stats:
		args.common_index = True
		args.common_fields = True
	return args
def parse_fields(args):
	return [segment.split(":")[0] for segment in args.fields.split(",")]
def get_params(args):
	args = apply_argument_rules(args)
	fields = parse_fields(args) if args.fields else None
	exclude_fields = args.exclude_fields.split(",") if args.exclude_fields else []
	layout = args.layout if args.layout else "normal"
	suppress = args.suppress if args.suppress else "no_suppress"
	params = {
		"header": args.header,
		"index": args.index,
		"common_fields": args.common_fields,
		"common_index": args.common_index,
		"fields": fields,
		"exclude_fields": exclude_fields,
		"layout": layout,
		"suppress": suppress
	}
	return params