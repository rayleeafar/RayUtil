import os
import logging
from logging.handlers import TimedRotatingFileHandler


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, level=logging.DEBUG, stream=True, log_dir=None, file_log_level=logging.DEBUG, backup_days=7):
        """
        init a log handler
        """
        self.name = name
        self.level = level
        logging.Logger.__init__(self, name, level=level)
        if stream:
            self.__setStreamHandler__()
        if log_dir:
            if not os.path.isabs(log_dir):
                raise ValueError("log_dir must be a absolute path")
            os.makedirs(log_dir)
            self.__setFileHandler__(log_dir, backup_days, level=file_log_level)

    def __setFileHandler__(self, log_dir, backup_days, level=None):
        """
        set a log file handler
        """
        file_name = os.path.join(log_dir, '{name}.log'.format(name=self.name))
        # save log msg to file_name,back up 15 days
        file_handler = TimedRotatingFileHandler(
            filename=file_name, when='D', interval=1, backupCount=backup_days)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set a stdio stream log handler
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)


if __name__ == '__main__':
    log = LogHandler('test', level=logging.ERROR, log_dir="/tmp/log")
    log.info('this is an info msg,if it shows ,you get a debug! ^x^')
    log.error('this is an erro msg')
