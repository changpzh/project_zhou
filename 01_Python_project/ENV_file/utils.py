
#!/usr/bin/python
import sys
import logging

class Cpdlog:
    """
    Cpdlog config
    """
    def __init__(self,logFile,file_level):
        self.MAPPING={"CRITICAL" :50,
           "ERROR" : 40,
           "WARNING" : 30,
           "INFO" : 20,
           "DEBUG" : 10,
           "NOTSET" :0,
           }
        self.config(logFile, file_level)

    def config(self,logFile,file_level):
        self.logger = logging.getLogger(" *Test Report* ")
        self.logger.setLevel(self.MAPPING[file_level])
        self.fh = logging.FileHandler(logFile,mode='w')
        self.fh.setLevel(self.MAPPING[file_level])

        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.MAPPING[file_level])

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s : %(message)s",'%Y-%m-%d %H:%M:%S')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)


    def debug(self,msg):
        if msg is not None:
            self.logger.debug(msg)
    def info(self,msg):
        if msg is not None:
            self.logger.info(msg)
    def warning(self,msg):
        if msg is not None:
            self.logger.warning(msg)
    def error(self,msg):
        if msg is not None:
            self.logger.error(msg)
    def critical(self,msg):
        if msg is not None:
            self.logger.critical(msg)
    def Close(self):
        """Close logger"""
        self.fh.flush()
        self.ch.flush()
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)
        return True