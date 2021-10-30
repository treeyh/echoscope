# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

from typing import List

from echoscope.model import ds_model, config_model


class Source(object):
  """定义导出接口

  Args:
      object ([type]): [description]
  """
  @abstractmethod
  def exportModel(self, conf: config_model.DataSourceConfig) -> ds_model.DataSourceModel:
    """根据数据源导出模型，需要实现该接口

    Args:
        conf (DataSourceConfig): [description]

    Returns:
        ds_model.DataSourceModel: [description]
    """
    pass
