# -*- coding: UTF-8 -*-

from typing import List

from echoscope.config import config
from echoscope.util import str_util


class FieldModel(object):
  """字段模型

  Args:
      object ([type]): [description]
  """

  def __init__(self, name: str, ftype: str, column_type: str, length: int = 0, scale: int = 0, default: str = '', nullFlag: bool = False, comment: str = '', charset: str = '', collation_name: str = '', indexFlag: int = 0, indexName: str = '', autoInc: bool = False, in_partition_key_flag: int = 0, in_sorting_key_flag: int = 0, in_primary_key_flag: int = 0, in_sampling_key_flag: int = 0):
    """初始化

    Args:
        name (str): 名称
        ftype (str): 字段类型
        column_type (str): 完整字段类型
        length (int, optional): 长度. Defaults to 0.
        scale (int, optional): 小数点后几位. Defaults to 0.
        default (str, optional): 默认值. Defaults to ''.
        nullFlag (bool, optional): 是否可为空. Defaults to False.
        comment (str, optional): 描述. Defaults to ''.
        charset (str, optional): 字符集. Defaults to ''.
        collation_name (str, optional): 字符集. Defaults to 'utf8'.
        indexFlag (int, optional): 索引标识，0非索引，1主键索引，2普通索引，3唯一索引. Defaults to 0.
        indexName (str, optional): 索引名称. Defaults to ''.
        autoInc (bool, optional): 是否自增. Defaults to False.
        in_partition_key_flag (int, optional): 分区key标识. Defaults to 0.
        in_sorting_key_flag (int, optional): 排序key标识. Defaults to 0.
        in_primary_key_flag (int, optional): 主键key标识. Defaults to 0.
        in_sampling_key_flag (int, optional): 抽样key标识. Defaults to 0.
    """
    super(FieldModel, self).__init__()
    self.name = name
    self.ftype = ftype
    self.column_type = column_type
    self.length = length
    self.scale = scale
    self.default = default
    self.nullFlag = nullFlag
    self.comment = comment
    self.charset = charset
    self.collation_name = collation_name
    self.indexFlag = indexFlag
    self.indexName = indexName
    self.autoInc = autoInc
    self.in_partition_key_flag = in_partition_key_flag
    self.in_sorting_key_flag = in_sorting_key_flag
    self.in_primary_key_flag = in_primary_key_flag
    self.in_sampling_key_flag = in_sampling_key_flag

  def get_markdown_table_row(self, dsType: str = 'mysql') -> str:
    """获取markdown表格行

    Args:
        dsType (str, optional): 数据源类型. Defaults to 'mysql'.

    Returns:
        str: [description]
    """
    if dsType == config.DsMysql:
      # mysql
      return '| %s | %s | %s | %s | %s | %s |' % (self.name, self.type_str(), self.null_flag_str(), self.index_flag_str(), self.default_str(), self.comment_str())
    elif dsType == config.DsClickHouse:
      # clickhouse
      return '| %s | %s | %s | %s | %s | %s | %s |' % (self.name, self.type_str(), self.default_str(), self.int_flag_str(self.in_partition_key_flag), self.int_flag_str(self.in_sorting_key_flag), self.int_flag_str(self.in_primary_key_flag), self.comment_str())

    return ''

  def type_str(self) -> str:
    """返回类型str

    Returns:
        str: [description]
    """
    typeStr = self.ftype
    if self.length != None and self.length > 0:
      if self.scale == None or self.scale <= 0:
        typeStr += '(%s)' % self.length
      else:
        typeStr += '(%s, %s)' % (self.length, self.scale)
    return typeStr

  def null_flag_str(self) -> str:
    """返回是否可空str

    Returns:
        str: [description]
    """
    if 'NO' == self.nullFlag:
      return 'N'
    return 'Y'

  def int_flag_str(self, flag: int = 0) -> str:
    """返回int 标识的说明

    Returns:
        str: [description]
    """
    if 1 == flag:
      return 'Y'
    return ''

  def auto_inc_str(self) -> str:
    """返回是否自增str

    Returns:
        str: [description]
    """
    if self.autoInc:
      return 'Y'
    return ''

  def index_flag_str(self) -> str:
    """返回索引类型str

    Returns:
        str: [description]
    """
    if 1 == self.indexFlag:
      return '主键'
    elif 2 == self.indexFlag:
      return '普通'
    elif 3 == self.indexFlag:
      return '唯一'
    return ''

  def default_str(self) -> str:
    """返回默认值str

    Returns:
        str: [description]
    """
    defaultStr = ''
    if self.autoInc:
      defaultStr += '自增'

    if None == self.default:
      return defaultStr

    if '' == self.default:
      return '\'\'' if defaultStr == '' else defaultStr + ', \'\''
    return self.default if defaultStr == '' else defaultStr + ', ' + self.default

  def comment_str(self) -> str:
    """返回默认值str

    Returns:
        str: [description]
    """
    if None == self.comment:
      return ''
    return self.comment.replace('|', '\|').replace('\r\n', '<br />').replace('\n', '<br />')

  def __repr__(self):
    """返回一个对象的描述信息"""
    return "{name:%s, ftype:%s, length:%s, scale:%s, default:%s, nullFlag:%s, comment:%s, charset:%s, collation_name:%s, indexFlag:%s, indexName:%s, autoInc:%s}" % (self.name, self.ftype, self.length, self.scale, self.default, self.nullFlag, self.comment, self.charset, self.collation_name, self.indexFlag, self.indexName, self.autoInc)


class TableModel(object):
  """表模型

  Args:
      object ([type]): [description]
  """

  def __init__(self, name: str, comment: str = '', collation_name: str = 'utf8', engine: str = '', fields: List[FieldModel] = [], create_script: str = ''):
    """初始化

    Args:
        name (str): 名称
        comment (str, optional): 描述. Defaults to ''.
        collation_name (str, optional): 字符集. Defaults to 'utf8'.
        engine (str, optional): db引擎. Defaults to ''.
        fields (List[FieldModel], optional): 字段列表. Defaults to [].
        create_script (str, optional): 创建脚本. Defaults to ''.
    """
    super(TableModel, self).__init__()
    self.name = name
    self.comment = comment
    self.collation_name = collation_name
    self.engine = engine
    self.fields = fields
    self.create_script = create_script

  def __repr__(self):
    """返回一个对象的描述信息"""
    return "{name:%s, comment:%s, collation_name:%s, engine:%s, fields:%s, create_script:%s}" % (self.name, self.comment, self.collation_name, self.engine, self.fields, self.create_script)

  def link_comment(self):
    """输出表名目录跳转链接

    Returns:
        [type]: [description]
    """
    return self.comment.replace(' ', '-')


class DbModel(object):
  """数据库模型

  Args:
      object ([type]): [description]
  """

  def __init__(self, name: str, comment: str = '', charset: str = 'utf8', collation_name: str = '', tables: List[TableModel] = [], create_script: str = ''):
    """初始化

    Args:
        name (str): 名称
        comment (str, optional): 描述. Defaults to ''.
        charset (str, optional): 字符集. Defaults to 'utf8'.
        collation_name (str, optional): [description]. Defaults to ''.
        tables (List[TableModel], optional): 表列表. Defaults to [].
        create_script (str, optional): 创建脚本. Defaults to ''.
    """
    super(DbModel, self).__init__()
    self.name = name
    self.comment = comment
    self.charset = charset
    self.collation_name = collation_name
    self.tables = tables
    self.create_script = create_script

  def __repr__(self):
    """返回一个对象的描述信息"""
    return "{name:%s, comment:%s, charset:%s, collation_name:%s, tables:%s, create_script:%s}" % (self.name, self.comment, self.charset, self.collation_name, self.tables, self.create_script)


class DataSourceModel(object):
  """连接对象模型

  Args:
      object ([type]): [description]
  """

  def __init__(self, name: str, comment: str = '', version: str = '', dbType: str = 'mysql', dbs: List[DbModel] = []):
    """初始化

    Args:
        name (str): 名称
        comment (str, optional): 描述. Defaults to ''.
        version (str, optional): 数据源版本. Defaults to 'version'.
        dbType (str, optional): 类型. Defaults to 'mysql'.
        dbs (List[DbModel], optional): 数据库列表. Defaults to [].
    """
    super(DataSourceModel, self).__init__()
    self.name = name
    self.comment = comment
    self.version = version
    self.dbType = dbType
    self.dbs = dbs

  def __repr__(self):
    """返回一个对象的描述信息"""
    return "{name:%s, comment:%s, version:%s, dbType:%s, dbs:%s}" % (self.name, self.comment, self.version, self.dbType, self.dbs)
