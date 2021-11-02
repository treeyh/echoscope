# -*- coding: UTF-8 -*-

import os
import logging
import sys
import jinja2

from typing import Dict, List

from echoscope.config import config
from echoscope.generate import generate
from echoscope.util import file_util, date_util
from echoscope.model import ds_model, config_model


class MarkdownGenerate(generate.Generate):
  """输出markdown文件

  Args:
      generate ([type]): [description]
  """

  def __init__(self, templatePath: str, exportPath: str):
    """初始化

    Args:
        templatePath (str): 模板路径
        exportPath (str): 输出路径
    """
    self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(templatePath))
    self.dsTemplate = self.env.get_template('ds-template.mdt')
    self.dbTemplate = self.env.get_template('db-template.mdt')
    self.sidebarTemplate = self.env.get_template('_sidebar-template.md')
    self.indexTemplate = self.env.get_template('index.html')
    self.readmeTemplate = self.env.get_template('README.md')
    self.exportPath = exportPath

  def generate_index_file(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel):

    setting = {
        'docTitle': config.DocTitle,
        'nowTime': date_util.get_now_time(),
    }

    dbPath = os.path.join(self.exportPath, conf.dsType, conf.code)
    file_util.mkdirs(dbPath, True)
    filePath = os.path.join(dbPath, 'README.md')

    logging.info('start generate conf:%s, ds: %s, filePath: %s' % (conf.code, ds.name, filePath))
    content = self.dsTemplate.render(conf=conf, ds=ds, setting=setting)
    file_util.write_file(filePath=filePath, content=content)
    logging.info('end generate conf:%s, ds: %s' % (conf.code, ds.name))
    return filePath

  def generate_file(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel):

    setting = {
        'docTitle': config.DocTitle,
        'mdType': config.DsMdCreateScriptType[conf.dsType],
        'nowTime': date_util.get_now_time(),
        'tableTitle': self.get_markdown_table_title(conf.dsType),
    }
    dbPath = os.path.join(self.exportPath, conf.dsType, conf.code)
    file_util.mkdirs(dbPath, True)
    for db in ds.dbs:
      filePath = os.path.join(dbPath, db.name + '.md')

      logging.info('start generate db: %s, filePath: %s' % (db.name, filePath))

      content = self.dbTemplate.render(
          conf=conf, db=db, setting=setting)
      file_util.write_file(filePath=filePath, content=content)

      logging.info('end generate db: %s' % db.name)
    return dbPath

  def generate_root_file(self, confss: List[List[config_model.DataSourceConfig]]):
    """生成根目录下索引页面

    Args:
        confs (List[config_model.DataSourceConfig]): 数据源列表
    """

    setting = {
        'docTitle': config.DocTitle,
        'nowTime': date_util.get_now_time(),
    }
    file_util.mkdirs(self.exportPath, True)
    filePath = os.path.join(self.exportPath, '_sidebar.md')

    logging.info('start generate root index file filePath: %s' % (filePath))
    content = self.sidebarTemplate.render(confss=confss, setting=setting)
    file_util.write_file(filePath=filePath, content=content)
    logging.info('end generate root index file filePath: %s' % (filePath))

    indexFilePath = os.path.join(self.exportPath, 'index.html')
    logging.info('start generate root index html indexFilePath: %s' % (indexFilePath))
    content = self.indexTemplate.render(confss=confss, setting=setting)
    file_util.write_file(filePath=indexFilePath, content=content)
    logging.info('end generate root index html indexFilePath: %s' % (indexFilePath))

    readmeFilePath = os.path.join(self.exportPath, 'README.md')
    logging.info('start generate root redeme md readmeFilePath: %s' % (readmeFilePath))
    content = self.readmeTemplate.render(confss=confss, setting=setting)
    file_util.write_file(filePath=readmeFilePath, content=content)
    logging.info('end generate root readme md readmeFilePath: %s' % (readmeFilePath))

    nojFilePath = os.path.join(self.exportPath, '.nojekyll')
    file_util.write_file(filePath=nojFilePath, content='')

    return filePath

  def get_markdown_table_title(self, dsType: str = 'mysql') -> str:
    """获取markdown标题

    Args:
        dsType (str, optional): 数据源类型. Defaults to 'mysql'.

    Returns:
        str: [description]
    """
    if dsType == config.DsMysql:
      # mysql
      return '| 字段名 | 类型 | 是否可空 | 索引类型 | 默认值 | 描述 |\n| :----- | :--- | :------- | :------- | :----- | :--- |'
    elif dsType == config.DsClickHouse:
      # clickhouse
      return '| 字段名 | 类型 | 默认值 | 分区key | 排序key | 主键key | 描述 |\n| :----- | :--- | :------- | :------- | :----- | :--- | :--- |'

    return ''
