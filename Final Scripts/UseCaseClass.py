class UseCase:
	def __init__(self):
		self.name = ''
		self.components = []
		self.include_UC = []
		self.extend_UC = []
		self.pre_condition = {}
		self.basic_flow = {}
		self.sub_flow = {}
		self.alternate_flow = {}
		self.post_conditions = {}
		

class BasicFlow:
	event = ''
	condition = ''
	action = ''
	associated_sub_flow = []
	associated_alternate_flow_origin = []

class SubFlow:
	description = ''
	action = ''
	associated_flow = []

class AlternateFlow:
	description = ''
	action = ''
	associated_flow_join = []
