# -*- coding: utf-8 -*-
# Copyright 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MisReportInstancePeriod(models.Model):

    _inherit = 'mis.report.instance.period'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account',
        oldname='account_analytic_id', required=False)

    @api.multi
    def _get_additional_move_line_filter(self):
        aml_domain = super(MisReportInstancePeriod, self).\
            _get_additional_move_line_filter()
        # we need sudo because, imagine a user having access
        # to operating unit A, viewing a report with 3 columns
        # for OU A, B, C: in columns B and C, self.operating_unit_ids
        # would be empty for him, and the query on a.m.l would be only
        # restricted by the record rules (ie showing move lines
        # for OU A only). So the report would display values
        # for OU A in all 3 columns.
        sudoself = self.sudo()
        #if sudoself.report_instance_id.account_analytic_id:
        #    aml_domain.append(
        #        ('account_analytic_id', 'child_of',
        #         sudoself.report_instance_id.account_analytic_id.id))
        if sudoself.analytic_account_id:
            aml_domain.append(
                ('analytic_account_id', 'child_of', 
                 sudoself.analytic_account_id.id))
        return aml_domain
    
    @api.multi
    @api.multi
    def _get_additional_budget_item_filter(self):
        aml_domain = super(MisReportInstancePeriod, self).\
            _get_additional_budget_item_filter()
        
        sudoself = self.sudo()
        
        if sudoself.analytic_account_id:
            aml_domain.append(
                ('analytic_account_id', 'child_of', 
                 sudoself.analytic_account_id.id))
        return aml_domain
