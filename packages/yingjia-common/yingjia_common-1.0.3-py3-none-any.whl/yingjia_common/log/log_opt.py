# coding=utf-8

import logging
import logging.config
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
import inspect
import time
import os


class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode, encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        # if codecs is None:
        #     encoding = None
        encoding = 'utf-8'
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_baseFilename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.baseFilename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()


class MyFileLog:
    '''
    单独的文件log
    '''

    file_dic = {}  # log 字典 如果存在直接返回logger

    def __init__(self, filename):
        self.dirname = 'logs'
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        self.log_file_path = self.dirname + '\\' + filename
        if filename in self.file_dic:
            self.logger = self.file_dic[filename]
        else:
            self.logger = self.init_riqi_log(self.log_file_path)
            self.file_dic[filename] = self.logger

    @staticmethod
    def init_riqi_log(f_name):
        """日期滚动"""
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler(f_name,
                                           when='d',
                                           interval=1,
                                           backupCount=7)
        log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(log_fmt))
        logger.addHandler(console)
        return logger

    @staticmethod
    def init_gundong_log_safe(f_name):
        '''
        日期滚动log,多进程安全, 不带文件删除
        :return:
        '''
        # 日志打印格式
        log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)
        log_file_handler = SafeFileHandler(filename=f_name, mode="a")
        log_file_handler.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger()
        log.addHandler(log_file_handler)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s'))
        log.addHandler(console)
        return log

    @staticmethod
    def get_m_r_p():
        invoked_m = inspect.stack()[2][3]
        row_num = inspect.stack()[2][2]
        file_path = inspect.stack()[2][1]
        file_path = '             ' + file_path
        return (invoked_m, row_num, file_path)

    def debug(self, s):
        m, r, p = self.get_m_r_p()
        self.logger.debug('{},{},{},{}'.format(s, p, r, m))

    def debug_input(self, s):
        m, r, p = self.get_m_r_p()
        self.logger.debug('{},input:{},{},{}'.format(m, s, p, r))

    def debug_return(self, s):
        m, r, p = self.get_m_r_p()
        self.logger.debug('{},return:{},{},{}'.format(m, s, p, r))

    def info(self, s):
        m, r, p = self.get_m_r_p()
        self.logger.info('{},{},{},{}'.format(s, p, r, m))

    def warning(self, ex):
        self.logger.warning(ex)

    def error(self, ex):
        self.logger.error(ex)

    def exception(self, ex):
        self.logger.exception(ex)


if __name__ == '__main__':
    MyFileLog('177').debug('xxx')
    MyFileLog('177').debug('xxx')
