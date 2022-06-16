# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Statement Accounting',
    'version': '1.1',
    'summary': 'Accounting Module',
    'description': """
Invoicing & Payments
====================
The specific and easy-to-use Invoicing system in Odoo allows you to keep track of your accounting, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.

You could use this simplified accounting in case you work with an (external) account to keep your books, and you still want to keep track of payments. This module also offers you an easy method of registering payments, without having to encode complete abstracts of account.
    """,

    'images': ['static/description/icon.png'],
    'depends': ['account'],
    'sequence': 13,
    'data': [
        'security/ir.model.access.csv',
        'reports/customer_statement_template_view.xml',
        'reports/vendor_statement_template_view.xml',
        'reports/journal_bank_statement_template_view.xml',
        'reports/journal_cash_statement_template_view.xml',
        'wizard/customer_statement_view.xml',
        'wizard/vedor_statement_view.xml',
        'wizard/journal_bank_statement_view.xml',
        'wizard/journal_cash_statement_view.xml',
        'reports/report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
