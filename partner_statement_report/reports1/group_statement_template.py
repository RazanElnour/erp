
# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools import float_round
from odoo.exceptions import UserError, Warning
from datetime import datetime


class CustomerStatementReport(models.AbstractModel):
    _name = 'report.is_penotee_accounting.group_statement_pdf_report_id'

    def _get_header_info(self, data):
        date_from = data['from_date']
        date_to = data['to_date']
        account = data['account_id']
        return {
            'start_date': date_from,
            'end_date': date_to,
            'account_id': account,
            'today': datetime.now().date(),
        }

    def _get_customer(self, data):
        res = []
        Account=[]
        group_ids = self.env['account.account'].search(
            [('group_id', '=',  data['account_id'])])
        if group_ids:
            for acc in group_ids:
               account = acc.id
               print(account,'aa')
               code = acc.code
               print(code,'cc')

               if data['from_date'] and data['to_date']:

                     move_line_ids = self.env['account.move.line'].search(
                           [('date', '<=', data['to_date']), ('date', '>=', data['from_date']),
                           ('move_id.state', '=', 'posted'),
                           ('account_id', '=', account)], order='date,id asc').mapped('id')
                     print(move_line_ids,'reportvhb')

                     records = self.env['account.move.line'].browse(move_line_ids)
                     print(records,'kol')
                     if move_line_ids:
                         debit = 0.0
                         credit = 0.0
                         for move in records:
                              account = move.account_id.name
                              debit += move.debit
                              credit += move.credit
                         res.append({'debit': debit, 'credit': credit, 'balance': debit - credit, 'account': account,'code': code})

        return res


    @api.model
    def _get_report_values(self, docids, data=None):
        data['records'] = self.env['account.move.line'].browse(data)
        docs = data['records']
        sales_details_report = self.env['ir.actions.report']._get_report_from_name('is_penotee_accounting.group_statement_pdf_report_id')
        docargs = {

            'data': data,
            'docs': docs,
        }
        return {
            'doc_ids': self.ids,
            'doc_model': sales_details_report.model,
            'docs': data,
            # 'get_data_from_report': self._get_data_from_report,
            'get_header_info': self._get_header_info(data),
            'get_customer': self._get_customer(data),
        }
