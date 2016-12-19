# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models
#已分配IP地址表
class cli_device(models.Model):
    _name = 'cmdb.ip_allocation'

    name = fields.Char(string='名称')


