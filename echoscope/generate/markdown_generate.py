# -*- coding: UTF-8 -*-

import os
import logging
import sys
import jinja2

from typing import Dict, List

from echoscope.config import config
from echoscope.generate import generate
from echoscope.util import file_util
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
    self.exportPath = exportPath

  def generateIndexFile(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel):

    dbPath = os.path.join(self.exportPath, conf.dsType, conf.code)
    file_util.mkdirs(dbPath, True)
    filePath = os.path.join(dbPath, 'README.md')

    logging.info('start generate conf:%s, ds: %s, filePath: %s' % (conf.code, ds.name, filePath))
    content = self.dsTemplate.render(conf=conf, ds=ds)
    file_util.write_file(filePath=filePath, content=content)
    logging.info('end generate conf:%s, ds: %s' % (conf.code, ds.name))
    return filePath

  def generateFile(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel):

    dbPath = os.path.join(self.exportPath, conf.dsType, conf.code)
    file_util.mkdirs(dbPath, True)
    for db in ds.dbs:
      filePath = os.path.join(dbPath, db.name + '.md')

      logging.info('start generate db: %s, filePath: %s' % (db.name, filePath))

      content = self.dbTemplate.render(conf=conf, db=db)
      file_util.write_file(filePath=filePath, content=content)

      logging.info('end generate db: %s' % db.name)
    return dbPath

  def generateRootIndexFile(self, confss: List[List[config_model.DataSourceConfig]]):
    """生成根目录下索引页面

    Args:
        confs (List[config_model.DataSourceConfig]): 数据源列表
    """

    file_util.mkdirs(self.exportPath, True)
    filePath = os.path.join(self.exportPath, '_sidebar.md')

    logging.info('start generate root index file filePath: %s' % (filePath))
    content = self.sidebarTemplate.render(confss=confss)
    file_util.write_file(filePath=filePath, content=content)
    logging.info('end generate root index file filePath: %s' % (filePath))
    return filePath
