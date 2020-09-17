# Copyright 2016-2019 Tecnativa - Pedro M. Baeza
# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartner(models.Model):
    """Add some fields related to commissions"""

    _inherit = "res.partner"

    commission_id = fields.Many2one(
        string="Commission",
        comodel_name="sale.commission",
        help="This is the default commission used in the sales where this "
        "agent is assigned. It can be changed on each operation if "
        "needed.",
    )
