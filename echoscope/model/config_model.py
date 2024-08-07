# -*- coding: UTF-8 -*-


from typing import List
from echoscope.model import ds_model


class DataSourceConfig(object):
  """数据源配置

  Args:
      object ([type]): [description]
  """

  def __init__(self, dsType: str = 'mysql', host: str = '', port: int = 0, user: str = '', passwd: str = '', db: str = 'information_schema', charset: str = 'utf8mb4', includes: List[str] = [], excludes: List[str] = [], name: str = '', code: str = '', comment: str = '', ds: ds_model.DataSourceModel = None):
    """初始化

    Args:
        dsType (str, optional): 数据源类型. Defaults to 'mysql'.
        host (str, optional): host地址. Defaults to ''.
        port (int, optional): 端口. Defaults to 0.
        user (str, optional): 用户名. Defaults to ''.
        passwd (str, optional): 密码. Defaults to ''.
        db (str, optional): 数据库. Defaults to 'information_schema'.
        charset (str, optional): 字符集. Defaults to 'utf8mb4'.
        includes (List[str], optional): 需要导出的数据库列表，空则是所有. Defaults to [].
        excludes (List[str], optional): 过滤的数据库列表. Defaults to [].
        name (str, optional): 名称. Defaults to ''.
        code (str, optional): 编号，用于生成文件夹命名. Defaults to ''.
        comment (str, optional): 备注描述. Defaults to ''.
        ds (ds_model.DataSourceModel, optional): 备注描述. Defaults to None.
    """
    super(DataSourceConfig, self).__init__()
    self.dsType = dsType
    self.host = host
    self.port = port
    self.user = user
    self.passwd = passwd
    self.db = db
    self.charset = charset
    self.includes = includes
    self.excludes = excludes
    self.name = name
    self.code = code
    self.comment = comment
    self.ds = ds

  def get_folder_name(self):
    """获取文件夹名称"""
    return self.dsType + '-' + self.code

  def __repr__(self):
    """返回一个对象的描述信息"""
    return "{dsType:%s, host:%s, port:%d, user:%s, passwd:%s, db:%s, charset:%s, includes:%s, excludes:%s, name:%s, code:%s, comment:%s}" % (self.dsType, self.host, self.port, self.user, self.passwd, self.db, self.charset, self.includes, self.excludes, self.name, self.code, self.comment)
