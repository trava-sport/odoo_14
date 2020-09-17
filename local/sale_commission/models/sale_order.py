# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("order_line.agent_ids.remuneration")
    def _compute_commission_total(self):
        for record in self:
            record.commission_total = sum(record.mapped("order_line.agent_ids.remuneration"))

    commission_total = fields.Float(
        string="Commissions", compute="_compute_commission_total", store=True,
    )

    def recompute_lines_agents(self):
        self.mapped("order_line").recompute_agents()

