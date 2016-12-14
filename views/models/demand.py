# -*- coding: utf-8 -*-
from openerp import models ,fields, api
import business_system

# 需求单表（面向业务部门）
class order(models.Model):
    _name = 'cmdb.order'
    _rec_name = "name"

    name = fields.Char(string="名称")
    applicant_id = fields.Many2one('hr.employee', string="hr")# 申请人
    state = fields.Selection(
        [
            (u'新建需求', u"新建需求"),
            (u'格式检查', u"格式检查"),
            (u'脚本复查', u"脚本复查"),
            (u'脚本执行', u"脚本执行"),
            (u'执行校验', u"执行校验"),
            (u'已关闭', u"已关闭"),
        ],string="需求单状态"
    )
    result = fields.Selection(
        [
            (u'成功', u"成功"),
            (u'异常终止', u"异常终止"),
            (u'回退', u"回退"),
            (u'格式检查失败', u"格式检查失败"),
            (u'脚本复查失败', u"脚本复查失败"),
            (u'校验失败', u"校验失败"),
        ],string="需求单结果"
    )
    server = fields.Text(string='服务器信息')
    lb = fields.Boolean(string="是否需要负载均衡")
    fw = fields.Boolean(string="是否需要防火墙")
    resources_apply_ids = fields.One2many('cmdb.resource_apply', 'order_id', string='resources_apply')#关联的资源申请单列表
    template_id = fields.Char(string="关联的模板ID")

    
# 资源申请表    
class resource_apply(models.Model):
    _name = 'cmdb.resource_apply'
    _rec_name = "name"
    name = fields.Char(string="名称")
    applicant_id = fields.Many2one('hr.employee', string="hr")# 申请人
    error_log = fields.Text(string='需求单处理错误日志')
    format_log = fields.Text(string='需求单优化日志')
    compliance_log = fields.Text(string='需求单合规检查日志')
    compliance_ok = fields.Boolean(string="需求单是否合规")
    type = fields.Selection(
        [
            (u'服务器', u"服务器"),
            (u'交换机', u"交换机"),
            (u'防火墙', u"防火墙"),
            (u'负载均衡', u"负载均衡"),
            (u'DNS', u"DNS"),
        ],string="资源申请类型"
    )
    resource_apply_line_ids = fields.One2many('cmdb.resource_apply_line', 'resource_apply_id', string="resource_apply_line")#关联的资源申请行列表
    business_system_id = fields.Many2one('cmdb.business_system', string="business_system")# 关联的业务应用
    order_id = fields.Many2one('cmdb.order', string="order")# 关联的需求单

    
# 资源申请行表    
class resource_apply_line(models.Model):
    _name = 'cmdb.resource_apply_line'
    _rec_name = "name"
    name = fields.Char(string="名称")
    type = fields.Selection(
        [
            (u'服务器', u"服务器"),
            (u'交换机', u"交换机"),
            (u'防火墙', u"防火墙"),
            (u'负载均衡', u"负载均衡"),
            (u'DNS', u"DNS"),
        ],string="资源申请类型"
    )
    server_name = fields.Char(string="服务器名称")
    server_type = fields.Selection(
        [
            (u'小型机', u"小型机"),
            (u'X86物理机', u"X86物理机"),
            (u'虚拟机', u"虚拟机"),
            (u'容器', u"容器"),
        ],string="服务器类型"
    )
    server_region_id = fields.Many2one('cmdb.region', string="server_region")# 服务器区域
    server_ip = fields.Char(string="服务器IP地址")
    server_device_id = fields.Many2one('cmdb.device', string="server_device")# 关联设备ID
    # server_script_run_id = fields.Many2one('cmdb.script_run', string="server_script_run")# 关联的执行脚本
    # server_script_rollback_id = fields.Many2one('cmdb.script_rollback', string="server_script_rollback")# 关联的回退脚本
    # switch_action_ids = fields.Many2one('cmdb.switch_action_metadata', string="switch_action_metadata")# 关联的交换机动作列表
    # switch_device_id = fields.Many2one('cmdb.device', string="switch_device")# 关联的交换机设备
    # switch_script_run_id = fields.Many2one('cmdb.script_run', string="switch_script_run")# 关联的交换机执行脚本
    # switch_script_rollback_id = fields.Many2one('cmdb.script_rollback', string="switch_script_rollback")# 关联的交换机回退脚本
    # fw_action_ids = fields.Many2one('cmdb.fw_action_metadata', string="fw_action_metadata")# 关联的防火墙动作列表
    # fw_script_run_id = fields.Many2one('cmdb.script_run', string="fw_script_run")# 关联的防火墙执行脚本
    # fw_device_id = fields.Many2one('cmdb.device', string="fw_device")# 关联的防火墙设备
    # fw_script_rollback_id = fields.Many2one('cmdb.script_rollback', string="fw_script_rollback")# 关联的防火墙回退脚本
    # lb_action_ids = fields.Many2one('cmdb.lb_action_metadata', string="lb_action_metadata")# 关联的负载均衡动作列表
    # lb_device_id = fields.Many2one('cmdb.device', string="lb_device")# 关联的负载均衡设备
    # lb_script_run_id = fields.Many2one('cmdb.script_run', string="lb_script_run")# 关联的负载均衡执行脚本
    # lb_script_rollback_id = fields.Many2one('cmdb.script_rollback', string="lb_script_rollback")# 关联的负载均衡回退脚本
    resource_apply_id = fields.Many2one('cmdb.resource_apply', string="resource_apply")# 关联的资源申请单
    status = fields.Selection(
        [
            (u'成功', u"成功"),
            (u'失败', u"失败"),
            (u'拒绝', u"拒绝"),
            (u'等待审批', u"等待审批"),
            (u'等待执行', u"等待执行"),
        ],string="状态"
    )
    
    
# 模板表    
class template(models.Model):
    _name = 'cmdb.template'
    _rec_name = "name"
    name = fields.Char(string="名称")