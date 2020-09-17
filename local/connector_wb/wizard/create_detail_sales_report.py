# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class CreateDetailSalesReport(models.TransientModel):
    _name = "create.detail.sales.report"
    _description = "Create detail sales report"

    partner_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, track_visibility='onchange')
    agreement_id = fields.Many2one(
        comodel_name='agreement', string='Agreement',
        track_visibility='onchange', required=True)
    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)
    commercial_partner_id = fields.Many2one(
        'res.partner',
        related='partner_id.commercial_partner_id',
        store=True,
        string='Commercial Entity',
        index=True
    )  
    
    def create_detail_sales_report(self):
        detail_sales_report = self.env['wb.detail.sales.report']
        detail_sales_report.create_report(self.partner_id, self.agreement_id, 
            self.date_from, self.date_to)

        return self.action_view_wb_report()

    def action_view_wb_report(self):
        action = self.env.ref('connector_wb.action_wb_detail_sales_report').read()[0]
        
        return action

