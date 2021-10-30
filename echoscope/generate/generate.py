# -*- coding: UTF-8 -*-

import logging
import sys
import jinja2

from abc import ABCMeta, abstractmethod

from typing import List

from echoscope.model import ds_model, config_model


class Generate(object):
  """定义导出接口

  Args:
      object ([type]): [description]
  """

  @abstractmethod
  def generateIndexFile(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel) -> str:
    """根据数据模型生成索引文件，需要实现该接口

    Args:
                    conf (config_model.DataSourceConfig): 数据源配置
                    ds (ds_model.DataSourceModel): 数据源模型

    Returns:
                    str: 文件路径
    """
    pass

  @abstractmethod
  def generateFile(self, conf: config_model.DataSourceConfig, ds: ds_model.DataSourceModel) -> str:
    """根据数据模型生成文件，需要实现该接口

    Args:
                    conf (config_model.DataSourceConfig): 数据源配置
                    ds (ds_model.DataSourceModel): 数据源模型

    Returns:
                    str: 文件路径
    """
    pass
