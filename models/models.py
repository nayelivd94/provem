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
class res_partner(models.Model):
    _inherit = 'res.partner'
    l10n_mx_edi_payment_method_id = fields.Many2one('l10n_mx_edi.payment.method', string='Metodo de Pago')
    l10n_mx_edi_usage = fields.Selection([
            ('G01', 'Acquisition of merchandise'),
            ('G02', 'Returns, discounts or bonuses'),
            ('G03', 'General expenses'),
            ('I01', 'Constructions'),
            ('I02', 'Office furniture and equipment investment'),
            ('I03', 'Transportation equipment'),
            ('I04', 'Computer equipment and accessories'),
            ('I05', 'Dices, dies, molds, matrices and tooling'),
            ('I06', 'Telephone communications'),
            ('I07', 'Satellite communications'),
            ('I08', 'Other machinery and equipment'),
            ('D01', 'Medical, dental and hospital expenses.'),
            ('D02', 'Medical expenses for disability'),
            ('D03', 'Funeral expenses'),
            ('D04', 'Donations'),
            ('D05', 'Real interest effectively paid for mortgage loans (room house)'),
            ('D06', 'Voluntary contributions to SAR'),
            ('D07', 'Medical insurance premiums'),
            ('D08', 'Mandatory School Transportation Expenses'),
            ('D09', 'Deposits in savings accounts, premiums based on pension plans.'),
            ('D10', 'Payments for educational services (Colegiatura)'),
            ('P01', 'To define'),
        ], 'Usage', default='P01',
            help='Used in CFDI 3.3 to express the key to the usage that will '
                 'gives the receiver to this invoice. This value is defined by the '
                 'customer. \nNote: It is not cause for cancellation if the key set is '
                 'not the usage that will give the receiver of the document.')
