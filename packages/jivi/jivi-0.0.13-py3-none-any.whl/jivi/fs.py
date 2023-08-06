from jivi.core import *
import math
try:
	from django.utils import timezone
except:
	pass

class Dir:
	@staticmethod
	def up(fp,n=1):
		return Dir.join(fp,('..' + os.sep)*n)

	@staticmethod
	def name(fp):
		return os.path.basename(Dir.fp(fp).rstrip(os.sep))
	
	@staticmethod
	def rel(fp,b):
		return os.path.relpath(fp,b).rstrip(os.sep)
	
	@staticmethod
	def find(fp,fn,deep=1):
		flags = '/b/a-d'
		if deep: flags += '/s'
		fp = Dir.fp(fp)
		s = 'dir {fp}{fn} {flags} 2>nul'.format(fp=Dir.fp(fp),fn=fn,flags=flags)
		for x in Popen(s): yield x
	@staticmethod
	def files(dir,full=1,ex=None,deep=None,img=None):
		if img:
			ex = ['bmp','jpg','jpeg','gif','png']
		dir = Dir.fp(dir)
		flags = '/b/a-d'
		if deep: 
			flags += '/s'
			full = 0
		if ex:
			if isinstance(ex,str): ex = [ex]
		else:
			ex = ["*"]
		s = 'dir {x} {flags} 2>nul'.format(x=" ".join(['"{dir}*.{e}"'.format(dir=dir,e=e) for e in ex]),flags=flags)
		
		for x in Popen(s):
			yield dir + x if full else x
	@staticmethod
	def dirs(dir,full=1,deep=None):
		dir = Dir.fp(dir)
		flags = '/b/ad'
		if deep: 
			flags += '/s'
			full = 0
		s = 'dir "{dir}" {flags} 2>nul'.format(dir=dir,flags=flags)
		for x in Popen(s):
			yield dir + x if full else x
	@staticmethod
	def exists(fp):
		return os.path.isdir(fp)
	@staticmethod
	def join(fp,d=0):
		return Dir.fp(os.path.join(fp,d) if d else fp)
	@staticmethod
	def fp(fp,d=0):
		fp = os.path.join(d,fp) if d else fp
		return os.path.abspath(fp).rstrip(os.sep) + os.sep
	@staticmethod
	def create(fp):
		fp = Dir.fp(fp)
		Command('IF NOT EXIST "{fp}" mkdir "{fp}"'.format(fp=fp))
		return fp
		
class File:
	@staticmethod
	def base(fp):
		return os.path.basename(fp)
	@staticmethod
	def fp(fp,dir=0):
		if dir:
			fp = os.path.join(dir,fp)
		return os.path.abspath(fp)
	@staticmethod
	def modified(fp,dt=False):
		try:
			m =os.path.getmtime(fp)
			if dt:
				return datetime.fromtimestamp(m, tz=timezone.utc)
			return m
		except:
			return 0
	@staticmethod
	def write(fp,s):
		try:
			with open(fp,'w') as f:
				f.write(s)
		except:
			return None
	@staticmethod
	def arwrite(fp,ar):
		try:
			with open(fp,'w') as f:
				f.write("\n".join(ar))
		except:
			return None
	@staticmethod
	def jread(fp,encoding='cp1252'):
		with open(fp,"r",encoding=encoding) as f:
			s = f.read()
			a = json.loads(s)
			return a
	@staticmethod
	def jwrite(fp,ob,indent=4,carefull=0):
		fp = File.fp(fp)
		
		if carefull:
			fp_tmp = File.dir(fp) + File.name(fp) + str(time()) + '.tmp'
			with open(fp_tmp,'w') as f:
				json.dump(ob,f,indent=indent)
			if File.jread(fp_tmp) != None:
				shutil.move(fp_tmp, fp)
				return True
			else:
				File.delete(fp)
		else:
			with open(fp,'w') as f:
				json.dump(ob,f,indent=indent)
	@staticmethod
	def delete(fp):
		try:
			os.remove(fp)
		except:
			return None
	@staticmethod
	def ex(fp,lower=True):
		if lower: return File.ex(fp,lower=False).lower()
		try:
			return os.path.splitext(fp)[1][1:]
		except:
			return ""
	@staticmethod
	def dir(fp):
		return Dir.fp(os.path.dirname(fp))
	@staticmethod
	def name(fp,lower=False):
		if lower: return File.name(fp).lower()
		return os.path.splitext(os.path.basename(fp))[0]
	@staticmethod
	def all(fp):
		try:
			with open(fp,'r') as f:
				x = f.read()
				return x
		except:
			pass
	@staticmethod
	def lines(fp,strip=1):
		try:
			with open(fp,'r') as f:
				x = [a.rstrip() if strip else a for a in f.readlines()]
				return x
		except:
			pass
		return []
	@staticmethod
	def lines_specialx(fp):
		try:
			with open(fp,'r') as f:
				x = []
				for l in f.readlines():
					line = l.rstrip()
					if not line:
						line = " "
					x.append(line)
				
				return x
		except:
			pass
	@staticmethod
	def lines_special(fp):
		
		try:
			x = File.all(fp)
			x = x.splitlines()
			return x
		except:
			pass
	@staticmethod
	def exists(fp):
		return os.path.isfile(fp)
		
	
	
def write_ar(fp,ar,name='ar',type='char'):
	l = len(ar)
	vars = json.dumps(ar)
	
	with open(fp,'w') as f:
		f.write("def var {name} as {type} extent {l} init {vars} no-undo.".format(name=name,type=type,l=l,vars=vars))





class String:
	@staticmethod
	def tabs(s,length):
		
		tabs = math.ceil(length/4)
		tabs_string = math.floor(len(s)/4)
		s = "\t"*max(0,tabs - tabs_string)
		
		return s
	
	@staticmethod
	def tabbed(s,length):
		return s + String.tabs(s,length)
	
		
	@staticmethod
	def tab(tab):
		keys = list(tab.keys())
		max_len = len(max(keys,key=len))
		
		return "\n".join(["{k} : {v}".format(k=String.tabbed(k,max_len),v=tab[k]) for k in keys])

