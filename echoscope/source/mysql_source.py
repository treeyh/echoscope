# -*- coding: UTF-8 -*-

import logging
from typing import List

from echoscope.config import config
from echoscope.util import mysql_util, str_util, log_util
from echoscope.model import ds_model, config_model
from echoscope.source import source


class MysqlSource(source.Source):
  def __init__(self):
    self.excludesDb = ['information_schema', 'performance_schema', 'mysql', 'sys', 'test']

  def export_model(self, conf: config_model.DataSourceConfig) -> ds_model.DataSourceModel:

    mysqlUtil = mysql_util.get_mysql_util(
        host=conf.host, port=conf.port, user=conf.user, passwd=conf.passwd, db=conf.db, charset=conf.charset)

    ver = self.get_db_version(mysqlUtil)
    if ver == '':
      logging.error(' mysql conn fail. ')
      return
    dsm = ds_model.DataSourceModel(
        name='%s:%d' % (conf.host, conf.port), dbType=config.DsMysql, version=ver)

    dsm.dbs = self.get_export_dbs(mysqlUtil, conf.includes, conf.excludes)

    dsm = self.fill_table_fields(mysqlUtil, dsm)

    return dsm

  def get_db_version(self, conn: mysql_util.MysqlUtil) -> str:
    """获取mysql版本

    Args:
        conn (mysql_util.MysqlUtil): [description]

    Returns:
        str: [description]
    """
    sql = 'select version() as ver from dual'
    cols = ['ver']
    ver = conn.find_one(sql, (), cols)

    return '' if ver == None else str_util.format_bytes_to_str(ver.get('ver', ''))

  def get_export_dbs(self, conn: mysql_util.MysqlUtil, includes: List[str] = [], excludes: List[str] = []) -> List[ds_model.DbModel]:
    """获取需要导出结构的数据库列表

    Args:
        conn (mysql_util.MysqlUtil): 数据库连接
        includes (List[str], optional): 需要包含的数据库列表. Defaults to [].
        excludes (List[str], optional): 需要排除的数据库列表. Defaults to [].

    Returns:
        List[ds_model.DbModel]: 需要导出的数据库列表
    """
    sql = 'select `SCHEMA_NAME` AS db_name, `DEFAULT_CHARACTER_SET_NAME` as charset, `DEFAULT_COLLATION_NAME` as collation_name from `information_schema`.`SCHEMATA` '
    cols = ['db_name', 'charset', 'collation_name']
    data = conn.find_all(sql, (), cols)
    dbs = []

    for d in data:
      db_name = str_util.format_bytes_to_str(d['db_name'])
      if db_name in self.excludesDb or db_name in excludes:
        # 需要过滤
        continue
      if len(includes) > 0 and db_name not in includes:
        # 不包含在include中
        continue

      charset = str_util.format_bytes_to_str(d['charset'])
      collation_name = str_util.format_bytes_to_str(d['collation_name'])
      dbModel = ds_model.DbModel(
          name=db_name, charset=charset, collation_name=collation_name)
      dbs.append(dbModel)

    return dbs

  def fill_table_fields(self, conn: mysql_util.MysqlUtil, dsModel: ds_model.DataSourceModel) -> ds_model.DataSourceModel:
    """获取数据库中的表信息

    Args:
        conn (mysql_util.MysqlUtil): 数据库连接
        dsModel (ds_model.DataSourceModel): 数据源，包含数据库列表

    Returns:
        ds_model.DataSourceModel: 数据源
    """
    sql = ''' select `TABLE_NAME`, `ENGINE`, `TABLE_COLLATION`, `TABLE_COMMENT` from `information_schema`.`TABLES` where `TABLE_SCHEMA` = %s and `TABLE_TYPE` = 'BASE TABLE' '''
    cols = ['TABLE_NAME', 'ENGINE', 'TABLE_COLLATION', 'TABLE_COMMENT']

    for db in dsModel.dbs:
      data = conn.find_all(sql, (db.name, ), cols)
      tables: ds_model.TableModel = []
      for d in data:
        tableName = str_util.format_bytes_to_str(d['TABLE_NAME'])
        comment = str_util.format_bytes_to_str(d['TABLE_COMMENT'])
        collation_name = str_util.format_bytes_to_str(d['TABLE_COLLATION'])
        engine = str_util.format_bytes_to_str(d['ENGINE'])
        table = ds_model.TableModel(
            name=tableName, comment=comment, collation_name=collation_name, engine=engine)
        logging.info('load table:%s fields.' % tableName)
        table.fields = self.get_fields(conn, db.name, tableName)
        table.create_script = self.get_create_script(conn, db.name, tableName)
        tables.append(table)
      db.tables = tables

    return dsModel

  def get_create_script(self, conn: mysql_util.MysqlUtil, dbName: str, tableName: str) -> str:
    """获取表的创建脚本

    Args:
        conn (mysql_util.MysqlUtil): 数据库连接
        dbName (str): 数据库名称
        tableName (str): 表名称

    Returns:
        str: 创建脚本
    """
    sql = ''' SHOW CREATE TABLE `%s`.`%s` ''' % (dbName, tableName)
    cols = ['Table', 'Create Table']
    data = conn.find_one(sql, (), cols)
    return '' if data == None else str_util.format_bytes_to_str(data.get('Create Table', ''))

  def get_fields(self, conn: mysql_util.MysqlUtil, dbName: str, tableName: str) -> List[ds_model.FieldModel]:
    """获取数据表中列信息

    Args:
        conn (mysql_util.MysqlUtil): 数据库连接
        dbName (str): 数据库名
        tableName (str): 表名

    Returns:
        List[ds_model.FieldModel]: 列列表
    """
    sql = ''' select `TABLE_SCHEMA`, `TABLE_NAME`, `COLUMN_NAME`, `ORDINAL_POSITION`, `COLUMN_DEFAULT`, `IS_NULLABLE`, `DATA_TYPE`, `CHARACTER_MAXIMUM_LENGTH`, `NUMERIC_PRECISION`, `NUMERIC_SCALE`,  `CHARACTER_SET_NAME`, `COLLATION_NAME`, `COLUMN_TYPE`, `COLUMN_KEY`, `EXTRA`, `COLUMN_COMMENT`   from `information_schema`.`columns` where `TABLE_SCHEMA` = %s and `TABLE_NAME` = %s ORDER BY `TABLE_SCHEMA` DESC, `TABLE_NAME` DESC, `ORDINAL_POSITION` ASC '''
    cols = ['TABLE_SCHEMA', 'TABLE_NAME', 'COLUMN_NAME', 'ORDINAL_POSITION', 'COLUMN_DEFAULT',
            'IS_NULLABLE', 'DATA_TYPE', 'CHARACTER_MAXIMUM_LENGTH', 'NUMERIC_PRECISION', 'NUMERIC_SCALE',
            'CHARACTER_SET_NAME', 'COLLATION_NAME', 'COLUMN_TYPE', 'COLUMN_KEY', 'EXTRA', 'COLUMN_COMMENT']

    data = conn.find_all(sql, (dbName, tableName, ), cols)

    fields = []
    for d in data:
      fname = str_util.format_bytes_to_str(d['COLUMN_NAME'])
      ftype = str_util.format_bytes_to_str(d['DATA_TYPE'])
      column_type = str_util.format_bytes_to_str(d['COLUMN_TYPE'])
      length = str_util.format_bytes_to_str(
          d['CHARACTER_MAXIMUM_LENGTH']) if d['CHARACTER_MAXIMUM_LENGTH'] != None else str_util.format_bytes_to_str(d['NUMERIC_PRECISION'])
      scale = str_util.format_bytes_to_str(d['NUMERIC_SCALE'])
      # on update CURRENT_TIMESTAMP
      default = str_util.format_bytes_to_str(d['COLUMN_DEFAULT'])
      ext = str_util.format_bytes_to_str(d['EXTRA'])
      if default == 'CURRENT_TIMESTAMP':
        if 'on update CURRENT_TIMESTAMP' in ext:
          default = 'update_time'
        else:
          default = 'create_time'
      nullFlag = str_util.format_bytes_to_str(d['IS_NULLABLE'])
      comment = str_util.format_bytes_to_str(d['COLUMN_COMMENT'])
      charset = str_util.format_bytes_to_str(d['CHARACTER_SET_NAME'])
      collation_name = str_util.format_bytes_to_str(d['COLLATION_NAME'])
      indexFlag = 0
      column_key = str_util.format_bytes_to_str(d['COLUMN_KEY'])
      if column_key == 'PRI':
        indexFlag = 1
      elif column_key == 'UNI':
        indexFlag = 3
      elif column_key == 'MUL':
        indexFlag = 2
      indexName = ''
      autoInc = False
      if 'auto_increment' in ext:
        autoInc = True

      field = ds_model.FieldModel(name=fname, ftype=ftype, column_type=ftype, length=length, scale=scale, default=default, nullFlag=nullFlag,
                                  comment=comment, charset=charset, collation_name=collation_name, indexFlag=indexFlag, indexName=indexName, autoInc=autoInc)
      fields.append(field)
    return fields
