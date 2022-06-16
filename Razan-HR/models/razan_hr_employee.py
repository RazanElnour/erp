
# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime



class RazanHrEmployee(models.Model):
    _inherit = 'hr.employee'
    english_name=fields.Char(string="English", related='resource_id.name', store=True, readonly=False, tracking=True)
    attachmentT_ids= fields.Many2many('ir.attachment', string="Attachment", required=True)
    employee_no=fields.Char()
    tt=fields.Selection([('moa','مواطن'),('mog','مقيم')] ,string="المواطنة")
    certificate1=fields.Selection([('no','غير متعلم'),('sec','ثانوي'),('dip','دبلوم'),('master','بكالريوس'),('phd','دكتوراه')] ,string="الدرجة العلمية")
    #user_idd=fields.Many2one('res.users', 'User', related='resource_id.user_id', store=True, readonly=False ,string="مستخدم مرتبط بمدير ")
    maritall = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')  ], string='Marital Status', default='single',)
    childrenn=fields.Integer(string='Children', tracking=True)


# class RazanHrrEmployee(models.Model):
#     _inherit = 'resource.calendar'
 
#     day_period = fields.Selection([('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening' ) ] , required=True, default='morning')
#     @api.model
#     def default_get(self, fields):
#         res = super(ResourceCalendar, self).default_get(fields)
#         if not res.get('name') and res.get('company_id'):
#             res['name'] = _('Working Hours of %s', self.env['res.company'].browse(res['company_id']).name)
#         if 'attendance_ids' in fields and not res.get('attendance_ids'):
#             company_id = res.get('company_id', self.env.company.id)
#             company = self.env['res.company'].browse(company_id)
#             company_attendance_ids = company.resource_calendar_id.attendance_ids
#             if company_attendance_ids:
#                 res['attendance_ids'] = [
#                     (0, 0, {
#                         'name': attendance.name,
#                         'dayofweek': attendance.dayofweek,
#                         'hour_from': attendance.hour_from,
#                         'hour_to': attendance.hour_to,
#                         'day_period': attendance.day_period,
#                     })
#                     for attendance in company_attendance_ids
#                 ]
#             else:
#                 res['attendance_ids'] = [
#                     (0, 0, {'name': _('Monday Morning'), 'dayofweek': '0', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
#                     (0, 0, {'name': _('Monday Afternoon'), 'dayofweek': '0', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
#                     (0, 0, {'name': _('Monday Evening'), 'dayofweek': '0', 'hour_from': 17, 'hour_to': 00, 'day_period': 'evening'}),

#                     (0, 0, {'name': _('Tuesday Morning'), 'dayofweek': '1', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
#                     (0, 0, {'name': _('Tuesday Afternoon'), 'dayofweek': '1', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
#                     (0, 0, {'name': _('Tuesday Evening'), 'dayofweek': '1', 'hour_from': 17, 'hour_to': 00, 'day_period': 'evening'}),


#                     (0, 0, {'name': _('Wednesday Morning'), 'dayofweek': '2', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
#                     (0, 0, {'name': _('Wednesday Afternoon'), 'dayofweek': '2', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
#                     (0, 0, {'name': _('Wednesday Evening'), 'dayofweek': '2', 'hour_from': 17, 'hour_to': 00, 'day_period': 'evening'}),

#                     (0, 0, {'name': _('Thursday Morning'), 'dayofweek': '3', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
#                     (0, 0, {'name': _('Thursday Afternoon'), 'dayofweek': '3', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
#                     (0, 0, {'name': _('Thursday Evening'), 'dayofweek': '3', 'hour_from': 17, 'hour_to': 00, 'day_period': 'evening'}),

#                     (0, 0, {'name': _('Friday Morning'), 'dayofweek': '4', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
#                     (0, 0, {'name': _('Friday Afternoon'), 'dayofweek': '4', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'})
#                 ]   (0, 0, {'name': _('Friday Evening'), 'dayofweek': '4', 'hour_from': 17, 'hour_to': 00, 'day_period': 'evening'}),
#         return res
#     