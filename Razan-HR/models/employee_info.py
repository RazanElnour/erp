# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime


class DevicesHistoryPDF(models.TransientModel):
    _name = 'employee.info.pdf'

    
    from_date = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)





    def print_report(self):
        data = {}
        res = {}
        if self.from_date and self.date_to:
            line_ids = self.env['hr.employee'].search(
                [('create_date', '>=', self.from_date), ('create_date', '<=', self.date_to)
                 ]).mapped('id')

        data['from_date'] = self.from_date
        data['date_to'] = self.date_to
        return self.env.ref('hr_employee_information.report_employee_pdf_id').report_action([], data=data)
