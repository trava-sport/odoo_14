# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - Manuel Calero
{
    "name": "Sales commissions",
    "version": "13.0.1.0.0",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": ["account", "product", "sale_management", 'agreement', 'sale', 'connector_wb'],
    "website": "https://github.com/OCA/commission",
    "development_status": "Mature",
    "maintainers": ["pedrobaeza"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_commission_view.xml",
        "views/product_template_view.xml",
        "views/сommission_agent_report_view.xml",
        "views/res_partner_view.xml",
        "views/сommission_order_views.xml",
        "report/products_on_sale_views.xml",
        "wizard/create_com_agent_report_views.xml",
    ],
    "installable": True,
}
