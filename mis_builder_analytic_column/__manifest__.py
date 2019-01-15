# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'MIS Builder with Analytic Account on Column',
    'version': '10.0.1.0.0',
    'category': 'Reporting',
    "author": "Stein & Gabelgaard ApS, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    'website': 'http://www.github.com/OCA/mis_builder',
    'depends': ['mis_builder_budget'],
    'data': [
        'view/mis_builder.xml',
        'security/mis_builder_security.xml'
    ],
    'installable': True,
}
