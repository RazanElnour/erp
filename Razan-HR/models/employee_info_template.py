
# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools import float_round
from odoo.exceptions import UserError, Warning
from datetime import datetime, timedelta


class EmployeeHistoryReport(models.AbstractModel):
    _name = 'report.hr_employee_information.info_pdf_report'

    def _get_header_info(self, data):
        date_from = data['from_date']
        date_to = data['date_to']
        res = []
        res.append(
            {'date_to': date_to, 'date_from': date_from})
        return res



    def _get_data_from_report(self, data):
        active_ids = self._context.get('active_ids')
        pdf = self.env['employee.info.pdf'].browse(active_ids)
        for rec in pdf:
            date_from = rec.from_date
            date_to = rec.date_to

        res = []
        days = 0.0
        obj = self.env['hr.employee'].search([('id_expiry_date', '>=', date_from),('id_expiry_date', '<=', date_to)])
        history = ''
        for object in obj:
            empolyee_name = object.name
            identification_id = object.identification_id
            id_expiry_date = object.id_expiry_date
            res.append({
                        'empolyee_name': empolyee_name,
                        'identification_id': identification_id,
                        'id_expiry_date': id_expiry_date,

            })
        return res

    def _get_data_passport_from_report(self, data):
        active_ids = self._context.get('active_ids')
        pdf = self.env['employee.info.pdf'].browse(active_ids)
        for rec in pdf:
            date_from = rec.from_date
            date_to = rec.date_to

        res = []
        days = 0.0
        obj = self.env['hr.employee'].search(
            [('passport_expiry_date', '>=', date_from), ('passport_expiry_date', '<=', date_to)])
        history = ''
        for object in obj:
            empolyee_name = object.name
            passport_id = object.passport_id
            passport_expiry_date = object.passport_expiry_date
            res.append({
                'empolyee_name': empolyee_name,
                'passport_id': passport_id,
                'passport_expiry_date': passport_expiry_date
            })
        return res



    @api.model
    def _get_report_values(self, docids, data=None):
        data['records'] = self.env['hr.employee'].browse(data)
        docs = data['records']
        sales_details_report = self.env['ir.actions.report']._get_report_from_name('hr_employee_information.info_pdf_report')
        docargs = {

            'data': data,
            'docs': docs,
        }
        return {
            'doc_ids': self.ids,
            'doc_model': sales_details_report.model,
            'docs': data,
            'get_data_passport_from_report': self._get_data_passport_from_report(data),
            'get_data_from_report': self._get_data_from_report(data),
            'get_header_info': self._get_header_info(data),


        }
