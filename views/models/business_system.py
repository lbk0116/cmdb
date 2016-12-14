# -*- coding: utf-8 -*-
from openerp import models , fields, api


# 业务应用表
class business_system(models.Model):
    _name = 'cmdb.business_system'
    _rec_name = "name"
    
    name = fields.Char(string="名称")
    department_id = fields.Many2one('hr.department', string="department")# 所属部门
    device_ids = fields.Many2many('cmdb.device', string='device')# 关联的硬件资产列表
    # dns_ids = fields.One2many('cmdb.dns', 'business_system_id', string='dns_ids')# 关联的DNS列表
    # os_ids = fields.One2many('cmdb.os_instance', 'business_system_id', string='os')# 关联的操作系统实例列表???
    resource_apply_ids = fields.One2many('cmdb.resource_apply', 'business_system_id', string='resource_apply')# 关联的资源申请列表

    
# 访问规则表
class access_rules(models.Model):
    _name = 'cmdb.access_rules'
    _rec_name = "name"
    
    name = fields.Char(string="名称")
    region_src_id = fields.Many2one('cmdb.region', string="region_src")# 源区域
    region_dst_id = fields.Many2one('cmdb.region', string="region_dst")# 目的区域
    ip_src = fields.Char(string="源IP地址")
    ip_dst = fields.Char(string="目的IP地址")
    action = fields.Selection(
        [
            ('deny', "deny"),
            ('allow', "allow"),
        ],string="动作"
    )

    
# 逻辑功能区域表（对应openstack的network）
class region(models.Model):
    _name = 'cmdb.region'
    _rec_name = "name"
    
    name = fields.Char(string="名称")
    ip_ids = fields.Char(string="关联的IP地址池列表")