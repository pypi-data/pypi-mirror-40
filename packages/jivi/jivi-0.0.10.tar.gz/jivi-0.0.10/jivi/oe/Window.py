from jivi.fs import *
from jivi.oe import *
from jivi.oe.Reader import Reader as oeReader
from jivi.oe.ArHelper import ArHelper
from jivi.oe.StatementReader import StatementReader as SR
from jivi.oe.constants import *

class Window:
	steps = ['set_oeReader','set_window','set_widgets','set_frames','read_frames']
	def __init__(self,environment,fp):
		self.environment = environment
		self.fp = File.fp(fp).lower()
		self.window = {}
		self.frames = {}
		self.widgets = {}
		for a in Window.steps:
			if not getattr(self,a)():
				print('failed ' + a)
				break
		
		
	def set_oeReader(self):
		self.oeReader = oeReader(self.fp)
		if not hasattr(self.oeReader,'new_commands'): return 0
		self.commands = self.oeReader.new_commands
		return 1
		
	def set_window(self):
		found = self.strip_command(['create','window'],1)
		if not found: return 0
		self.window_index = self.strip_command_last_found_index
		found = ArHelper.strip_until(found,'assign')
		if not found: return 0
		self.window = SR.assign(found)
		return self.window
			
	def set_widget(self,ar):
		for i,x in enumerate(ar):
			if x in define_types:
				ar[i] = define_types[x]
				ar[i+1] = ar[i+1].lower()
				widget = dict(type=ar[i],name=ar[i+1])
				ar=ar[i+2:]
				
				if widget['type'] == 'buffer':
					ar,p = ArHelper.strip_property(ar,'for')
					widget['table'] = self.environment.get_table_name(p)
				elif widget['type'] == 'temp-table':
					#self.read_temp_table(...) !todo
					pass
				
				widget['rest'] = ar
				self.widgets[widget['name']] = widget
				return 1
	def set_widgets(self):
		for i,c in enumerate(self.commands):
			if i > self.window_index: return 1
			if c[0] != 'define': continue
			self.set_widget(c)
	
		
	def set_frames(self):
		for name,widget in self.widgets.items():
			if not widget['type'] == 'frame': continue
			self.frames[name] = widget
	

	def read_frames(self):
		for framname,frame in self.frames.items():
			items = []
			with_statement = []
			
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
		
	def brol(self):
		
		global dirs_created
		for a in self.ar:
			if (not self.window) and self.check_window(a): break
			if not (self.window):
				if not self.check_frame(a):
					self.check_def(a)
			else:
				self.check_frame(a)
			
		if not self.window: return
		for a in self.pp:
			tfp = File.fp("tussenstap\\" + a)
			d = File.dir(tfp)
			tfp = d + File.name(a) + ".json"
			
			if not d in dirs_created:
				dirs_created[d] = 1
				Dir.create(d)
				sleep(1)
			if (not self.only_exists) or not File.exists(tfp):
				File.jwrite(tfp,dict(fp=self.fp,window=self.window,ar=self.ar,frames=self.frames,widgets=self.widgets))
			
		

		for f in self.frames.values():
			for x in f['els']:
				n = 0
				for a in x:
					if a == 'at':
						n += 1
				if n != 1:
					File.jwrite("out\\window.json",self.window)
					File.jwrite("out\\ar.json",self.ar)
					File.jwrite("out\\frames.json",self.frames)
					File.jwrite("out\\widgets.json",self.widgets)
					print(self.fp)
					print(x)
					exit()
					
		
			
	
	def check_frame(self,a):
		rest = self.same_ar(a,['define','frame'])
		if not rest: return
		frame_name = rest[0]

		if not frame_name in self.frames:
			self.frames[frame_name] = dict(name=frame_name,els=[],w=[])
		
		rest = rest[1:]
		el = []
		
		i = len(rest) - 1
		while i != -1:
			a = rest[i]
			if a == 'with':
				self.frames[frame_name]['w'].append(rest[i:])
				rest = rest[:i]
				break
			elif a in self.widgets:
				break
			i -= 1
		
		def is_decimal(x):
			try:
				s = float(x)
				return 1
			except:
				return 0
			
		def check_new_widget(x):
			if x in self.widgets: return 1
			if not x.startswith('"') and x.find('.') != -1 and (not is_decimal(x)): return 1
			return 0
		
		for i,x in enumerate(rest):
			if check_new_widget(x):
				if el:
					self.frames[frame_name]['els'].append(el)
					el = []
			elif x == 'view-as' and ((len(el) > 3) or (not el)):
				if el:
					self.frames[frame_name]['els'].append(el[:-1])
					el = el[-1:]
			el.append(x)
		if el:
			self.frames[frame_name]['els'].append(el)
		return 1
	
	def check_frame(self,a):
		rest = self.same_ar(a,['define','frame'])
		if not rest: return
		frame_name = rest[0]

		if not frame_name in self.frames:
			self.frames[frame_name] = dict(name=frame_name,els=[],w=[])
		
		rest = rest[1:]
		el = []
		
		i = len(rest) - 1
		while i != 0:
			a = rest[i]
			if a == 'with':
				self.frames[frame_name]['w'].append(rest[i:])
				rest = rest[:i]
				break
			elif a in self.widgets and (rest[i-1].find('button') == -1):
				break
			i -= 1
		
		def is_decimal(x):
			try:
				s = float(x)
				return 1
			except:
				return 0
			
		def check_new_widget(i,x):
			if x in self.widgets: return 1
			if not x.startswith('"') and (x.find('(') == -1) and x.find('.') != -1 and (not is_decimal(x)): return 1
			return 0
		
		for i,x in enumerate(rest):
			if check_new_widget(i,x):
				if el:
					self.frames[frame_name]['els'].append(el)
					el = []
			elif x == 'view-as' and rest[i+1] == 'text':
				if len(el) > 1:
					self.frames[frame_name]['els'].append(el[:-1])
				el = el[-1:]
			el.append(x)
		if el:
			self.frames[frame_name]['els'].append(el)
		return 1
	
	def check_def(self,a):
		rest = self.same_ar(a,['define'])
		if not rest: return
		found = 0
		for i,x in enumerate(rest):
			if x in define_types:
				rest[i] = define_types[x]
				found = rest[i:]
				break
				
		if not found: return
		self.widgets[found[1]] = found
		
	def has_ar(self,a,b):
		start_ind = -1
		for i,x in enumerate(a):
			if x == b[0]:
				if self.same_ar(a[i:],b):
					return 1
			
	def same_ar(self,a,b):
		try:
			for i,x in enumerate(b):
				if a[i] != x: return 0
			return a[len(b):]
		except:
			return 0
			
	def find_assign(self,a):
		for i,b in enumerate(a):
			if b == 'assign':
				t = {}
				n = i
				n += 1
				while (n + 2) < len(a):
					t[a[n]] = a[n+2]
					n += 3
				return t
			
	def check_window(self,a):
		rest = self.same_ar(a,"if,session:display-type,=".split(','))
		if not rest: return 0
		if not self.has_ar(rest,["create","window"]): return 0
		self.window = self.find_assign(rest)
		return 1
		

def run():

	last_failed = r'c:\develop\l_intex\intex\prg\syslogging.w'
	last_failed_found = 1
	#os.system('del tussenstap\\*.json /s/q/f')
	#ENV.wfiles = [File.fp(fp).lower() for fp in [r'C:\develop\l_intex\Intex\prg\browacoh.w']]
	for fp in ENV.wfiles:
		last_failed_found = last_failed_found or fp == last_failed
		if not last_failed_found: continue
		f = Ana(fp)
		#f = Ana(r'C:\develop\l_intex\Intex\prg\mainartk.w')
		