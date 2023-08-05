# -*- coding:utf-8 -*-
import csv


class CommonUtils:

    @staticmethod
    def write_csv(file_name, mode='w', write_fn=None):
        """
        write record to csv file
        :param file:
        :param mode: 'r','w'
        :param csvwrite_fn:
        :return:
        """
        with open(file_name, mode) as stream:
            csvwriter = csv.writer(stream)
            write_fn(csvwriter)

    @staticmethod
    def write_h5(file_name, mode='w', db_name='', shape=(1,), dtype='f', data=None):
        import h5py
        h5_file = h5py.File(file_name, mode)
        h5_dataset = h5_file.create_dataset(db_name, shape, data)
        return h5_file

    @staticmethod
    def cycle(iterable=[None]):
        """
        e.g.
        from py_common_util.common.common_utils import CommonUtils
        ...
        iter = CommonUtils.cycle([0,2,3,1])
        next(iter)->0,next(iter)->2,...,next(iter)->0,next(iter)->2,...
        :param iterable: e.g. [0,2,3,1]
        :return:
        """
        from itertools import cycle
        return cycle(iterable)

    @staticmethod
    def datetime_to_int(datetime):
        import time
        return int(time.mktime(datetime.timetuple()))

    @staticmethod
    def int_to_datetime(datetime_int):
        from datetime import datetime
        return datetime.fromtimestamp(datetime_int)

    @staticmethod
    def str_to_datetime(datetime_str, format="%Y%m%d%H%M%S"):
        from datetime import datetime
        return datetime.strptime(datetime_str, format)

    @staticmethod
    def datetime_to_str(date_time, format="%Y%m%d%H%M%S"):
        from datetime import datetime
        return datetime.strftime(date_time, format)  # 将日期转成字面整型字符串, e.g. date: 2009-12-08 16:34:00 -> '20091208163400'

    @staticmethod
    def datetime_now():
        from datetime import datetime
        return datetime.now()