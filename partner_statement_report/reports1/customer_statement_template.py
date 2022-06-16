
# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools import float_round
from odoo.exceptions import UserError, Warning
from datetime import datetime


class CustomerStatementReport(models.AbstractModel):
    _name = 'report.is_penotee_accounting.customer_statement_pdf_report'

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
        customer_ids = self.env['res.partner'].search(
            [('customer', '=', True),
             ('property_account_receivable_id', '=', data['account_id'])])
        # # print (customers_ids)
        if customer_ids:
            for customer_id in customer_ids:
                customer = customer_id
                if data['from_date'] and data['to_date']:
                    move_line_ids = self.env['account.move.line'].search(
                        [('date', '<=', data['to_date']), ('date', '>=', data['from_date']),
                         ('move_id.state', '=', 'posted'),
                         ('account_id.internal_type', '=', 'receivable'),
                         ('partner_id', '=', customer.id)], order='date,id asc').mapped('id')
                    # , ('account_id.internal_type', '=', 'receivable')
                    records = self.env['account.move.line'].browse(move_line_ids)
                    if move_line_ids:
                        debit = 0
                        credit = 0
                        for move in records:
                            if data['currency'] == False:
                                debit += move.debit
                                credit += move.credit
                            elif data['currency'] == True:
                                if move.amount_currency > 0:
                                    debit += abs(move.amount_currency)
                                    credit += 0
                                elif move.amount_currency < 0:
                                    debit += 0
                                    credit += abs(move.amount_currency)
                        res.append({'debit': debit, 'credit': credit, 'balance': debit - credit, 'customer_name': customer.name})

        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        data['records'] = self.env['account.move.line'].browse(data)
        docs = data['records']
        sales_details_report = self.env['ir.actions.report']._get_report_from_name('is_penotee_accounting.customer_statement_pdf_report')
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
