# -*- coding: utf-8 -*-
# Copyright 2019 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MisMultiReport(models.TransientModel):

    _name = 'mis.multi.report'
    
    def _get_report_id(self):
        return self.env['mis.report'].browse(self.env.context.get('active_id'))

    report_id = fields.Many2one('mis.report.instance',
        string='Report',
        required=True,
        ondelete='cascade',
        default=_get_report_id
    )

    analytic_account_id = fields.Many2one(related='report_id.analytic_account_id')
        
    @api.multi
    def doit(self):
        
        self.ensure_one()
        context = dict(
            self.report_id._context_with_filters(),
        )
        return self.env['report'].with_context(context).get_action(
            self.report_id,
            'mis.report.instance2.xlsx',
        )