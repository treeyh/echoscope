# -*- coding: UTF-8 -*-

import logging
from typing import List


from echoscope.config import config
from echoscope.util import str_util, log_util, clickhouse_util
from echoscope.model import ds_model, config_model
from echoscope.source import source


class ClickhouseSource(source.Source):
  def __init__(self):
    self.excludesDb = ['default', 'system']

  def export_model(self, conf: config_model.DataSourceConfig) -> ds_model.DataSourceModel:

    clickhouseUtil = clickhouse_util.get_clickhouse_util(
        host=conf.host, port=conf.port, user=conf.user, passwd=conf.passwd, db=conf.db, charset=conf.charset)

    ver = self.get_db_version(clickhouseUtil)
    if ver == '':
      logging.error(' clickhouse conn fail. ')
      return
    dsm = ds_model.DataSourceModel(
        name='%s:%d' % (conf.host, conf.port), dbType=config.DsClickHouse, version=ver)

    dsm.dbs = self.get_export_dbs(clickhouseUtil, conf.includes, conf.excludes)

    dsm = self.fill_table_fields(clickhouseUtil, dsm)

    return dsm

  def get_db_version(self, conn: clickhouse_util.ClickhouseUtil) -> str:
    """获取mysql版本

    Args:
        cursor (clickhouse cursor): [description]

    Returns:
        str: [description]
    """
    sql = 'select version() as ver;'
    cols = ['ver']
    ver = conn.find_one(sql, None, cols)

    return '' if ver == None else str_util.format_bytes_to_str(ver.get('ver', ''))

  def get_export_dbs(self, conn: clickhouse_util.ClickhouseUtil, includes: List[str] = [], excludes: List[str] = []) -> List[ds_model.DbModel]:
    """获取需要导出结构的数据库列表

    Args:
        conn (clickhouse_util.ClickhouseUtil): 数据库连接
        includes (List[str], optional): 需要包含的数据库列表. Defaults to [].
        excludes (List[str], optional): 需要排除的数据库列表. Defaults to [].

    Returns:
        List[ds_model.DbModel]: 需要导出的数据库列表
    """
    sql = 'select name, engine from `system`.databases '
    cols = ['name', 'engine']
    data = conn.find_all(sql, None, cols)
    dbs = []

    for d in data:
      db_name = str_util.format_bytes_to_str(d['name'])
      if db_name in self.excludesDb or db_name in excludes:
        # 需要过滤
        continue
      if len(includes) > 0 and db_name not in includes:
        # 不包含在include中
        continue

      charset = ''
      collation_name = ''
      dbModel = ds_model.DbModel(
          name=db_name, charset=charset, collation_name=collation_name)
      dbs.append(dbModel)

    return dbs

  def fill_table_fields(self, conn: clickhouse_util.ClickhouseUtil, dsModel: ds_model.DataSourceModel) -> ds_model.DataSourceModel:
    """获取数据库中的表信息

    Args:
        conn (clickhouse_util.ClickhouseUtil): 数据库连接
        dsModel (ds_model.DataSourceModel): 数据源，包含数据库列表

    Returns:
        ds_model.DataSourceModel: 数据源
    """
    sql = ''' select database , name , engine , create_table_query , engine_full , partition_key , sorting_key , primary_key , total_rows , total_bytes , comment from `system`.tables  WHERE  database  = %(dbName)s '''
    cols = ['database', 'name', 'engine', 'create_table_query', 'engine_full',
            'partition_key', 'sorting_key', 'primary_key', 'total_rows', 'total_bytes', 'comment']

    for db in dsModel.dbs:
      data = conn.find_all(sql, {'dbName': db.name}, cols)
      tables: ds_model.TableModel = []
      for d in data:
        tableName = str_util.format_bytes_to_str(d['name'])
        comment = str_util.format_bytes_to_str(d['comment'])
        collation_name = ''
        engine = str_util.format_bytes_to_str(d['engine'])
        create_script = self.get_create_script(conn, db.name, tableName)
        table = ds_model.TableModel(
            name=tableName, comment=comment, collation_name=collation_name, engine=engine, create_script=create_script)
        logging.info('load table:%s fields.' % tableName)
        table.fields = self.get_fields(conn, db.name, tableName)
        tables.append(table)
      db.tables = tables

    return dsModel

  def get_create_script(self, conn: clickhouse_util.ClickhouseUtil, dbName: str, tableName: str) -> str:
    """获取表的创建脚本

    Args:
        conn (clickhouse_util.ClickhouseUtil): 数据库连接
        dbName (str): 数据库名称
        tableName (str): 表名称

    Returns:
        str: 创建脚本
    """
    sql = ''' SHOW CREATE TABLE %(dbName)s.%(tableName)s ''' % {
        'dbName': dbName, 'tableName': tableName}
    cols = ['statement']
    data = conn.find_one(sql, None, cols)
    return '' if data == None else str_util.format_bytes_to_str(data.get('statement', ''))

  def get_fields(self, conn: clickhouse_util.ClickhouseUtil, dbName: str, tableName: str) -> List[ds_model.FieldModel]:
    """获取数据表中列信息

    Args:
        conn (clickhouse_util.ClickhouseUtil): 数据库连接
        dbName (str): 数据库名
        tableName (str): 表名

    Returns:
        List[ds_model.FieldModel]: 列列表
    """
    sql = ''' select database , `table` , name , `type` , `position`, default_expression, comment ,  is_in_partition_key , is_in_sorting_key , is_in_primary_key , is_in_sampling_key from `system`.columns c where database = %(dbName)s and `table` = %(tableName)s ORDER BY `position` ASC  '''
    cols = ['database', 'table', 'name', 'type', 'position', 'default_expression', 'comment',
            'is_in_partition_key', 'is_in_sorting_key', 'is_in_primary_key', 'is_in_sampling_key']

    data = conn.find_all(sql, {'dbName': dbName, 'tableName': tableName}, cols)

    fields = []
    for d in data:
      fname = str_util.format_bytes_to_str(d['name'])
      ftype = str_util.format_bytes_to_str(d['type'])
      length = None
      scale = None
      # on update CURRENT_TIMESTAMP
      default = str_util.format_bytes_to_str(d['default_expression'])
      nullFlag = False
      comment = str_util.format_bytes_to_str(d['comment'])
      charset = ''
      collation_name = ''
      indexFlag = 0
      is_in_sorting_key = str_util.format_bytes_to_str(d['is_in_sorting_key'])
      if is_in_sorting_key == '1':
        indexFlag = 1
      indexName = ''
      autoInc = False

      field = ds_model.FieldModel(name=fname, ftype=ftype, length=length, scale=scale, default=default, nullFlag=nullFlag,
                                  comment=comment, charset=charset, collation_name=collation_name, indexFlag=indexFlag, indexName=indexName, autoInc=autoInc)
      fields.append(field)
    return fields
