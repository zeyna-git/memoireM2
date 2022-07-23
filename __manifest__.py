# -*- coding: utf-8 -*-
{
    'name': "memoire",

    'sequence': 1,

    'description': """
        Deploiement et gestion de l'infrasture
    """,

    'author': "zeyna BEYE",
    'website': "https://salihate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
            'views/index.xml',
            'views/detail.xml',
            'views/success.xml',
            # 'views/assets.xml',
            # 'menu/menu.xml',
            # 'security/security.xml',
            # 'security/role.xml',
            # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'auto_install': False,
    'application':True,
}