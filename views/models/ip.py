# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

#IP地址组表
class ip_group(models.Model):
    _name = 'cmdb.ip_group'

    name = fields.Char(string='名称')
    region_id = fields.Many2one('cmdb.region',string='关联的逻辑功能区域')
    ip_version = fields.Char(string='IP地址类型')
    cidr = fields.Char(string='关联的逻辑功能区域')
    gateway_ip = fields.Char(string='网关IP地址')
    enable_dhcp = fields.Char(string='是否启用DHCP')

#可分配IP地址池表
class ip_allocation_pool(models.Model):
    _name = 'cmdb.ip_allocation_pool'

    first_ip = fields.Char(string='首个IP')
    last_ip = fields.Char(string='末个IP')
    ip_groups_id = fields.Many2one('cmdb.ip_group',string='关联的IP地址组')

#可用IP地址范围表
class availability_range(models.Model):
    _name = 'cmdb.availability_range'

    allocation_pool_id = fields.Many2one('cmdb.ip_allocation_pool',string='关联的可分配IP地址池')
    first_ip = fields.Char(string='首个可用IP')
    last_ip = fields.Char(string='末个可用IP')

#已分配IP地址表
class ip_allocation(models.Model):
    _name = 'cmdb.ip_allocation'

    name = fields.Char(string='名称')
    interface_id = fields.Many2one('cmdb.interface',string='关联的接口')
    ip_address = fields.Char(string='IP地址')
    region_id= fields.Many2one('cmdb.region',string='关联的逻辑功能区域')
    ip_groups_id= fields.Many2one('cmdb.ip_group',string='关联的地址组')
    interface_id = fields.Many2one('cmdb.interface',)

