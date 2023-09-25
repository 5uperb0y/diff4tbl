from .args import parse_arguments, get_params, check_arguments
from .load import load_data
from .methods import MapFieldAndMethod
from .stats import Stats
from .proc import Proc
from .diff import Diff
def _parse_and_check_arguments():
	args = parse_arguments()
	check_arguments(args)
	return args, get_params(args)
def _load_and_process_tables(args, params):
	df1 = load_data(args.file1, header = params["header"])
	df2 = load_data(args.file2, header = params["header"])
	dfs = Proc(df1, df2, params)
	return dfs.process()
def _map_stats_method_to_field(args, df):
	mapping = MapFieldAndMethod(args.fields) if args.fields else MapFieldAndMethod(",".join(df.columns))
	mapping.maps()
	return(mapping)
def _calculate_stats(methods, df1, df2):
    for field, method in methods.items():
        result = Stats.calculate(method, df1.sort_index()[field], df2.sort_index()[field])
        Stats.show(field, method, result)
def _compare_tables(df1, df2, params):
	diff_dfs = Diff(df1, df2, params)
	diff_dfs.show()
def main():
	args, params = _parse_and_check_arguments()
	if args.list_stats_methods:
		Stats.list_methods()
		return
	df1, df2 = _load_and_process_tables(args, params)
	# If the user wants to perform statistical analysis, do it and then exit.
	if args.stats:
		mapping = _map_stats_method_to_field(args, df1)
		_calculate_stats(mapping.methods, df1, df2)
		return
	# Otherwise, compare the tables
	_compare_tables(df1, df2, params)
if __name__ == "__main__":
    main()