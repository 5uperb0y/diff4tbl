import pandas as pd
def detect_separator(f_path):
	with open(f_path, "r") as file:
		content = file.read(1024)
	if "\t" in content:
		return "\t"
	elif "," in content:
		return ","
	elif " " in content:
		return " "
	else:
		raise ValueError("Could not determine the separator!")
def load_data(f_path, header = None):
	df = pd.read_csv(f_path, sep = detect_separator(f_path), keep_default_na = False, dtype = str, header = header)
	return df