class Stats():
	methods = {
		"max": {
			"type": float,
			"func": lambda s1, s2: (s2 - s1).max(),
			"description": "Max difference between columns"
		},
		"min": {
			"type": float,
			"func": lambda s1, s2: (s2 - s1).min(),
			"description": "Min difference between columns"
		},
		"mean": {
			"type": float,
			"func": lambda s1, s2: (s2 - s1).mean(),
			"description": "Mean difference between columns"
		},
		"median": {
			"type": float,
			"func": lambda s1, s2: (s2 - s1).median(),
			"description": "Median difference betweeen columns"
		},
		"identity": {
			"type": str,
			"func": lambda s1, s2: (s2 == s1).sum() / len(s1),
			"description": "Identical cell ratio between columns"
		},
		"corr": {
			"type": float,
			"func": lambda s1, s2: (s2 - s1).corr(),
			"description": "Correlation between columns"
		}
	}
	@classmethod
	def list_methods(cls):
		for m in cls.methods.keys():
			print(m + ": " + cls.methods[m]["description"])
	@classmethod
	def ensure_type(cls, method, s):
		if method not in cls.methods:
			raise ValueError("Unknown method: " + method)
		return s.astype(cls.methods[method]["type"])
	@classmethod
	def calculate(cls, method, s1, s2):
		if len(s1) != len(s2):
			raise ValueError("Both series must have the same length.")
		s1 = cls.ensure_type(method, s1)
		s2 = cls.ensure_type(method, s2)
		return cls.methods[method]["func"](s1, s2)
	@classmethod
	def show(cls, col, method, stats):
		print(col + "\t" + method + "\t" + str(stats))