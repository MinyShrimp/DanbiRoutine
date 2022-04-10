
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

    def error( self, msg: str ):
        self.logger.error( msg )

    def info( self, msg: str, id: int ):
        self.logger.info( "{} | {}".format(msg, id) )
    
    def warning( self, msg: str ):
        self.logger.warning( msg )
    
    def critical( self, msg: str ):
        self.logger.critical( msg )