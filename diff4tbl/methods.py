class MapFieldAndMethod:
	def __init__(self, fields = None):
		self.fields = fields
		self.methods = {}
	def _map_default_method(self, segment):
		self.methods[segment] = "identity"
	def _map_custom_method(self, segment):
		field, method = segment.split(":")
		self.methods[field] = method
	def get_parsed_fields(self):
		return list(self.methods.keys())
	def maps(self):
		for segment in self.fields.split(","):
			if ":" in segment:
				self._map_custom_method(segment)
			else:
				self._map_default_method(segment)