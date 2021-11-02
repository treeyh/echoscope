# 数据模型生成

配置文件替换

/echoscope/config/config_bak.py -> /echoscope/config/config.py

修改为需要的配置

需要python3.6以上，开发环境为python3.9，其他版本暂未测试


## 安装执行

项目根目录下：

```bash

# 安装虚拟环境
python -m venv ./venv/

# 激活虚拟环境
# Linux、mac、Unix
$ source ./bin/activate

# windows cms
C:> xxx/Scripts/activate.bat

# windows powershell
PS C:> xxx/Scripts/Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 程序执行
python -m echoscope

```

配置文件说明`./echoscope/config/config.py`：


```python

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
    DsClickHouse: 'sql'
}

# 导出数据类型
ExportTypeMarkdown = 'markdown'


# 导出数据源配置
exportDsConfig: List[config_model.DataSourceConfig] = [
    config_model.DataSourceConfig(dsType=DsMysql, host='192.168.223.130', port=3306,
                                  user='root', passwd='mysqlpwd', includes=[], name='测试导出数据库', code='test-export', comment='测试导出数据库'),
    config_model.DataSourceConfig(dsType=DsClickHouse, host='10.0.2.114', port=8123, db='system',
                                  user='bbbbb', passwd='aaaaa', includes=[], name='clickhouse测试环境', code='clickhouse-test', comment='clickhouse测试环境'),
]

```


输出文件默认目录：

./export/md/


## 部署

将输出文件上传至服务器，启动http服务即可访问：

```python

python3 -m http.server 12004

```