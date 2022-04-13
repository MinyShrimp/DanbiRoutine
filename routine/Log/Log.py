
from logging import getLogger

class SingletonInstane:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class Log(SingletonInstane):
    logger = getLogger('danbi.routine')

    def get_str( self, msg, *args ):
        _str = msg
        for arg in args:
            _str += " | {}".format(arg)
        return _str

    def error( self, msg: str, *args ):
        self.logger.error( self.get_str( msg, *args ) )

    def info( self, msg: str, *args ):
        self.logger.info( self.get_str( msg, *args ) )

    def warning( self, msg: str, *args ):
        self.logger.warning( self.get_str( msg, *args ) )
    
    def critical( self, msg: str, *args ):
        self.logger.critical( self.get_str( msg, *args ) )