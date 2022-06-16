# -*- coding: utf-8 -*-

from odoo import models, fields, api,_, SUPERUSER_ID
from odoo.exceptions import Warning, ValidationError,UserError
from datetime import timedelta,date,datetime
from odoo import tools


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    def send_birthday_mail(self):
        local_context = self.env.context.copy()
        self.env.cr.execute("""select id from hr_employee
                                WHERE 
                                    active = True
                                AND
                                    DATE_PART('day', birthday) = date_part('day', %s::date)
                                AND
                                    DATE_PART('month', birthday) = date_part('month', %s::date);""", 
                                    (datetime.now().date(),datetime.now().date()))
        birth_emps  = self.env.cr.dictfetchall()
        if birth_emps:
            for emp in birth_emps:
                template = self.env.ref('hrms_birthday.birthday_mail_template1')
                template.with_context(local_context).send_mail(emp['id'], force_send=True)
            
            
            
            