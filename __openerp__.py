# -*- coding: utf-8 -*-
{
    'name': "Provem",

    'summary': """
       Contrato Provem""",

    'description': """
   Personalizaciones
    """,

    'author': "Nayeli Valencia Díaz",
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock','hr'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/layout.xml',
        'reports/report_contrat_determindo.xml',
        'reports/report_contract_indeterminado.xml',
    'reports/report_contrats.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}