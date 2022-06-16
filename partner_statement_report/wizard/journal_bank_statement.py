# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time


class CustomerStatementPDF(models.TransientModel):
    _name = 'journal.bank.statement.pdf'

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date',)
    journal_id = fields.Many2one('account.journal', 'Bank', required=True,domain="[('type', '=', 'bank')]")

    def print_report(self):
        data = {}
        res = {}
        if self.from_date and self.to_date:
            move_line_ids = self.env['account.move.line'].search(
                [('date', '<=', self.to_date), ('date', '>=', self.from_date), ('move_id.state', '=', 'posted'),
                 ('account_id', '=', self.journal_id.default_account_id.id)], order='date,id asc').mapped('id')
            print(move_line_ids,'move_line_ids')

        else:
            move_line_ids = self.env['account.move.line'].search(
                [ ('move_id.state', '=', 'posted'),
                 ('account_id', '=', self.journal_id.default_account_id.id)], order='date,id asc').mapped('id')
        data['from_date'] = self.from_date
        data['to_date'] = self.to_date
        data['journal_id'] = self.journal_id.default_account_id.id
        data['journal_name'] = self.journal_id.name
        return self.env.ref('partner_statement_report.jornal_bank_statement_pdf_report_id').report_action([], data=data)
