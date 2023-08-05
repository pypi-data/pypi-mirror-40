class Window:
	def __init__(self,fp):
		self.fp = File.fp(fp).lower()
		self.window = {}
		self.frames = {}
		self.widgets = {}
		