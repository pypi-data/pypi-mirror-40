from jivi.oe import *
from jivi.fs import *
from jivi.oe.ArHelper import ArHelper
from jivi.oe.ArHelper import StatementReader as SR

class Window:
	steps = ['set_oeReader','set_window','set_defines','write']
	def __init__(self,env,fp):
		self.env = env
		self.fp = File.fp(fp).lower()
		self.window = {}
		self.frames = {}
		self.widgets = {}
		for a in Window.steps:
			if not getattr(self,a)():
				print('failed ' + a)
				break
		
	def write(self):
		File.write("out\\" + File.name(self.fp) + ".html",h)
		
	def get_widget(self,name):
		name = name.lower().strip()
		if name in self.defines:
			return self.defines[name]
		return Field(self.env.get_field_widget(name))
	
	def set_defines(self):
		self.defines = {}
		self.frames = {}
		for a in self.commands:
			if not a: continue
			if Keyword(a[0]) == 'define':
				d = statement(a,self)
				if d.type == 'frame':
					if d.name in self.frames:
						self.frames[d.name].widget_ar += d.widget_ar
						self.frames[d.name].update(d.tab)
						
					else:
						self.frames[d.name] = d
				else:
					self.defines[d.name] = d
					
				continue
				
		return 1
	def set_oeReader(self):
		self.oeReader = Stripper(self.fp)
		self.commands = self.oeReader.commands
		
			
		return 1
		
	def set_window(self):
		found = self.strip_command(['create','window'],1)
		if not found: return 0
		self.window_index = self.strip_command_last_found_index
		found = ArHelper.strip_until(found,'assign')
		if not found: return 0
		self.window = SR.assign(found)
		return self.window
			
	
	
			
	def strip_command(self,ar,fullblock=1):
		for i,c in enumerate(self.commands):
			for j,cl in enumerate(c):
				if cl == ar[0] and ArHelper.same(c[j:],ar):
					ret_val = c[j:]
					if fullblock:
						self.commands = self.commands[:i] + self.commands[i+1 :]
					else:
						self.commands[i] = self.commands[i][:j] + self.commands[i][j+len(ar):]
					self.strip_command_last_found_index = i
					return ret_val
		

