# -*- encoding: utf-8 -*-

import hashlib
import uuid
import sys
import urllib
from datetime import date, datetime, timedelta
import time
import re
import json

import hmac
import base64


def upper_first_word(inStr):
  ''' 首字母大写 '''
  return inStr[:1].upper() + inStr[1:]


def lower_first_word(inStr):
  ''' 首字母小写 '''
  return inStr[:1].lower() + inStr[1:]


def format_bytes_to_str(val):
  """bytes对象转str

  Args:
      val ([type]): [description]

  Returns:
      [type]: [description]
  """
  vtype = type(val).__name__
  if vtype == 'bytes':
    return val.decode('utf-8', 'replace')
  else:
    return val


def hump2underline(hunp_str):
  '''
  驼峰形式字符串转成下划线形式
  :param hunp_str: 驼峰形式字符串
  :return: 字母全小写的下划线形式字符串
  '''
  # 匹配正则，匹配小写字母和大写字母的分界位置
  p = re.compile(r'([a-z]|\d)([A-Z])')
  # 这里第二个参数使用了正则分组的后向引用
  sub = re.sub(p, r'\1_\2', hunp_str).lower()
  return sub


def underline2hump(underline_str):
  '''
  下划线形式字符串转成驼峰形式
  :param underline_str: 下划线形式字符串
  :return: 驼峰形式字符串
  '''
  # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
  sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
  return sub


def under_score_case_to_camel_case(value):
  if "_" in value:
    """ 
            #方法二：
            strlist = str.split("_")
            Strlist = [s.capitalize() for s in strlist]
            outStr = "".join(Strlist)
            print(outStr)
    """
    # 方法一：
    return "".join(map(lambda x: x.capitalize(), value.split("_")))

  return value.capitalize()
