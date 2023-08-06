# coding=utf-8

import logging
import logging.config
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
import inspect
import time
import os

import os
import re
import datetime
import logging

try:
    import codecs
except ImportError:
    codecs = None


# 作者：有点d伤
# 链接：https://www.jianshu.com/p/d874a05edf19
class MultiprocessHandler(logging.FileHandler):
    """支持多进程的TimedRotatingFileHandler"""
    def __init__(self,filename,when='D',backupCount=30,encoding='utf-8',delay=False):
        """filename 日志文件名,when 时间间隔的单位,backupCount 保留文件个数
        delay 是否开启 OutSteam缓存
            True 表示开启缓存，OutStream输出到缓存，待缓存区满后，刷新缓存区，并输出缓存数据到文件。
            False表示不缓存，OutStrea直接输出到文件"""
        self.prefix = filename
        self.backupCount = backupCount
        self.when = when.upper()
        # 正则匹配 年-月-日
        self.extMath = r"^\d{4}-\d{2}-\d{2}"

        # S 每秒建立一个新文件
        # M 每分钟建立一个新文件
        # H 每天建立一个新文件
        # D 每天建立一个新文件
        self.when_dict = {
            'S':"%Y-%m-%d-%H-%M-%S",
            'M':"%Y-%m-%d-%H-%M",
            'H':"%Y-%m-%d-%H",
            'D':"%Y-%m-%d"
        }
        #日志文件日期后缀
        self.suffix = self.when_dict.get(when)
        if not self.suffix:
            raise ValueError(u"指定的日期间隔单位无效: %s" % self.when)
        #拼接文件路径 格式化字符串
        self.filefmt = os.path.join("","%s.%s" % (self.prefix,self.suffix))  # logs
        #使用当前时间，格式化文件格式化字符串
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        #获得文件夹路径
        _dir = os.path.dirname(self.filefmt)
        try:
            #如果日志文件夹不存在，则创建文件夹
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        except Exception:
            print (u"创建文件夹失败")
            print (u"文件夹路径：" + self.filePath)
            pass

        if codecs is None:
            encoding = None

        logging.FileHandler.__init__(self,self.filePath,'a+',encoding,delay)

    def shouldChangeFileToWrite(self):
        """更改日志写入目的写入文件
        :return True 表示已更改，False 表示未更改"""
        #以当前时间获得新日志文件路径
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        #新日志文件日期 不等于 旧日志文件日期，则表示 已经到了日志切分的时候
        #   更换日志写入目的为新日志文件。
        #例如 按 天 （D）来切分日志
        #   当前新日志日期等于旧日志日期，则表示在同一天内，还不到日志切分的时候
        #   当前新日志日期不等于旧日志日期，则表示不在
        #同一天内，进行日志切分，将日志内容写入新日志内。
        if _filePath != self.filePath:
            self.filePath = _filePath
            return True
        return False

    def doChangeFile(self):
        """输出信息到日志文件，并删除多于保留个数的所有日志文件"""
        #日志文件的绝对路径
        self.baseFilename = os.path.abspath(self.filePath)
        #stream == OutStream
        #stream is not None 表示 OutStream中还有未输出完的缓存数据
        if self.stream:
            #flush close 都会刷新缓冲区，flush不会关闭stream，close则关闭stream
            #self.stream.flush()
            self.stream.close()
            #关闭stream后必须重新设置stream为None，否则会造成对已关闭文件进行IO操作。
            self.stream = None
        #delay 为False 表示 不OutStream不缓存数据 直接输出
        #   所有，只需要关闭OutStream即可
        if not self.delay:
            #这个地方如果关闭colse那么就会造成进程往已关闭的文件中写数据，从而造成IO错误
            #delay == False 表示的就是 不缓存直接写入磁盘
            #我们需要重新在打开一次stream
            #self.stream.close()
            self.stream = self._open()
        #删除多于保留个数的所有日志文件
        if self.backupCount > 0:
            print ('删除日志')
            for s in self.getFilesToDelete():
                print (s)
                os.remove(s)

    def getFilesToDelete(self):
        """获得过期需要删除的日志文件"""
        #分离出日志文件夹绝对路径
        #split返回一个元组（absFilePath,fileName)
        #例如：split('I:\ScripPython\char4\mybook\util\logs\mylog.2017-03-19）
        #返回（I:\ScripPython\char4\mybook\util\logs， mylog.2017-03-19）
        # _ 表示占位符，没什么实际意义，
        dirName,_ = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        #self.prefix 为日志文件名 列如：mylog.2017-03-19 中的 mylog
        #加上 点号 . 方便获取点号后面的日期
        prefix = self.prefix + '.'
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                #日期后缀 mylog.2017-03-19 中的 2017-03-19
                suffix = fileName[plen:]
                #匹配符合规则的日志文件，添加到result列表中
                if re.compile(self.extMath).match(suffix):
                    result.append(os.path.join(dirName,fileName))
        result.sort()

        #返回  待删除的日志文件
        #   多于 保留文件个数 backupCount的所有前面的日志文件。
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """发送一个日志记录
        覆盖FileHandler中的emit方法，logging会自动调用此方法"""
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self,record)
        except (KeyboardInterrupt,SystemExit):
            raise
        except:
            self.handleError(record)


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
        # handler = TimedRotatingFileHandler(f_name,
        #                                    when='d',
        #                                    interval=1,
        #                                    backupCount=7)

        handler = MultiprocessHandler(f_name)
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
    # MyFileLog('177').debug('xxx')
