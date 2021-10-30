# -*- encoding: utf-8 -*-

import time
# pip install mysql-connector-python
import mysql.connector
import logging


class MysqlUtil(object):
  """ MysqlUtil """

  def __init__(self, host, port, user, passwd, db, charset):
    super(MysqlUtil, self).__init__()

    self.host = host
    self.user = user
    self.passwd = passwd
    self.db = db
    self.charset = charset
    self.port = port

  def _getConnection(self):
    i = 0
    count = 5
    while (1):
      try:
        i = i + 1
        conn = mysql.connector.connect(host=self.host, port=self.port,
                                       user=self.user, passwd=self.passwd, db=self.db)  # , use_unicode=True, charset=self.charset,
        return conn
      except BaseException as e:
        logging.error('Error %d: %s' % (e.args[0], e.args[1]))
        if (i >= 3):
          logging.error('sql connection get count %d ' % (count))
          return None
        time.sleep(5)

  def find_one(self, sql, params=(), mapcol=None):
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

  def find_all(self, sql, params=(), mapcol=None):
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


_mysql_utils = {}


def get_mysql_util(host: str, port: int, user: str, passwd: str, db: str, charset: str) -> MysqlUtil:
  global _mysql_utils
  key = '%(host)s_%(port)s_%(user)s_%(db)s' % {
      'host': host, 'port': str(port), 'user': user, 'db': db}
  if None == _mysql_utils.get(key, None):
    mysqlUtils = MysqlUtil(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    _mysql_utils[key] = mysqlUtils

  return _mysql_utils[key]
