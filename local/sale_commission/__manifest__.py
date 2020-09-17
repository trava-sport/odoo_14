# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - Manuel Calero
{
    "name": "Sales commissions",
    "version": "13.0.1.0.0",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": ["account", "product", "sale_management", 'agreement', 'sale'],
    "website": "https://github.com/OCA/commission",
    "development_status": "Mature",
    "maintainers": ["pedrobaeza"],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_commission_security.xml",
        "views/sale_commission_view.xml",
        "views/product_template_view.xml",
        "views/account_move_views.xml",
        "views/сommission_agent_report_view.xml",
        "views/сommission_order_views.xml",
        "report/sale_commission_analysis_report_view.xml",
        "report/products_on_sale_views.xml",
    ],
    "installable": True,
}
