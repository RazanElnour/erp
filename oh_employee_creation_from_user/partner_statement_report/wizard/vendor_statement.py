# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time


class CustomerStatementPDF(models.TransientModel):
    _name = 'vendor.statement.pdf'

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date',)
    partner_id = fields.Many2one('res.partner', 'Vendor', required=True )

    def print_report(self):
        data = {}
        res = {}
        if self.from_date and self.to_date:
            move_line_ids = self.env['account.move.line'].search(
                [('date', '<=', self.to_date), ('date', '>=', self.from_date), ('move_id.state', '=', 'posted'),
                 ('partner_id', '=', self.partner_id.id)], order='date,id asc').mapped('id')
            print(move_line_ids,'move_line_ids')
        else:
            move_line_ids = self.env['account.move.line'].search(
                [ ('move_id.state', '=', 'posted'),
                 ('partner_id', '=', self.partner_id.id)], order='date,id asc').mapped('id')
            print(move_line_ids,'move_line_ids')

        data['from_date'] = self.from_date
        data['to_date'] = self.to_date
        data['partner_id'] = self.partner_id.name
        return self.env.ref('partner_statement_report.vendor_statement_pdf_report_id').report_action([], data=data)
