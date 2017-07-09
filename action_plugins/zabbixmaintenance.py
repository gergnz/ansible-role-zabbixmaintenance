#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native, to_text
from ansible.utils.hashing import checksum_s
from ansible.parsing.yaml.objects import AnsibleUnicode
from pyzabbix import ZabbixAPI
from pprint import pprint
import datetime

class ActionModule(ActionBase):
    ''' Set downtime on zabbix for a host '''

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if self._play_context.check_mode:
            result['skipped'] = True
            result['msg'] = "skipped, this module does not support check_mode."
            return result

        zabbix_url = self._task.args.get('zabbix_url', None)
        zabbix_user = self._task.args.get('zabbix_user', None)
        zabbix_pass = self._task.args.get('zabbix_pass', None)
        maintenance_active = self._task.args.get('zabbix_maintenance_active', 900)
        maintenance_period = self._task.args.get('zabbix_maintenance_period', 900)
        maintenance_host = self._task.args.get('zabbix_maintenance_host', None)

        if (zabbix_url is None or
            zabbix_user is None or
            zabbix_pass is None or
            maintenance_host is None):
                result['failed'] = True
                result['msg'] = "you forgot to provide something, review the docs"
                return result

        zapi = ZabbixAPI(url=zabbix_url, user=zabbix_user, password=zabbix_pass)

        now = int(datetime.datetime.now().strftime("%s"))
        soon = now+maintenance_active

        hostid = zapi.get_id('host', maintenance_host)

        x = {}
        x['name'] = str(maintenance_host) + '-' + str(now)
        x['active_since'] = now
        x['active_till'] = soon
        x['hostids'] = [hostid]
        x['timeperiods'] = [
                {
                    "timeperiod_type": 0,
                    "period": 900
                }
            ]

        final = zapi.do_request('maintenance.create', x)
        result['changed'] = True
        result['msg'] = final
        return result
