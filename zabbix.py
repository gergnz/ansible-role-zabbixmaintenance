#!/usr/bin/env python
from pyzabbix import ZabbixAPI
from pprint import pprint
import datetime

zapi = ZabbixAPI(url='https://s2s-zabbix-01.serve2serve.com.au/zabbix/', user='gregc', password='28g35J#2')

now = int(datetime.datetime.now().strftime("%s"))
soon = now+900

result = zapi.get_id('host','s2s-inf-01.serve2serve.com.au')

x = {}
x['name'] = now
x['active_since'] = now
x['active_till'] = soon
x['hostids'] = [result]
x['timeperiods'] = [
        {
            "timeperiod_type": 0,
            "period": 900
        }
    ]

zapi.do_request('maintenance.create', x)
