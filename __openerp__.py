# -*- coding: utf-8 -*-
{
    'name': "cmdb",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nantian",
    'website': "http://www.nantian.com.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'cmdb',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/hardware_asset_menu.xml',
        'views/hardware_asset_view.xml',
        'views/business_system_menu.xml',
        # 'views/business_system_view.xml',
        'views/demand_menu.xml',
        'views/software_asset_menu.xml',
        'views/ip_menu.xml',
        'views/sw_menu.xml',
        'views/sw_view.xml',

    ],
    # only loaded in demonstration mode
    'application': True,
}