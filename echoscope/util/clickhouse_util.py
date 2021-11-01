# -*- encoding: utf-8 -*-

import time
# pip install clickhouse-connector-python
from clickhouse_driver import connect
import traceback
import logging


class ClickhouseUtil(object):
  """ ClickhouseUtil """

  def __init__(self, host, port, user, passwd, db, charset):
    super(ClickhouseUtil, self).__init__()

    self.host = host
    self.user = user
    self.passwd = passwd
    self.db = db
    self.charset = charset
    self.port = port

  def _getConnection(self):
    i = 0
    count = 5
    connUrl = 'clickhouse://%s:%s@%s:%d/%s' % (self.user,
                                               self.passwd, self.host, self.port, self.db)

    while (1):
      try:
        i = i + 1
        # , use_unicode=True, charset=self.charset,
        conn = connect(connUrl)
        return conn
      except BaseException as e:
        logging.error(traceback.format_exc())
        if (i >= 3):
          logging.error('clickhouse connection get count %d ' % (count))
          return None
        time.sleep(5)

  def find_one(self, sql, params=None, mapcol=None):
    conn = self._getConnection()
    c = None
    result = None
    try:
      c = conn.cursor()
      c.execute(sql, params)
      yz = c.fetchone()
      if yz == None:
        return None
      if mapcol == None:
        return yz
      result = self._result_to_map(yz, mapcol)
      return result
    except BaseException as e:
      logging.error('Error %d: %s' % (e.args[0], e.args[1]))
      return result
    finally:
      if None != c:
        c.close()
      if None != conn:
        conn.close()

  def find_all(self, sql, params=None, mapcol=None):
    conn = self._getConnection()
    c = None
    try:
      c = conn.cursor()
      c.execute(sql, params)
      yz = c.fetchall()
      if yz == None:
        return None
      if mapcol == None:
        return yz
      result = []
      for y in yz:
        result.append(self._result_to_map(y, mapcol))
      return result
    except BaseException as e:
      logging.error('sql %s, %s ;Error %d: %s' % (sql, str(params), e.args[0], e.args[1]))
      return result
    finally:
      if None != c:
        c.close()
      if None != conn:
        conn.close()

  def _result_to_map(self, yz, mapcol):
    if yz == None or mapcol == None:
      return None
    if len(yz) != len(mapcol):
      return None
    i = 0
    map = {}
    for y in yz:
      map[mapcol[i]] = y
      i = i + 1
    return map


_clickhouse_utils = {}


def get_clickhouse_util(host: str, port: int, user: str, passwd: str, db: str, charset: str) -> ClickhouseUtil:
  global _clickhouse_utils
  key = '%(host)s_%(port)s_%(user)s_%(db)s' % {
      'host': host, 'port': str(port), 'user': user, 'db': db}
  if None == _clickhouse_utils.get(key, None):
    clickhouseUtils = ClickhouseUtil(host=host, port=port, user=user,
                                     passwd=passwd, db=db, charset=charset)
    _clickhouse_utils[key] = clickhouseUtils

  return _clickhouse_utils[key]
