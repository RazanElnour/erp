# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import AccessError, UserError, AccessDenied

class ResCompany(models.Model):
    _inherit = "res.company"

    transfer_account_id = fields.Many2one('account.account',
        domain=lambda self: [('reconcile', '=', True), ('user_type_id.id', '=', self.env.ref('account.data_account_type_current_assets').id), ('deprecated', '=', False)], string="Inter-Banks Transfer Account", help="Intermediary account used when moving money from a liquidity account to another")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    transfer_account_id = fields.Many2one('account.account', string="Transfer Account", readonly=False,related='company_id.transfer_account_id',
                                          domain=lambda self: [('reconcile', '=', True), ('user_type_id.id', '=',
                                                             self.env.ref('account.data_account_type_current_assets').id)],
                                          help="Intermediary account used when moving money from a liquidity account to another")


class payment(models.Model):
    _inherit = 'account.payment'

    to_journal = fields.Many2one('account.journal', 'Destination Journal')
    internal_payment_id = fields.Many2one('account.payment','Internal Payment',readonly=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer/Vendor",
        store=True, readonly=False, ondelete='restrict',
        compute='_compute_partner_id',
        domain="['|', ('parent_id','=', False), ('is_company','=', True)]",
        check_company=True,default=lambda self: self.env.company.partner_id.id)

    def action_post(self):
        res = super(payment, self)
        res.action_post()
        self.check_reconcil_transfer()
        return res

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super(payment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        res[0].update({'account_id': self.journal_id.default_account_id.id})
        return res

    def check_reconcil_transfer(self):
        for rec in self:
            if rec.is_internal_transfer and (not self.to_journal or not self.amount):
                raise UserError(_("PLease Add Destination Journal or Payment Amount"))
            if rec.is_internal_transfer and rec.payment_type == 'outbound':
                payment_obj = self.env['account.payment']
                internal_payment=None
                if  not rec.internal_payment_id:
                    internal_payment = payment_obj.create(
                        {
                            'payment_type':'inbound',
                            'is_internal_transfer':True,
                            'amount':rec.amount,
                            'journal_id':rec.to_journal.id,
                            'payment_method_id':rec.payment_method_id.id,
                            'to_journal':rec.to_journal.id,
                            'company_id': rec.company_id.id,
                            'currency_id':rec.currency_id.id,
                            'date': rec.date,

                        })
                    internal_payment.action_post()
                elif not rec.internal_payment_id:
                    internal_payment = payment_obj.create(
                        {
                            'payment_type': 'inbound',
                            'is_internal_transfer': True,
                            'amount': rec.amount,
                            'journal_id': rec.to_journal.id,
                            'to_journal': rec.to_journal.id,
                            'payment_method_id': rec.payment_method_id.id,
                            'company_id': rec.company_id.id,
                            'currency_id': rec.currency_id.id,
                            'date': rec.date,

                        })
                    internal_payment.action_post()
                if internal_payment:
                    rec.internal_payment_id = internal_payment.id

                    amls = internal_payment.move_id.line_ids + rec.move_id.line_ids
                    amls.filtered(lambda line: not line.reconciled and line.account_id.id == rec.destination_account_id.id).reconcile()
            else:
                return





