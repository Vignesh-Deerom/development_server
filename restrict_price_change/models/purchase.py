from odoo import models, api, _, fields
from odoo.exceptions import UserError


class PurchaseOrderline(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[('approved', 'Approved'), ('pending', 'Approval pending')])
    price_bool = fields.Boolean()

    @api.onchange('order_line', 'price_unit')
    def price_unit_change(self):
        flag1 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_product_price_change')
        flag2 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_service_price_change')
        for order in self.order_line:
            product_type = order.product_id.type
            product_price = order.price_unit
            price = order.product_id.standard_price
            if flag1:
                if product_type not in ['consu', 'product'] and (product_price != price):
                    # order.price_limit = True
                    self.price_bool = True
            if flag2:
                if product_type not in ['service'] and (product_price != price):
                    # order.price_limit = True
                    self.price_bool = True

    def action_req_approval(self):
        self.state = "pending"

    def action_approval(self):
        self.state = "draft"
        self.price_bool = False
        for orders in self.order_line:
            orders.price_limit = False


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order.line"

    price_limit = fields.Boolean('Price Limit')
