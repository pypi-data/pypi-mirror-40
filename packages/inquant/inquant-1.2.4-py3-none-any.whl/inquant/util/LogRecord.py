# -*- coding: utf-8 -*-
import logging
import datetime
import os
import traceback

class LogRecord(object):
    """日志帮助类"""

    __logPath = os.path.dirname(__file__)

    def setLogPath(logPath):
        '''设置日志目录'''
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        LogRecord.__logPath = logPath

    def __getLogger(fileName):

        logger = logging.getLogger(fileName)
        logger.setLevel(level = logging.INFO)

        if not fileName.endswith('.log'):
            fileName += '.log'
        filePath = LogRecord.__logPath + datetime.datetime.now().strftime("%Y%m%d_%H_") + fileName

        if logger.hasHandlers():
            for x in logger.handlers:
                if isinstance(x,logging.FileHandler) and x.baseFilename != os.path.abspath(filePath):
                    logger.removeHandler(x)
                    x.close()

        if len(logger.handlers) <= 0:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.INFO)
            logger.addHandler(consoleHandler)

        if len(logger.handlers) <= 1:
            fileHandler = logging.FileHandler(filePath)
            fileHandler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        return logger

    def writeLog(fileName,msg):
        try:
            logger = LogRecord.__getLogger(fileName)
            logger.info(msg)
        except Exception as e:
            tracelog = traceback.format_exc()
            print(tracelog)
            print(msg)
       

if __name__ == '__main__':
    #新建策略
    LogRecord.setLogPath("d:/home/logs/")
    idx = 0
    while idx < 100000:
        LogRecord.writeLog("logtest",idx)
        LogRecord.writeLog('testerror',idx)
        idx = idx + 1
    print('end of logger')