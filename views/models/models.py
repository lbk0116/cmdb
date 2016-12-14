# -*- coding: utf-8 -*-
##############################################################################
#
#    Change automatic
#    Copyright (C) 2016-2017 Nantian.
#
#
#
##############################################################################
from openerp import models , fields, api
import re
# from IPy import IP
# import json,sys
# import urllib2,requests
# import cookielib
# from urllib import urlencode
# import os
# import pexpect
# import getpass,os
# import traceback
# import logging
# import systems
# _logger = logging.getLogger(__name__)
# class network_equipment(models.Model):
#     _name = 'cmdb.ne'
#     _rec_name = 'manage_ip'
#
#     name = fields.Char(string=u"设备名称")
#     device_model = fields.Char(string=u'设备型号')
#     device_interface = fields.Char(string=u'管理接口')
#     type = fields.Many2one('cmdb.ne_type',string="equipment_type")
#     type3 = fields.Selection([('IOS','IOS'),('WebNS','WebNS'),('OSX','OSX'),('SOS','SOS'),('AOS','AOS'),('OBSD','OBSD')],string="equipment_type")
#     manage_ip = fields.Char(string=u"管理IP")
#     account_name = fields.Char(string=u"账户名")
#     account_password = fields.Char(string=u"账户密码")
#     notes= fields.Text(string=u"说明")
#     active = fields.Boolean(string=u"有效",default=True)
#
#     _sql_constraints = [('manage_ip_unique','UNIQUE(manage_ip)',"管理IP必须唯一！"),]
#
#     @api.multi
#     def get_type(self):
#         if self.type3 == 'IOS':
#             type = systems.SystemProfiles['IOS']
#         elif self.type3 == 'WebNS':
#             type = systems.SystemProfiles['WebNS']
#         elif self.type3 == 'OSX':
#             type = systems.SystemProfiles['OSX']
#         elif self.type3 == 'SOS':
#             type = systems.SystemProfiles['SOS']
#         elif self.type3 == 'AOS':
#             type = systems.SystemProfiles['AOS']
#         elif self.type3 == 'OBSD':
#             type = systems.SystemProfiles['OBSD']
#         else:
#             pass
#         return type
#
#
#     def ssh_command(self,command):
#         """
#            This runs a command on the remote host. This could also be done with the
#            pxssh class, but this demonstrates what that class does at a simpler level.
#            This returns a pexpect.spawn object. This handles the case when you try to
#            connect to a new host and ssh asks you if you want to accept the public key
#            fingerprint and continue connecting.
#            """
#         ssh_newkey = 'Are you sure you want to continue connecting'
#         # 为 ssh 命令生成一个 spawn 类的子程序对象.
#         child = pexpect.spawn('ssh -l %s %s %s' % (self.account_name, self.manage_ip,command),maxread=2000)
#         #child.send('\n')
#         i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
#         # 如果登录超时，打印出错信息，并退出.
#         if i == 0:  # Timeout
#             print 'ERROR!'
#             print 'SSH could not login. Here is what SSH said:'
#             print child.before, child.after
#             return None
#         # 如果 ssh 没有 public key，接受它.
#         if i == 1:  # SSH does not have the public key. Just accept it.
#             child.sendline('yes')
#             child.expect('password: ')
#             i = child.expect([pexpect.TIMEOUT, 'password: '])
#             if i == 0:  # Timeout
#                 print 'ERROR!'
#             print 'SSH could not login. Here is what SSH said:'
#             print child.before, child.after
#             return None
#         # 输入密码.
#         child.sendline(self.account_password)
#         return child
#
#     @api.multi
#     def show_version(self):
#         command = ['show version']
#         ip = self.env['cmdb.ne'].search([],limit=1)
#         self.env['cmdb.network_management_ip'].create({'device_ip': ip.id,'date':fields.Datetime.now()})
#         ip_device=self.env['cmdb.network_management_ip'].search([('device_ip','=',ip.id)])[-1]
#         for comm in command:
#             child = ip.ssh_command(comm)
#             model_line =''
#             #if comm == 'show version':
#             before = child.before
#             for line in before.splitlines():
#                 if line:
#                     m=re.match('^Model number.*',line)
#                     if m is not None:
#                         model_line=m.group()
#                     n=re.search('.*uptime',line)
#                     if n is not None:
#                         name_line= n.group().split()
#             device_name = name_line[0]
#             model=model_line.split(':')
#             model=model[1].strip()
#             ip_device.update({'version_log': child.before,'device_model':model,'device_name':device_name})
#             #else:
#                 #ip_device.update({'interface_log': child.before})
#     @api.multi
#     def show_interface(self):
#         command = 'show interface'
#         ip = self.env['cmdb.ne'].search([], limit=1)
#         self.env['cmdb.network_management_ip'].create({'device_ip': ip.id, 'date': fields.Datetime.now()})
#         ip_device = self.env['cmdb.network_management_ip'].search([('device_ip', '=', ip.id)])[-1]
#         interfaces = self.env[''].search([('','=',ip_device)])
#         child = ip.ssh_command(command)
#         before = child.before
#         f=open(r'C:\Users\nantian\Desktop\test.txt','r')
#         interface_list = []
#         interface_detail = ''
#         #for line in before.splitlines():
#         for line in f.readlines():
#             if line:
#                 interfaces_detail+=line
#                 if re.search('buffers swapped out', line):
#                     interface_list.append(interface_detail)
#                     interfaces_detail = ''
#         print interface_list
#
#         # for interface in interface_list:
#         #
#         #     for line in interface
#         #
#         #
#         #     ip_device.update({'version_log': child.before, 'device_model': model, 'device_name':device_name})
#
#
