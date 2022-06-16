# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api, tools, _
from openerp.exceptions import ValidationError
import xlsxwriter
import base64
import datetime
from io import StringIO, BytesIO
from datetime import *
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import os
import io
# from odoo.exceptions import UserError
from openerp.exceptions import Warning as UserError
from dateutil import relativedelta

class wizard_partner(models.Model):
    _name = 'wizard.partner'
    _description = 'Print all Partners'

    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)
    customer_id = fields.Many2one('res.partner', 'Customer Or Vendor', required=True)

    def print_report(self):
        for report in self:
            # logo = report.env.user.company_id
            from_date = report.from_date
            to_date = report.to_date
            customer_id = report.customer_id
            if report.from_date > report.to_date:
                raise UserError(_("You must be enter start date less than end date !"))
            file_name = _('Partner Statement.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            excel_sheet = workbook.add_worksheet('Partner Statement')
            # image_data = BytesIO(base64.b64decode(logo))  # to convert it to base64 file
            # excel_sheet.insert_image('B1', 'logo.png', {'image_data': image_data})
            header_date = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white'})
            excel_sheet2 = workbook.add_worksheet('الشيكات الاجلة')
            excel_sheet.right_to_left()
            excel_sheet2.right_to_left()
            header_date.set_align('left')
            contain_format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            contain_format.set_align('center')
            contain_format.set_text_wrap()
            contain_format.set_num_format('#,##0.00')
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'white', 'bg_color': '#696969', 'border': 1})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            format = workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white'})
            header_format.set_align('center')
            header_format.set_align('vertical center')
            header_format.set_text_wrap()
            format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1, 'font_size': '10'})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format.set_align('center')
            format.set_align('center')
            header_format_sequence.set_align('center')
            format.set_text_wrap()
            format_details = workbook.add_format()
            sequence_format = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            sequence_format.set_align('center')
            sequence_format.set_text_wrap()
            total_format = workbook.add_format(
                {'bold': True, 'font_color': 'black', 'bg_color': '#808080', 'border': 1, 'font_size': '10'})
            total_format.set_align('center')
            total_format.set_text_wrap()
            format_details.set_num_format('#,##0.00')
            sequence_id = 0
            col = 0
            row = 11
            first_row = 13
            report_title = customer_id.name + ' Partner Statement From '
            excel_sheet.merge_range(10, 2, 10, 7, report_title, title_format)
            excel_sheet.set_column(col, col, 5)
            excel_sheet.write(row, col, '#', header_format)
            col += 1
            excel_sheet.set_column(col, col, 15)
            excel_sheet.write(row, col, 'Date', header_format)
            col += 1
            excel_sheet.set_column(col, col, 15)
            excel_sheet.write(row, col, 'Narration', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'JRNL', header_format)
            col += 1
            excel_sheet.set_column(col, col, 15)
            excel_sheet.write(row, col, 'Account', header_format)
            col += 1
            excel_sheet.set_column(col, col, 15)
            excel_sheet.write(row, col, 'Ref', header_format)
            col += 1
            excel_sheet.set_column(col, col, 20)
            excel_sheet.write(row, col, 'Amount Currency ', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Currency ', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Debit', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Credit', header_format)
            col += 1
            excel_sheet.set_column(col, col, 10)
            excel_sheet.write(row, col, 'Balance', header_format)

            move_ids = self.env['account.move.line'].search([('partner_id', '=', customer_id.id), ('date', '>=', from_date), ('date', '<=', to_date), ('move_id.state', '=', 'posted')], order='date,id asc')
            if move_ids:
                for move in move_ids:
                    partner = move.partner_id
                    account = move.account_id
                    if account.internal_type == 'Receivable' or account.internal_type == 'Payable':
                        date = move.date
                        journal = move.journal_id.code
                        move_id = move.move_id.name
                        narration = move.name
                        debit = move.debit
                        credit = move.credit
                        balance = debit - credit
                        account_code = account.code
                        amount_currency = move.amount_currency
                        currency = move.currency_id.name

                        col = 0
                        row += 1
                        sequence_id += 1
                        excel_sheet.write(row, col, sequence_id, sequence_format)
                        col += 1
                        if date:
                            excel_sheet.write(row, col, str(date), format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if narration:
                            excel_sheet.write(row, col, narration, format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if journal:
                            excel_sheet.write(row, col, journal, format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if account_code:
                            excel_sheet.write(row, col, account_code, format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if move_id:
                            excel_sheet.write(row, col, move_id, format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if amount_currency:
                            excel_sheet.write(row, col, amount_currency, format)
                        else:
                            excel_sheet.write(row, col, '0.0', format)
                        col += 1
                        if currency:
                            excel_sheet.write(row, col, currency, format)
                        else:
                            excel_sheet.write(row, col, '', format)
                        col += 1
                        if debit:
                            excel_sheet.write(row, col, debit, format)
                        else:
                            excel_sheet.write(row, col, '0.0', format)
                        col += 1
                        if credit:
                            excel_sheet.write(row, col, credit, format)
                        else:
                            excel_sheet.write(row, col, '0.0', format)
                        col += 1
                        if balance:
                            excel_sheet.write(row, col, balance, format)
                        else:
                            excel_sheet.write(row, col, '', format)
            col = 0
            row += 1
            excel_sheet.merge_range(row, col, row, col + 5, 'Total', header_format)
            excel_sheet.write_formula(row, col + 6, 'SUM(g' + str(first_row) + ':g' + str(row) + ')', header_format)
            excel_sheet.write(row, col + 7, ' ', header_format)
            excel_sheet.write_formula(row, col + 8, 'SUM(i' + str(first_row) + ':i' + str(row) + ')', header_format)
            excel_sheet.write_formula(row, col + 9, 'SUM(j' + str(first_row) + ':j' + str(row) + ')', header_format)
            excel_sheet.write_formula(row, col + 10, 'SUM(k' + str(first_row) + ':k' + str(row) + ')', header_format)



#######################################################################

           
            workbook.close()
            file_download = base64.b64encode(fp.getvalue())
            fp.close()
            wizardmodel = self.env['partner.report.excel']
            res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
            return {
                'name': 'Files to Download',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'partner.report.excel',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': res_id.id,
            }


class partner_report_excel(models.TransientModel):
    _name = 'partner.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)
