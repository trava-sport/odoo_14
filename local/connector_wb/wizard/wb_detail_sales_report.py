from itertools import groupby


from odoo import _, api, exceptions, fields, models
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang, get_lang
from odoo.exceptions import AccessError, UserError, ValidationError


class WBDetailSalesReport(models.Model):
    _name = "wb.detail.sales.report"
    _description = "Detailed sales reports"
    _inherit = ['portal.mixin', "mail.thread", "mail.activity.mixin", 'utm.mixin']


    name = fields.Char(string='Report number', required=True, copy=False, readonly=True, index=True, default=lambda self:self.env['ir.sequence'].next_by_code('commission.agent.report'))
    date_report = fields.Date(required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, track_visibility='onchange')
    partner_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='onchange')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, track_visibility='onchange')
    start_date = fields.Date(required=True, readonly=True, copy=False, track_visibility='onchange')
    end_date = fields.Date(required=True, readonly=True, copy=False, track_visibility='onchange')
    agreement_id = fields.Many2one(
        comodel_name='agreement', string='Agreement', ondelete='restrict',
        track_visibility='onchange', required=True, copy=False,
        states={'draft': [('readonly', False)]})
    sales_amount = fields.Monetary(string='Sales amount', store=True, readonly=True, compute='_sales_amount', tracking=4)
    amount_commission_wb = fields.Monetary(string='Commission WB', store=True, readonly=True, compute='_amount_commission_wb')
    amount_transfer_supplier = fields.Monetary(string='To transfer to the supplier', store=True, readonly=True, compute='_amount_transfer_supplier')
    total_percentage_WB = fields.Integer(string='Total percentage of the WB', store=True, readonly=True, compute='_amount_commission_wb')
    logistics = fields.Monetary(string='Logistics', store=True, readonly=True, compute='_logistics')
    percentage_logistic = fields.Integer(string='Percentage of logistics', store=True, readonly=True, compute='_percentage_logistic')
    warehouse_storage = fields.Monetary(string='Warehouse storage', required=True, default=0)
    percentage_storage = fields.Integer(string='Percentage of storage', store=True, readonly=True, compute='_percentage_storage')
    received_bank_account = fields.Monetary(string='Received to your Bank account', required=True, default=0)
    sum_wholesale_prices = fields.Monetary(string='Sum of the wholesale prices', store=True, readonly=True, compute='_sum_wholesale_prices')
    percentage_purchases = fields.Integer(string='Percentage of purchases', store=True, readonly=True, compute='_percentage_purchases')
    amount_net_income = fields.Integer(string='Amount of net income', store=True, readonly=True, compute='_amount_net_income')
    percentage_net_income = fields.Integer(string='Percentage of net income', store=True, readonly=True, compute='_percentage_net_income')
    total_number_sales = fields.Integer(string='Total number of sales', store=True, readonly=True, compute='_total_number_sales')
    average_wholesale_price = fields.Float(string='Average wholesale price', store=True, readonly=True, compute='_average_wholesale_price')
    average_selling_price = fields.Float(string='Average selling price', store=True, readonly=True, compute='_average_selling_price')
    total_number_sales_ekb = fields.Integer(string='Ekaterinburg', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_kras = fields.Integer(string='Krasnodar', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_kazan = fields.Integer(string='Kazan', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_novosib = fields.Integer(string='Novosibirsk', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_spb = fields.Integer(string='Saint Petersburg', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_khab = fields.Integer(string='Khabarovsk', store=True, readonly=True, compute='_total_number_sales')
    total_number_sales_koledino = fields.Integer(string='Koledino', store=True, readonly=True, compute='_total_number_sales')

    report_line = fields.One2many('wb.detail.sales.report.line', 'report_id', string='Sales Report Lines', copy=True, auto_join=True)

    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True, required=True, default=lambda self: self.env.company.currency_id.id)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    

    @api.depends('report_line.retail_price_withdisc_rub')
    def _sales_amount(self):
        self.sales_amount = sum(self.report_line.retail_price_withdisc_rub)

    @api.depends('report_line.for_pay')
    def _amount_transfer_supplier(self):
        self.amount_transfer_supplier = sum(self.report_line.for_pay)

    @api.depends('sales_amount', 'amount_transfer_supplier')
    def _amount_commission_wb(self):
        self.amount_commission_wb = self.sales_amount - self.amount_transfer_supplier
        self.total_percentage_WB = (self.sales_amount - self.amount_transfer_supplier) / self.sales_amount

    @api.depends('report_line.delivery_rub')
    def _logistics(self):
        self.logistics = sum(self.report_line.delivery_rub)

    @api.depends('logistics', 'sales_amount')
    def _percentage_logistic(self):
        self.percentage_logistic = self.logistics / self.sales_amount

    @api.depends('warehouse_storage', 'sales_amount')
    def _percentage_storage(self):
        self.percentage_storage = self.warehouse_storage / self.sales_amount

    @api.depends('report_line.wholesale_price')
    def _sum_wholesale_prices(self):
        self.sum_wholesale_prices = sum(self.report_line.wholesale_price)

    @api.depends('sum_wholesale_prices', 'sales_amount')
    def _percentage_purchases(self):
        self.percentage_purchases = self.sum_wholesale_prices / self.sales_amount

    @api.depends('amount_transfer_supplier', 'sum_wholesale_prices')
    def _amount_net_income(self):
        self.amount_net_income = self.amount_transfer_supplier - self.sum_wholesale_prices

    @api.depends('amount_net_income', 'sales_amount')
    def _percentage_net_income(self):
        self.percentage_net_income = self.amount_net_income / self.sales_amount

    @api.depends('report_line.quantity')
    def _total_number_sales(self):
        self.total_number_sales = sum(self.report_line.quantity)

    @api.depends('sum_wholesale_prices', 'total_number_sales')
    def _average_wholesale_price(self):
        self.average_wholesale_price = self.sum_wholesale_prices / self.total_number_sales

    @api.depends('total_number_sales', 'sales_amount')
    def _average_selling_price(self):
        self.average_selling_price = self.sales_amount / self.total_number_sales

    def _prepare_report(self, partner_id, agreement_id, date_from, date_to):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        report_vals = {
            'partner_id': partner_id.id,
            'start_date': date_from,
            'end_date': date_to,
            'agreement_id': agreement_id.id or False,
            'report_line': [],
        }
        return report_vals

    def _collecting_data_for_report(self, date_from, date_to):
        # commission_line = self.env('wb.report.detail').search([])
        # for i in commission_line:
        #     r = i.rr_dt
        # date_from_111 = str(date_from)
        commission_line = self.env['wb.report.detail'].search([("rr_dt", ">=", str(date_from)), ("rr_dt", "<=", str(date_to))])
        return commission_line

    def create_report(self, partner_id, agreement_id, date_from, date_to):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        # 1) Create agent report.
        report_vals_list = []
        # Report values.
        report_vals = self._prepare_report(partner_id, agreement_id, date_from, date_to)

        # Invoice line values (keep only necessary sections).
        report_line = self._collecting_data_for_report(date_from, date_to)
        for line in report_line:
            product_id = self.env['product.product'].search([("barcode", "=", line.barcode)])
            print(product_id)
            res = {
                'product_id': product_id.id,
                'realizationreport_id': line.realizationreport_id,
                'suppliercontract_code': line.suppliercontract_code,
                'rr_dt': line.rr_dt,
                'rr_dt_and_time': line.rr_dt,
                'rrd_id': line.rrd_id,
                'gi_id': line.gi_id,
                'subject_name': line.subject_name,
                'nm_id': line.nm_id,
                'brand_name': line.brand_name,
                'sa_name': line.sa_name,
                'ts_name': line.ts_name,
                'barcode': line.barcode,
                'doc_type_name': line.doc_type_name,
                'quantity': line.quantity,
                'nds': line.nds,
                'cost_amount': line.cost_amount,
                'retail_price': line.retail_price,
                'retail_amount': line.retail_amount,
                'retail_commission': line.retail_commission,
                'sale_percent': line.sale_percent,
                'commission_percent': line.commission_percent,
                'customer_reward': line.customer_reward,
                'supplier_reward': line.supplier_reward,
                'office_name': line.office_name,
                'supplier_oper_name': line.supplier_oper_name,
                'order_dt': line.order_dt,
                'sale_dt': line.sale_dt,
                'shk_id': line.shk_id,
                'retail_price_withdisc_rub': line.retail_price_withdisc_rub,
                'for_pay': line.for_pay,
                'for_pay_nds': line.for_pay_nds,
                'delivery_amount': line.delivery_amount,
                'return_amount': line.return_amount,
                'delivery_rub': line.delivery_rub,
                'gi_box_type_name': line.gi_box_type_name,
                'product_discount_for_report': line.product_discount_for_report,
                'supplier_promo': line.supplier_promo,
                'supplier_spp': line.supplier_spp,
            }
            report_vals['report_line'].append((0, 0, res))

        report_vals_list.append(report_vals)

        if not report_vals_list:
            raise UserError(_(
                'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

        # 3) Create report.
        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        self.sudo().create(report_vals_list)


class WBDetailSalesReportLine(models.Model):
    _name = "wb.detail.sales.report.line"
    _description = "Detailed sales reports line"


    product_id = fields.Many2one(
        'product.product', string='Product')  # Unrequired company
    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id")

    report_id = fields.Many2one('wb.detail.sales.report', string='Link to the report', required=True, ondelete='cascade', index=True, copy=False)

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
    
    standard_price = fields.Float(
        'Wholesale price', compute='_compute_standard_price',
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
        In FIFO: value of the last unit that left the stock (automatically computed).
        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
        Used to compute margins on sale orders.""")
    net_profit = fields.Float('Net profit', store=True, readonly=True, compute='_net_profit')


    def _compute_standard_price(self):
        for line in self:
            if line.barcode == False:
                line.standard_price = 0
                continue
            product_id = line.env['product.product'].search([('barcode', '=', line.barcode)], limit=None).id
            products = line.env['ir.property'].search([('res_id', '=', 'product.product,%s' % product_id)], limit=None)
            line.standard_price = products.value_float
    
    @api.depends('for_pay', 'standard_price')
    def _net_profit(self):
        self.net_profit = self.for_pay - self.standard_price

    