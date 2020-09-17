# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class CreateComAgentReport(models.TransientModel):
    _name = "create.com.agent.report"
    _description = "Create agent report"

    partner_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, track_visibility='onchange')
    agreement_id = fields.Many2one(
        comodel_name='agreement', string='Agreement',
        track_visibility='onchange', required=True)
    commission_id = fields.Many2one(string="Commission", comodel_name="sale.commission", required=True)
    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)
    
    def create_com_agent_report(self):
        сom_agent_report = self.env['commission.agent.report']
        сom_agent_report.create_report(self.partner_id, self.agreement_id, 
            self.commission_id, self.date_from, self.date_to)

        return self.action_view_wb_report()

    def action_view_wb_report(self):
        action = self.env.ref('sale_commission_2.action_report_commission_agent').read()[0]
        
        return action

