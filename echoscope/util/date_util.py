# -*- encoding: utf-8 -*-

from datetime import date, datetime, timedelta
import time


def get_now_time():
  """
  获取当前时间
  :return:
  """
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
