# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class AccountMoveLine(models.Model):
    _inherit = ["account.move.line"]
    _name = "account.move.line"

    commission_line_ids = fields.Many2many(
        'commission.agent.report.line',
        'commission_agent_line_invoice_rel',
        'invoice_line_id', 'commission_line_id',
        string='Commission Agent Report Line', readonly=True, copy=False)
