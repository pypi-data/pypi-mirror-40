# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zretry.py
   Author :       Zhang Fan
   date：         19/01/07
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import time


class out_of_max_attempt_count_err(Exception):
    pass


class result_is_retry_flag_err(Exception):
    pass


def _except_retry(func, interval: float = 1, max_attempt_count: int = None,
                  result_retry_flag=None, error_callback=None):
    def decorator(*args, **kw):
        attempt_count = max_attempt_count
        while True:
            try:
                result = func(*args, **kw)
                if result_retry_flag is not None and result is result_retry_flag:
                    raise result_is_retry_flag_err('返回值是重试标记')
                return result
            except:
                if error_callback is not None:
                    error_callback(func)

                if attempt_count is not None:
                    attempt_count -= 1
                if attempt_count == 0:
                    raise out_of_max_attempt_count_err('超出最大尝试次数')

                time.sleep(interval)

    return decorator


class retry():
    def __init__(self, *, interval: float = 1, max_attempt_count: int = None,
                 result_retry_flag: any = None, error_callback=None):
        assert error_callback is None or hasattr(error_callback, '__call__')

    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)

        inst.interval = kwargs.get('interval') or 1
        inst.max_attempt_count = kwargs.get('max_attempt_count') or None
        inst.result_retry_flag = kwargs.get('result_retry_flag') or None
        inst.error_callback = kwargs.get('error_callback') or None

        # @retry方式
        if len(args) == 1:
            return inst(args[0])

        # @retry(...)方式
        return inst

    def __call__(self, func):
        self.func = func
        return _except_retry(func, interval=self.interval, max_attempt_count=self.max_attempt_count,
                             result_retry_flag=self.result_retry_flag, error_callback=self.error_callback)
