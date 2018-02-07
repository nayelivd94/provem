# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockQuantFilter(models.TransientModel):
    _name = 'stock.quant.filter'
    _description = 'Valoración de Inventario con Filtros'

    compute_at_date = fields.Selection([
        (0, 'Mostrar todo el inventario'),
        (1, 'Filtrar por fecha')
    ], string="Compute", help="Muestra con filtros el inventario")
    date = fields.Datetime('Inventory at Date', help="Choose a date to get the inventory at that date")

    def open_table(self):
        self.ensure_one()

        if self.compute_at_date:
            tree_view_id = self.env.ref('stock.view_stock_quant_tree').id
            form_view_id = self.env.ref('stock.view_stock_quant_form').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': _('Valoracion de inventario v10'),
                'res_model': 'stock.quant',
                #"'context': dict(self.env.context, to_date=self.date),
                'context':{'search_default_internal_loc': 1, 'search_default_locationgroup':1},
                'domain':  [('create_date', '>=',  self.date)],
            }
            return action
        else:
            self.env['stock.quant']._merge_quants()
            return self.env.ref('stock.quantsact').read()[0]
