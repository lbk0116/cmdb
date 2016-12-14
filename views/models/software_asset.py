# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

#应用软件表
class software(models.Model):
    _name = 'cmdb.software'

    name = fields.Char(string='名称')
    desc = fields.Char(string='描述')
    type = fields.Selection([('application','application'),('vswitch','vswitch'),('vrouter','vrouter'),('vlb','vlb'),('vfw','vfw')],string='软件类型')
    soft_version = fields.Char(string='软件版本')
    license = fields.Char(string='许可证号')
    instance_total = fields.Integer(string='可安装个数')
    manage_mode = fields.Selection([('API','API'),('CLI','CLI'),('controller','controller')],string='纳管方式')

#操作系统实例表
class os_instance(models.Model):
    _name = 'cmdb.os_instance'

    name = fields.Char(string='名称')
    desc = fields.Char(string='描述')
    memory = fields.Char(string='内存大小')
    software_id = fields.Many2one('cmdb.software',string='关联软件')
    device_id = fields.Many2one('cmdb.device',string='关联硬件设备')
    region_id = fields.Many2one('cmdb.region',string='所属逻辑功能区')
    route_ids = fields.Char(string='包含的路由')
    business_system_id = fields.Many2one('cmdb.business_system')#关联业务应用表

#应用软件实例表
class software_instance(models.Model):
    _name = 'cmdb.software_instance'

    desc = fields.Char(string='描述')
    software_id = fields.Many2one('cmdb.software')
    os_id = fields.Many2one('cmdb.os_instance')
    responsible = fields.Many2one('hr.employee')

#接口表
class interface(models.Model):
    _name = 'cmdb.interface'

    name = fields.Char(string='接口名称')
    os_id = fields.Many2one('cmdb.os_instance',string='关联的操作系统实例表')
    type = fields.Selection([(u'物理',u'物理'),(u'虚拟',u'虚拟'),('VIP','VIP')],string='类型')
    ip_ids = fields.One2many('cmdb.ip_allocation','interface_id',string='分配的IP地址')
    vlan = fields.Char(string='所属VLAN')
    device_id = fields.Many2one('cmdb.device',string='关联的设备')
    software_instance_id = fields.Many2one('cmdb.software_instance',string='关联的软件')
    vs_id = fields.Char(string='关联的VS')
    region_id = fields.Many2one('cmdb.region',string='网关IP地址')
    mac_address = fields.Char(string='MAC地址')
    status = fields.Char(string='状态')
    link_status = fields.Selection([('up','up'),('down','down')],string='链路状态')
    line_protocol_status = fields.Selection([('up','up'),('down','down')],string='链路协议状态')

#路由表
class route(models.Model):
    _name = 'cmdb.route'

    desc = fields.Char(string='描述')
    src_ip = fields.Char(string='源IP地址')
    src_netmask = fields.Char(string='源IP地址掩码')
    dst_ip = fields.Char(string='目的IP地址')
    dst_netmask = fields.Char(string='目的IP地址掩码')
    next_hop = fields.Char(string='下一跳')
    interface_id = fields.Char(string='关联的路由接口')
    metric = fields.Char(string='度量值')
    os_id = fields.Char(string='关联的操作系统')

#ARP表
class arp(models.Model):
    _name = 'cmdb.arp'
    interface_id = fields.Many2one(string='接口')
    ip = fields.Char(string='IP地址')
    mac_id = fields.Many2one('cmdb.mac',string='关联的MAC地址')
    os_id = fields.Many2one('cmdb.os_instance',string='关联的操作系统')

# NAT表
class nat(models.Model):
    _name = 'cmdb.nat'
    os_id = fields.Many2one('cmdb.os_instance',string='关联的操作系统')
    from_interface = fields.Char(string='源')
    from_ip = fields.Char(string='源IP')
    to_interface = fields.Char(string='目标')
    to_ip = fields.Char(string='目标IP')
    flag = fields.Char(string='标志')

#MAC表
class mac(models.Model):
    _name = 'cmdb.mac'
    interface_type = fields.Selection([(u'物理',u'物理'),('portchannel','portchannel')],string='接口类型')
    interface_id = fields.Many2one('cmdb.interface',string='关联的接口')
    vlan_ids = fields.Many2one('cmdb.vlan',string='关联的所属VLAN')
    mac = fields.Char(string='MAC地址')
    interface_status = fields.Selection([('vlan','vlan'),('trunk','trunk')],string='接口模式')

#vlan表
class vlan(models.Model):
    _name = 'cmdb.vlan'
    name = fields.Char(string='名称')

#license信息表
class license(models.Model):
    _name = 'cmdb.license'
    device_id = fields.Many2one('cmdb.device',string='关联的设备')
    software_id = fields.Many2one('cmdb.software',string='关联的软件')
