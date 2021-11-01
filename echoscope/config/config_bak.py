# -*- coding: UTF-8 -*-

import os
from typing import List

from echoscope.model import config_model

# 配置文件
# 生成页面title
DocTitle = '数据模型说明'

# 根路径
BasePath = os.getcwd()
# 全局输出路径
ExportPath = os.path.join(BasePath, 'export')
# markdown输出路径
MarkdownExportPath = os.path.join(ExportPath, 'md')
# 模板路径
TemplatePath = os.path.join(BasePath, 'resources', 'template')

# 日志路径
LogPath = os.path.join(ExportPath, 'log.log')

# 数据源类型
DsMysql = 'mysql'
DsClickHouse = 'clickhouse'
# 支持的数据源类型
SupportDsType = [DsMysql, DsClickHouse]

# markdown 建表语句类型
DsMdCreateScriptType = {
    DsMysql: 'sql',
    DsClickHouse: 'clickhouse'
}

# 导出数据类型
ExportTypeMarkdown = 'markdown'


class Config(object):
  """程序配置

  Args:
      object ([type]): [description]
  """

  # 导出数据源配置
  exportDsConfig: List[config_model.DataSourceConfig] = [
      config_model.DataSourceConfig(dsType=DsMysql, host='192.168.223.130', port=3306,
                                    user='root', passwd='mysqlpwd', includes=[], name='测试导出数据库', code='test-export', comment='测试导出数据库'),
      config_model.DataSourceConfig(dsType=DsClickHouse, host='10.0.2.114', port=8123, db='system',
                                    user='bbbbb', passwd='aaaaa', includes=[], name='clickhouse测试环境', code='clickhouse-test', comment='clickhouse测试环境'),
  ]
