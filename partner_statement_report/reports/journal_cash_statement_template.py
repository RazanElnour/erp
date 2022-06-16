
# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools import float_round
from odoo.exceptions import UserError, Warning
from datetime import datetime,date


class CustomerStatementReport(models.AbstractModel):
    _name = 'report.partner_statement_report.cash_statement_pdf_report'

    def _get_header_info(self, data):
        date_from = data['from_date']
        date_to = data['to_date']
        journal_id = data['journal_id']
        journal_name = data['journal_name']
        return {
            'start_date': date_from,
            'end_date': date_to,
            'journal_id': journal_id,
            'journal_name': journal_name,
            'today': date.today(),
        }

    def _get_cash_statement(self, data):
        res = []
        if data['from_date'] and data['to_date']:
            move_line_ids = self.env['account.move.line'].search(
                [('date', '<=', data['to_date']), ('date', '>=', data['from_date']),
                 ('move_id.state', '=', 'posted'),
                 ('account_id', '=', data['journal_id']),
                 ], order='date,id asc').mapped('id')


        else:
            move_line_ids = self.env['account.move.line'].search(
                [
                 ('move_id.state', '=', 'posted'),
                    ('account_id', '=', data['journal_id'])], order='date,id asc').mapped('id')
        records = self.env['account.move.line'].browse(move_line_ids)
        if move_line_ids:
            debit = 0
            credit = 0
            for move in records:
                    debit = move.debit
                    credit = move.credit
                    name = move.name
                    ref = move.ref
                    date = move.date
                    res.append({'debit': debit, 'credit': credit, 'balance': debit - credit,'name': name,'ref': ref,'date': date})

        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        data['records'] = self.env['account.move.line'].browse(data)
        docs = data['records']
        sales_details_report = self.env['ir.actions.report']._get_report_from_name('partner_statement_report.cash_statement_pdf_report')
        docargs = {

            'data': data,
            'docs': docs,
        }
        return {
            'doc_ids': self.ids,
            'doc_model': sales_details_report.model,
            'docs': data,
            'get_header_info': self._get_header_info(data),
            'get_cash_statement': self._get_cash_statement(data),
        }
