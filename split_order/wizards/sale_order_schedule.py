from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrderSchedule(models.TransientModel):
    _name = 'sale.order.schedule'

    order_id = fields.Many2one('sale.order', 'Order')
    delivery_type = fields.Selection([('full', 'Make DO'),
                                      ('split_delivery', 'Split Delivery'),
                                      ('reserve_qty', 'Unscheduled')],
                                     stribng="Delivery Type", default='full')
    schedule_line_ids = fields.One2many("sale.order.schedule.line", "schedule_id")
    contact_name = fields.Char("Contact name")
    address = fields.Char("Address")
    phone = fields.Char("Phone")
    schedule_date = fields.Date("Scheduled Date")

    def done_delivery(self):
        if self.order_id.state != 'sale':
            self.order_id.action_confirm()
            picking = self.order_id.picking_ids.sorted(reverse=True)
            if picking:
                picking[0].write({'x_studio_contact_name': self.contact_name,
                                  'x_studio_contact_phone_1': self.phone,
                                  'scheduled_date2': self.schedule_date})
                if '.' not in picking[0]['name']:
                    picking[0]['name']=picking[0]['name']+'.1'
                for move in picking[0].move_ids_without_package:
                    s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                    move.product_uom_qty = s_line.do_qty
        else:
            picking = self.order_id.picking_ids.sorted(reverse=True)
            if picking:
                picking[0].write({'x_studio_contact_name': self.contact_name,
                                  'x_studio_contact_phone_1': self.phone,
                                  'scheduled_date2': self.schedule_date})
                if '.' not in picking[0]['name']:
                    picking[0]['name']=picking[0]['name']+'.1'
                picking = picking[0].with_context({'name': str(picking[-1].name)[:-2] + '.' + str(len(picking)+1)}).copy()
                for move in picking.move_ids_without_package:
                    s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                    move.product_uom_qty = s_line.do_qty

    def schedule_another(self):
        view = self.env.ref('split_order.sale_order_schedule_form')
        ctx = self.env.context.copy()
        ctx['default_order_id'] = self.order_id.id
        data = lines = self.env['sale.order.schedule.line']
        if self.order_id.state != 'sale':
            self.order_id.action_confirm()
            picking = self.order_id.picking_ids.sorted(reverse=True)
            logging.warning(str(picking))
            if picking:
                picking[0].write({'x_studio_contact_name': self.contact_name,
                                  'x_studio_contact_phone_1': self.phone,
                                  'scheduled_date2': self.schedule_date})
                if '.' not in picking[0]['name']:
                    picking[0]['name']=picking[0]['name']+'.1'
                for move in picking[0].move_ids_without_package:
                    s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                    if len(s_line)>1:
                        raise Warning("Duplicate products are on this order, unable to split deliveries")
                    move.product_uom_qty = s_line.do_qty
            for line in self.order_id.order_line:
                minus_line = self.schedule_line_ids.filtered(lambda r: r.product_id == line.product_id)
                if line.product_uom_qty - minus_line.do_qty > 0:
                    lines |= data.create({'product_id': line.product_id.id,
                                          'product_qty': line.product_uom_qty - minus_line.do_qty,
                                          'order_qty': line.product_uom_qty, })
            ctx['default_schedule_line_ids'] = [(6, 0, lines.ids)]
        else:
            picking = self.order_id.picking_ids.sorted(reverse=True)
            logging.warning(str(picking))
            if picking:
                picking[0].write({'x_studio_contact_name': self.contact_name,
                                  'x_studio_contact_phone_1': self.phone,
                                  'scheduled_date2': self.schedule_date})
                if '.' not in picking[0]['name']:
                    picking[0]['name']=picking[0]['name']+'.1'
                picking = picking[0].with_context({'name': str(picking[-1].name)[:-2] + '.' + str(len(picking)+1)}).copy()
                for move in picking.move_ids_without_package:
                    s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                    move.product_uom_qty = s_line.do_qty
            for line in self.order_id.order_line:
                minus_line = self.schedule_line_ids.filtered(lambda r: r.product_id == line.product_id)
                if line.product_uom_qty - minus_line.do_qty > 0:
                    lines |= data.create({'product_id': line.product_id.id,
                                          'product_qty': minus_line.product_qty - minus_line.do_qty,
                                          'order_qty': line.product_uom_qty, })
            ctx['default_schedule_line_ids'] = [(6, 0, lines.ids)]
            ctx['default_delivery_type'] = 'split_delivery'
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.schedule',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': ctx,
        }

    def make_delivery(self):
        if self.delivery_type == 'full':
            self.order_id.action_confirm()
        else:
            if self.order_id.state != 'sale':
                self.order_id.action_confirm()
                picking = self.order_id.picking_ids.sorted(reverse=True)
                logging.warning(str(picking))
                if picking:
                    picking[0].with_context({'picking_state': 'hold'})._compute_state()
                    for move in picking[0].move_ids_without_package:
                        move.state = 'hold'
                        s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                        move.reserved_availability = s_line.reserved_qty
            else:
                picking = self.order_id.picking_ids.sorted(reverse=True)
                logging.warning(str(picking))
                if picking:
                    picking = picking[0].with_context({'name': str(picking[-1].name)[:-2] + '.' + str(len(picking))}).copy()
                    picking[0].with_context({'picking_state': 'hold'})._compute_state()
                    for move in picking.move_ids_without_package:
                        move.state = 'hold'
                        s_line = self.schedule_line_ids.filtered(lambda r: r.product_id == move.product_id)
                        move.product_uom_qty = s_line.product_qty
                        move.reserved_availability = s_line.reserved_qty


class SaleOrderScheduleLine(models.TransientModel):
    _name = 'sale.order.schedule.line'

    product_id = fields.Many2one("product.product")
    order_qty = fields.Float("Order Quantity")
    product_qty = fields.Float("Remaining Quantity")
    remaining_qty = fields.Float("Remaining Order Qty", compute="_get_remaining_qty")
    do_qty = fields.Float("DO Quantity")
    reserved_qty = fields.Float("Reserve Qty")
    onhand_qty = fields.Float("On hand Qty", related="product_id.qty_available")
    schedule_id = fields.Many2one("sale.order.schedule")

    @api.depends('do_qty', 'product_id', 'product_qty')
    def _get_remaining_qty(self):
        for rec in self:
            rec.remaining_qty = rec.product_qty - rec.do_qty
