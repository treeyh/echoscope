# -*- coding: UTF-8 -*-

import sys
import logging
import argparse
import shutil

from typing import Dict, List

from echoscope.util import file_util, log_util
from echoscope.config import config
from echoscope.model import config_model
from echoscope.source import source, mysql_source, clickhouse_source
from echoscope.generate import generate, markdown_generate

# 源数据导出map
__source_map: Dict[str, source.Source] = {}

# 输出文件类型map
__generate_map: Dict[str, generate.Generate] = {}

__generate = None


def init():
  """初始化
  """
  file_util.mkdirs(config.LogPath, False)
  log_util.log_init(config.LogPath)

  __source_map[config.DsMysql] = mysql_source.MysqlSource()
  __source_map[config.DsClickHouse] = clickhouse_source.ClickhouseSource()

  mdGenerate = markdown_generate.MarkdownGenerate(config.TemplatePath, config.MarkdownExportPath)
  __generate_map[config.ExportTypeMarkdown] = mdGenerate


def _parse_option():
  """获取命令行参数

  Returns:
                  [type]: [description]
  """
  parser = argparse.ArgumentParser(description='Echoscope')
  parser.add_argument('-g', '--generate', type=str, default='markdown',
                      help='generate file type. support: markdown')
  options = parser.parse_args()

  return options, sys.argv[1:]


def main():
  init()
  options, args = _parse_option()

  shutil.rmtree(path=config.MarkdownExportPath, ignore_errors=True)

  confMap: Dict[str, List[config_model.DataSourceConfig]] = {}

  # 生成模型文件
  for dsConfig in config.Config.exportDsConfig:
    logging.info("start generate model file: %s" % dsConfig)

    ds = __source_map[dsConfig.dsType].export_model(conf=dsConfig)
    dsConfig.ds = ds

    filePath = __generate_map[options.generate].generate_index_file(conf=dsConfig, ds=ds)
    logging.info("generate model index file path: %s" % filePath)

    filePath = __generate_map[options.generate].generate_file(conf=dsConfig, ds=ds)

    if confMap.get(dsConfig.dsType, None) == None:
      confMap[dsConfig.dsType] = [dsConfig]
    else:
      confMap[dsConfig.dsType].append(dsConfig)
    logging.info("end generate model file path: %s" % filePath)

  logging.info("start generate root index file ")
  confss: List[List[config_model.DataSourceConfig]] = []

  for dsType in config.SupportDsType:
    print(dsType)
    confs = confMap.get(dsType, None)
    if confs == None:
      continue
    print(dsType)
    confss.append(confs)

  __generate_map[config.ExportTypeMarkdown].generate_root_file(confss)
  logging.info("end generate root index file ")


main()
