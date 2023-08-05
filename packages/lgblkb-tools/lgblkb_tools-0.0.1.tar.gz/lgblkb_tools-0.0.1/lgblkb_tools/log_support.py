import collections
import sys
from timeit import default_timer as timer
import os
import logging
from logging.handlers import TimedRotatingFileHandler as TimedHandler
import logging.handlers as loghandlers
import functools
from python_log_indenter import IndentedLoggerAdapter
from datetime import datetime
from .locations import get_name,create_path,Folder

def create_filter(filter_func,*args,filter_name='',**kwargs):
	class CustomFilter(logging.Filter):
		
		def filter(self,record):
			return filter_func(record.getMessage(),*args,**kwargs)
	
	return CustomFilter(filter_name)

logging.INFORM=INFORM=369
logging.addLevelName(INFORM,"INFORM")

def inform(self,message,*args,**kws):
	# Yes, logger takes its '*args' as 'args'.
	if self.isEnabledFor(INFORM):
		self._log(INFORM,message,args,**kws)

logging.Logger.inform=inform

# region level_mapper:
level_mapper=dict()
level_mapper[logging.DEBUG]=lambda some_logger:some_logger.debug
level_mapper[logging.INFO]=lambda some_logger:some_logger.info
level_mapper[logging.WARNING]=lambda some_logger:some_logger.warning
level_mapper[logging.ERROR]=lambda some_logger:some_logger.error
level_mapper[logging.CRITICAL]=lambda some_logger:some_logger.critical
level_mapper[logging.INFORM]=lambda some_logger:some_logger.inform

# endregion
#todo:Group log files into folder. After expiration, delete folder (if left empty after cleaning).
class TheLogger(IndentedLoggerAdapter):
	
	def __init__(self,name,level=logging.DEBUG,log_format=None,to_stream=True,**kwargs):
		super(TheLogger,self).__init__(logging.Logger(name,level),**dict(dict(spaces=1,indent_char='|---'),**kwargs))
		self.formatter=logging.Formatter(log_format or simple_fmt)
		if to_stream: self.addHandler(logging.StreamHandler())
	
	def addHandler(self,logHandler,level=None,log_format=None):
		logHandler.setLevel(level or self.logger.level)
		if log_format is None: formatter=self.formatter
		else: formatter=logging.Formatter(log_format)
		logHandler.setFormatter(formatter)
		self.logger.addHandler(logHandler)
		return logHandler
	
	def add_timed_handler(self,filepath,when='d',interval=1,backupCount=14,level=None,
	                      log_format=None,**other_opts):
		# filepath=filepath or create_path(1,logs_dir,get_name(self.name)+'.log')
		return self.addHandler(loghandlers.TimedRotatingFileHandler(
			filename=filepath,when=when,interval=interval,backupCount=backupCount,**other_opts),
			level=level,log_format=log_format)
	
	def create_log_file(self,filename,info=None,dir_depth=None,**kwargs):
		modified_info=collections.OrderedDict(file=get_name(filename),
		                                      **(info or {}),datetime=datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),pid=os.getpid())
		if dir_depth is None: dir_depth=len(info or {})+1
		fp=get_logger_filepath(modified_info,dir_depth=dir_depth)
		self.add_timed_handler(fp,**kwargs)
		self.info('log_filepath=%s',fp)
		self.pop()
		# self.info('pid=%s',os.getpid())
		return self
	
	def __getitem__(self,item):
		return level_mapper[item](self)
	
	def inform(self,msg,*args,**kwargs):
		self.logger.inform(msg,*args,**kwargs)

log_fmt="%(asctime)s -- %(levelname)s -- %(name)s -- %(funcName)s -- %(filename)s -- %(lineno)d -- %(message)s"
simple_fmt="%(asctime)s|||pid:%(process)d|||: %(message)s"
logging_level=logging.DEBUG
logs_folder=None

def get_logger_filepath(info: dict,dir_depth=1):
	assert logs_folder is not None and isinstance(logs_folder,)
	kv_pairs=[f'{k}={v}' for k,v in info.items()]
	log_filename="___".join([*kv_pairs[dir_depth:],*kv_pairs[:dir_depth]])
	log_filepath=create_path(1,logs_folder.path,*kv_pairs[:dir_depth],log_filename+'.log')
	return log_filepath

simple_logger=TheLogger('simple_logger')  #create_process_logger(__file__,collections.OrderedDict(pid=os.getpid()))

def with_logging(logger=simple_logger,log_level=logging.INFO):
	logger_say=level_mapper[log_level](logger)
	
	def second_wrapper(func):
		@functools.wraps(func)
		def wrapper(*args,**kwargs):
			logger_say('Running "%s":',func.__name__)
			logger.add()
			
			start=timer()
			try:
				result=func(*args,**kwargs)
			except KeyboardInterrupt:
				logger_say('KeyboardInterrupt within %s. Duration: %s',
				           func.__name__,timer()-start)
				sys.exit()
			except Exception as e:
				logger_say(str(e),exc_info=True)
				raise e
			logger.sub()
			logger_say('Done "%s". Duration: %.3f sec.',func.__name__,timer()-start)
			return result
		
		return wrapper
	
	return second_wrapper

def main():
	return

if __name__=='__main__':
	main()
	pass
