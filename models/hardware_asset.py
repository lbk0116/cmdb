# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

#资产元数据表
class property_metadata(models.Model):
    _name = 'cmdb.property_metadata'
    _rec_name = "name"

    name = fields.Char(string="名称", required="True")
    type = fields.Many2one("cmdb.property_metadata", string="类型")
    is_parent = fields.Boolean(string="是否父类", default=0, required=True)

# 资产设备表
class device(models.Model):
    _name = 'cmdb.device'

    name = fields.Char(string="设备名称", required="True")
    # device_login_ip = fields.Char(string="设备登录地址")
    type_id = fields.Many2one("cmdb.property_metadata", string="设备类型", required="True",
                              domain=[('type', 'ilike', "配件类型")])
    manufacturer_id = fields.Many2one("cmdb.property_metadata", string="厂商", required="True",
                                      domain=[('type', 'ilike', "设备品牌")])
    sn = fields.Char(string="序列号", required="True")
    model_id = fields.Many2one("cmdb.property_metadata", string="型号", required="True",
                               domain=[('type', 'ilike', "硬件型号")])
    soft_verison = fields.Char(string="软件版本", required="True")
    inline_owner = fields.Char(string="行内归属人")
    purchase_date = fields.Date(string="设备购入时间")
    manage_ip = fields.Char(string="管理IP")
    manage_type = fields.Selection([('API', 'API'), ('CLI', 'CLI'), ], string="管理类型", default="")
    username = fields.Char(string="用户名")
    password = fields.Char(string="密码")
    status = fields.Char(string="状态")
    area_id = fields.Many2one("cmdb.property_metadata", string="所在地域", domain=[('type', 'ilike', "位置")])
    building_id = fields.Many2one("cmdb.property_metadata", string="所在楼宇", domain=[('type', 'ilike', "位置")])
    room_id = fields.Many2one("cmdb.property_metadata", string="所在机房", domain=[('type', 'ilike', "位置")])
    cabinet_id = fields.Many2one("cmdb.cabinet", string="所在机柜")
    position_u_id = fields.Many2one("cmdb.position_u", string="所在U位")
    used_u= fields.Integer(string="占用U位数")
    department_id = fields.Many2one("hr.department", string="所属部门")
    responsible = fields.Many2one("hr.employee", string="责任人")
    maintenance_start = fields.Date(string="维保起始日期")
    maintenance_end = fields.Date(stirng="维保终止日期")
    contract_purchase_id = fields.Many2one("cmdb.contract_purchase", string="采购合同")
    chassis_id = fields.Many2one("cmdb.property", string="所属机箱")
    business_system_ids = fields.Char(string='关联的业务系统列表')

#机柜表
class cabinet(models.Model):
    _rec_name = "name"
    _name = 'cmdb.cabinet'

    name = fields.Char(string="名称", required="True")
    counts_u = fields.Integer(string="总U数", default="42", required="True")
    area_id = fields.Many2one("cmdb.property_metadata", string="所在地域", required="True")
    building_id = fields.Many2one("cmdb.property_metadata", string="所在楼宇", required="True")
    room_id = fields.Many2one("cmdb.property_metadata", string="所在机房", required="True")

# u位表
class position_u(models.Model):
    _name = "cmdb.position_u"

    name = fields.Char(string="名称")
    status = fields.Boolean(string="状态", default=False)
    cabinet_id = fields.Many2one("cmdb.cabinet", string="所在机柜", required="True")

# 采购合同表
class contract_purchase(models.Model):
    _name = "cmdb.contract_purchase"
    _rec_name = "number"

    name = fields.Char(string="名称")
    number = fields.Char(string="合同编号")