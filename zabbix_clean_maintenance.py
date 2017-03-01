#!/usr/bin/env python
from pyzabbix import ZabbixAPI
from pprint import pprint
import datetime

zapi = ZabbixAPI(url='https://s2s-zabbix-01.serve2serve.com.au/zabbix/', user='gregc', password='28g35J#2')

now = int(datetime.datetime.now().strftime("%s"))
todelete = []

maintenances = zapi.do_request('maintenance.get', {"output": "extend"})

for maint in maintenances['result']:
    if int(maint['active_till']) < now:
        todelete.append(maint['maintenanceid'])

deletes = zapi.do_request('maintenance.delete', todelete)
