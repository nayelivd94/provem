## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, date, time,timedelta
import logging
from . import amount_to_text
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit ='hr.employee'

    @api.one
    def _compute_days(self):
        if str(self.birthday) != 'False':
            # _logger.info(_("entrooooooooooo  \n\n \n%s") % (str(self.validity_date)))
            fecha = str(self.birthday) + ' 00:00:00'
            cumple = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').date()
            _logger.info(_("cumple: \n\n \n%s") % (cumple))
            i = datetime.now()
            hoy = (str(i.year) + '-' + str(i.month, ) + '-' + str(i.day) + ' 00:00:00')
            fecha_hoy = datetime.strptime(hoy, '%Y-%m-%d %H:%M:%S').date()
            _logger.info(_("fecha hoy: \n\n \n%s") % (fecha_hoy))
            total = fecha_hoy - cumple
            years = str(int(total.days / 365))
            _logger.info(_("Edad: \n\n \n%s") % (years))
            self.edad = years
    edad= fields.Integer(string="Edad", compute="_compute_days")
    x_nss= fields.Char(string="No. de Seguro Social")

class hrcontract(models.Model):
    _inherit ='hr.contract'

    @api.one
    @api.depends('wage')
    def _get_amount_to_text(self):
        _logger.info(_("ENNTRO a monto texto "))
        self.amount_to_text = amount_to_text.get_amount_to_text(self, self.wage,'MXN')
    amount_to_text = fields.Char(compute='_get_amount_to_text', string='Monto en Texto', readonly=True,
                                 help='Amount of the invoice in letter', store=True)
    x_localidad = fields.Char("Localidad")
    period_salary = fields.Char("Periodo Salarial")
