from odoo import models, fields, api

class EventRegistration(models.Model):
    _inherit = 'event.registration'


    @api.constrains('event_id', 'event_ticket_id')
    def _check_event_ticket(self):

        for rec in self:
            if rec.event_ticket_id and rec.event_ticket_id.event_id != rec.event_id:
                pass

# class CustomEventRegistrationAnswer(models.Model):
#     _inherit = 'event.registration.answer'
#
#     # New fields based on the screenshot
#     sales_order = fields.Char(string="Sales Order")  # e.g., "500103"
#     sales_order_line = fields.Char(string="Sales Order Line")  # e.g., "500103 - Open Return (Ahmed aziz)"
#     campaign = fields.Char(string="Campaign")  # e.g., "Medium?"
#     source = fields.Char(string="Source")  # e.g., "Adult"
#     text_answer = fields.Char(string="Text Answer")  # e.g., "25-1-1990"
#     kind = fields.Selection([('male', 'Male')], string="Kind")  # Example selection
#     luggage = fields.Integer(string="Luggage")  # e.g., "1"
#     nationality = fields.Selection([('egypt', 'Egypt')], string="Nationality")  # Example selection
#     packing = fields.Integer(string="Packing")  # e.g., "1"
#     pass_expiry_date = fields.Char(string="Pass Expiry Date")  # e.g., "10-5-2030" (could also be Date field)
#     pass_issue_date = fields.Char(string="Pass Issue Date")  # e.g., "10-5-2020" (could also be Date field)
#     passport_sn = fields.Char(string="Passport S/N")