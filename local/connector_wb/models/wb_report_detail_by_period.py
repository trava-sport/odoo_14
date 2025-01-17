from odoo import api, fields, models


class WBSalesReport(models.Model):
    """ Report detail by period """

    _name = 'wb.report.detail'
    _description = 'Report detail by period'

    realizationreport_id  = fields.Integer('Report number', readonly=True)
    suppliercontract_code  = fields.Char('Contract', readonly=True)
    rr_dt = fields.Date('Transaction date', readonly=True)
    rr_dt_and_time = fields.Datetime('Transaction date and time', readonly=True)
    rrd_id = fields.Char('Line number', readonly=True)
    gi_id = fields.Integer('Delivery number', readonly=True)
    subject_name = fields.Char('Subject', readonly=True)
    nm_id = fields.Integer('Article number', readonly=True)
    brand_name = fields.Char('Brand', readonly=True)
    sa_name = fields.Char('Suppliers article', readonly=True)
    ts_name = fields.Char('Size', readonly=True)
    barcode = fields.Char('Barcode', readonly=True)
    doc_type_name = fields.Char('Document type', readonly=True)
    quantity = fields.Integer('Quantity', readonly=True)
    nds = fields.Integer('VAT rate', readonly=True)
    cost_amount = fields.Float('The Cost Amount', readonly=True)
    retail_price = fields.Integer('Retail price', readonly=True)
    retail_amount = fields.Float('Sales amount(Returns)', readonly=True)
    retail_commission = fields.Float('The amount of the sales Commission', readonly=True)
    sale_percent = fields.Float('The agreed discount', readonly=True)
    commission_percent = fields.Float('The Commission percentage', readonly=True)
    customer_reward = fields.Integer('Remuneration to the buyer', readonly=True)
    supplier_reward = fields.Float('Remuneration to the supplier', readonly=True)
    office_name = fields.Char('Warehouse', readonly=True)
    supplier_oper_name = fields.Char('Justification for payment', readonly=True)
    order_dt = fields.Datetime('Order date', readonly=True)
    sale_dt = fields.Datetime('Date of sale', readonly=True)
    shk_id = fields.Char('SHK', readonly=True)
    retail_price_withdisc_rub = fields.Float('Retail price, subject to the agreed discount', readonly=True)
    for_pay = fields.Float('To transfer to the supplier', readonly=True)
    for_pay_nds = fields.Float('To transfer VAT to the supplier', readonly=True)
    delivery_amount = fields.Integer('Number of deliveries', readonly=True)
    return_amount = fields.Integer('The number of returns', readonly=True)
    delivery_rub = fields.Integer('Cost of logistics', readonly=True)
    gi_box_type_name = fields.Char('Type of boxes', readonly=True)
    product_discount_for_report = fields.Integer('Agreed grocery discount', readonly=True)
    supplier_promo = fields.Integer('Promo code', readonly=True)
    supplier_spp = fields.Integer('Regular customer discount', readonly=True)