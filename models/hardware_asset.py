# -*- coding: utf-8 -*-bbb
from openerp import fields,api
from openerp import models
import create_sw_record

#资产元数据表
class property_metadata(models.Model):
    _name = 'cmdb.property_metadata'
    _rec_name = "name"

    name = fields.Char(string="名称", required="True")
    type = fields.Many2one("cmdb.property_metadata", string="类型")
    is_parent = fields.Boolean(string="是否父类", default=0)

# 资产设备表
class device(models.Model):
    _name = 'cmdb.device'

    name = fields.Char(string="设备名称", required="True")
    # device_login_ip = fields.Char(string="设备登录地址")
    type_id = fields.Many2one("cmdb.property_metadata", string="设备类型", required="True",
                              domain=[('type', 'ilike', "设备类型")])
    manufacturer_id = fields.Many2one("cmdb.property_metadata", string="厂商", required="True",
                                      domain=[('type', 'ilike', "厂商")])
    sn = fields.Char(string="序列号", required="True")
    model_id = fields.Many2one("cmdb.property_metadata", string="型号", required="True",
                               domain=[('type', 'ilike', "型号")])
    soft_verison = fields.Many2one('cmdb.software',string="软件版本", required="True")
    inline_owner = fields.Char(string="行内归属人")
    purchase_date = fields.Date(string="设备购入时间")
    manage_ip = fields.Char(string="管理IP")
    manage_type = fields.Selection([('API', 'API'), ('CLI', 'CLI'), ], string="纳管方式", default="CLI")
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
    maintenance_end = fields.Date(string="维保终止日期")
    contract_purchase_id = fields.Many2one("cmdb.contract_purchase", string="采购合同")
    chassis_id = fields.Many2one("cmdb.device", string="所属机箱")
    business_system_ids = fields.Char(string='关联的业务系统列表')
    ass_type = fields.Selection([('ilo','ilo'),('hardware','hardware'),('software','software')],string='资产类型')


    @api.multi
    def pop_window(self):
        form_id = self.env['ir.model.data'].search([('name','=','cmdb_device_command_form_view'),('module','=','cmdb')]).res_id
        tree_id = self.env['ir.model.data'].search([('name','=','cmdb_device_command_tree_view'),('module','=','cmdb')]).res_id
        value = {
            'name': ('选择查看信息'),
            'res_model': 'cmdb.show_infomatiaon',
            'views': [[form_id, 'form']],
           # 'view_mode':'tree',
            'type': 'ir.actions.act_window',
            # 'domain': [('id','=',1)],
            'target':'new'
        }
        return value


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

# 执行命令
class show_infomatiaon(models.Model):
    _name = "cmdb.show_infomatiaon"
    _rec_name = "os_id"

    @api.multi
    def _default_os_id(self):
        return self.env['cmdb.os_instance'].browse(self._context.get('active_ids'))
    @api.multi
    def subscribe(self):
        os_id =self.env['cmdb.os_instance'].browse(self._context.get('active_ids'))
        print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        if os_id:
            create_sw_record.create_all(os_id)
            print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
            return {'aaaaaaaaaaaaaa'}
    os_id = fields.Many2one('cmdb.os_instance',string="名称",default = _default_os_id)
    name = fields.Selection([(u'查看接口信息',u'查看接口信息'),(u'查看硬件信息',u'查看硬件信息')],string="合同编号")
