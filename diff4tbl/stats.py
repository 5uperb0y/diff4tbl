class Stats():
	# -------------- Complex Statistics --------------
	def kappa(s1, s2):
		N = len(s1)
		p_o = (s1 == s2).sum() / N
		s1_freq = s1.value_counts() / N
		s2_freq = s2.value_counts() / N
		p_e = (s1_freq * s2_freq).fillna(0).sum()
		coef = (p_o - p_e) / (1 - p_e)
		return coef
	# -------------- Sanity Check Methods --------------
	@classmethod
	def _method_exist(cls, method):
		if method not in cls.methods:
			raise ValueError("Unknown method: " + method)
	@staticmethod
	def _to_type(s, type):
		try:
			return s.astype(type)
		except:
			raise ValueError("Error converting series. Numeric method on a string, a blank, or a missing value?")
	@staticmethod
	def _equal_length(s1, s2):
		if len(s1) != len(s2):
			raise ValueError("Both series must have the same length.")
	@classmethod
	def _ensure_type(cls, method, s):
		cls._method_exist(method)
		return cls._to_type(s, cls.methods[method]["type"])
	# -------------- Deliverable Methods --------------
	@classmethod
	def list_methods(cls):
		for m in cls.methods.keys():
			print(m + ": " + cls.methods[m]["description"])
	@classmethod
	def calculate(cls, method, s1, s2):
		cls._equal_length(s1, s2)
		s1 = cls._ensure_type(method, s1)
		s2 = cls._ensure_type(method, s2)
		return cls.methods[method]["func"](s1, s2)
	@staticmethod
	def show(col, method, stats):
		print(col + "\t" + method + "\t" + str(stats))
	# -------------- Statistics List --------------
	methods = {
		"md": {
			"type": float,
			"func": lambda s1, s2: abs(s2 - s1).mean(),
			"description": "Mean absolute difference between columns"
		},
		"mad": {
			"type": float,
			"func": lambda s1, s2: abs(s2 - s1).median(),
			"description": "Median absolute difference betweeen columns"
		},
		"kappa": {
			"type": str,
			"func": kappa,
			"description": "Cohen's kappa coefficient between columns"
		},
		"identity": {
			"type": str,
			"func": lambda s1, s2: (s2 == s1).sum() / len(s1),
			"description": "Identical cell ratio between columns"
		},
		"corr": {
			"type": float,
			"func": lambda s1, s2: s1.corr(s2),
			"description": "Correlation between columns"
		}
	}
