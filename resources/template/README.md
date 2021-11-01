
# {{ setting.docTitle }}

> 生成时间：`{{ setting.nowTime }}`

- [首页](/)
{% for confs in confss %}- {{ confs[0].dsType }}
{% for conf in confs %}  - [{{ conf.name }}]({{ conf.dsType }}/{{conf.code}}/README.md)
{% for db in conf.ds.dbs %}    - [{{ db.name }}]({{ conf.dsType }}/{{conf.code}}/{{db.name}}.md)
{% endfor %}{% endfor %}{% endfor %}