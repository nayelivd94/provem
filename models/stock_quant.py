## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import logging
import datetime
import time
_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit ='stock.quant'

    @api.one
    @api.depends('standard_price')
    def _compute_standardprice(self):
        self.standard_price = self.product_id.standard_price
    standard_price= fields.Float(string="Costo", compute="_compute_standardprice", store=True)