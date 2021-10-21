from odoo import models, api, _, fields


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    price_bool = fields.Boolean()
    # state = fields.Selection(selection_add=[('approved', 'Approved'), ('pending', 'Approval pending')],
    #                          ondelete={'draft': 'set default'})

    @api.onchange('invoice_line_ids', 'price_unit')
    def price_unit_change(self):
        flag1 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_product_price_change')
        flag2 = self.env['res.users'].has_group('restrict_price_change.groups_restrict_service_price_change')
        for invoice in self.invoice_line_ids:
            product_type = invoice.product_id.type
            product_price = invoice.price_unit
            price = invoice.product_id.standard_price
            if flag1:
                if product_type not in ['consu', 'product'] and (product_price != price):
                    # invoice.price_limit = True
                    self.price_bool = True

            if flag2:
                if product_type not in ['service'] and (product_price != price):
                    # invoice.price_limit = True
                    self.price_bool = True

    def action_req_approval(self):
        self.state = "pending"

    def action_approval(self):
        self.state = "draft"
        self.price_bool = False
        for orders in self.order_line:
            orders.price_limit = False


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    price_limit = fields.Boolean('Price Limit')
