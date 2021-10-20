from odoo import models, api, _, fields
from odoo.exceptions import UserError


class PurchaseOrderline(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[('approved', 'Approved'), ('pending', 'Wait To Approve')])
    price_bool = fields.Boolean()

    @api.onchange('order_line', 'price_unit')
    def price_unit_change(self):
        flag1 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_product_price_change')
        flag2 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_service_price_change')
        for journal in self.order_line:
            product_type = journal.product_id.type
            if flag1:
                if product_type in ['consu', 'product']:
                    print("...")
                else:
                    journal.price_limit = True
                    self.price_bool = True
            if flag2:
                print("kkkkk")
                if product_type in ['service']:
                    print("...")
                else:
                    journal.price_limit = True
                    self.price_bool = True

    def action_req_approval(self):
        self.state = "pending"

    def hello(self):
        print("lllllllll")


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order.line"

    price_limit = fields.Boolean('Price Limit')
