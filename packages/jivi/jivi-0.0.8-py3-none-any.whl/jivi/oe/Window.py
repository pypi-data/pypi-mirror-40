class Window:
	def __init__(self,environment,fp):
		self.environment = environment
		self.fp = File.fp(fp).lower()
		self.window = {}
		self.frames = {}
		self.widgets = {}
		