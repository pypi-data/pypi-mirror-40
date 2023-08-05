# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    The useful methods stand here.
"""
import re
import time
from collections import Iterable


def get_host_ip():
    import socket

    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    if hostname == 'bogon':
        return '127.0.0.1'
    return socket.gethostbyname(hostname)


def current_milli_time():
    """
    当前毫秒值

    :return:
    """
    return int(time.time() * 1000)


def strptime_milli_time(time_str, fm):
    """
    时间字符串转毫秒值

    :param time_str:
    :param fm:
    :return:
    """
    return int(time.mktime(time.strptime(time_str, fm)) * 1000)


def is_str_null(s):
    """
    是否为字符串的null

    :param s: str
    :return:
    """
    return isinstance(s, str) and s.lower() == 'null'


def not_str_null(s):
    """
    是否不为字符串的null

    :param s: str
    :return:
    """
    return not is_str_null(s)


def to_hump(s):
    """
    转驼峰命名

    :param s: str
    :return:
    """
    return re.sub(r'_(\w)', lambda m: str(m[1]).upper(), s)


def pick(source, keys, default=None):
    """

    :type source: dict
    :type keys: Iterable
    :param default: 当k对应值不存在时设置默认值
    :return:
    """
    if default:
        return {k: source.get(k, default) for k in keys}
    else:
        return {k: source[k] for k in keys if source.get(k)}


def omit(source, keys):
    """

    :type source: dict
    :type keys: Iterable
    :return:
    """
    return {k: v for k, v in source.items() if k not in keys}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    except TypeError:
        pass
    return False
