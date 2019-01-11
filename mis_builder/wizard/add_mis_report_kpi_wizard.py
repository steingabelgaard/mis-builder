# -*- coding: utf-8 -*-
# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AddMisReportKpiWizard(models.TransientModel):

    _name = 'add.mis.report.kpi.wizard'
    
    def _get_report_id(self):
        return self.env['mis.report'].browse(self.env.context.get('active_id'))

    account_ids = fields.Many2many('account.account', string='Accounts to add')
    name = fields.Char('Expression', help='{code} will be replaced with the actual account code')
    report_id = fields.Many2one('mis.report',
        string='Report',
        required=True,
        ondelete='cascade',
        default=_get_report_id
    )

    style_id = fields.Many2one(
        string="Style",
        comodel_name="mis.report.style",
        required=False
    )
    style_expression = fields.Char(
        string='Style expression',
        help='An expression that returns a style depending on the KPI value. '
             'Such style is applied on top of the row style.')
    
    budgetable = fields.Boolean(
        default=False,
    )

    inc_acc_code = fields.Boolean('Include Account Code in KPI Description')
    
    @api.multi
    def doit(self):
        for wizard in self:
            if wizard.inc_acc_code:
                desc_fmt = u'{code} {name}'
            else:
                desc_fmt = u'{name}'
            for account in wizard.account_ids:
                
                vals = {'description': desc_fmt.format(code=account.code,
                                                       name=account.name),
                        'style_id': wizard.style_id.id,
                        'style_expression': wizard.style_expression,
                        'report_id': wizard.report_id.id,
                        'expression_ids': [(0, 0, {'name': wizard.name.format(code=account.code)})],
                        'budgetable': wizard.budgetable,
                }

                vals = self.env['mis.report.kpi'].play_onchanges(vals, ['description'])
                self.env['mis.report.kpi'].create(vals)
            
#         action = {
#             'type': 'ir.actions.act_window',
#             'name': 'Action Name',  # TODO
#             'res_model': 'result.model',  # TODO
#             'domain': [('id', '=', result_ids)],  # TODO
#             'view_mode': 'form,tree',
#         }
        return True
