import base64
from itertools import groupby
import re
import logging
from datetime import datetime
from io import BytesIO

from lxml import etree
from lxml.objectify import fromstring
from suds.client import Client

from odoo import _, api, fields, models, tools
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT
from odoo.exceptions import UserError
import logging
from . import amount_to_text
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit ='account.invoice'
    l10n_mx_edi_cfdi_name = fields.Char(string='Nombre CFDIs',
                                        help='The attachment name of the CFDI.')
    name_xml = fields.Char(string='Nombre XML', help='The attachment name of the CFDI.')

    @api.onchange('name_xml')
    def onchange_qtydone(self):
        self.l10n_mx_edi_cfdi_name = self.name_xml

    @api.multi
    @api.depends('l10n_mx_edi_cfdi_name')
    def _compute_cfdi_values(self):
        '''Fill the invoice fields from the cfdi values.
        '''
        for inv in self:
            attachment_id = inv.l10n_mx_edi_retrieve_last_attachment()
            fal = False
            if not attachment_id:
                continue
            if inv.l10n_mx_edi_cfdi_name is False:
                inv.write({'l10n_mx_edi_cfdi_name': inv.name_xml})
            # At this moment, the attachment contains the file size in its 'datas' field because
            # to save some memory, the attachment will store its data on the physical disk.
            # To avoid this problem, we read the 'datas' directly on the disk.
            datas = attachment_id._file_read(attachment_id.store_fname)
            inv.l10n_mx_edi_cfdi = datas
            tree = inv.l10n_mx_edi_get_xml_etree(base64.decodestring(datas))
            # if already signed, extract uuid
            tfd_node = inv.l10n_mx_edi_get_tfd_etree(tree)
            if tfd_node is not None:
                inv.l10n_mx_edi_cfdi_uuid = tfd_node.get('UUID')
            inv.l10n_mx_edi_cfdi_amount = tree.get('total')
            inv.l10n_mx_edi_cfdi_supplier_rfc = tree.Emisor.get('rfc')
            inv.l10n_mx_edi_cfdi_customer_rfc = tree.Receptor.get('rfc')
            certificate = tree.get('noCertificado', tree.get('NoCertificado'))
            inv.l10n_mx_edi_cfdi_certificate_id = inv.env['l10n_mx_edi.certificate'].sudo().search(
                [('serial_number', '=', certificate)], limit=1)
