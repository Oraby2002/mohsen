# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    def action_make_registration(self):
        res = super(RegistrationEditor, self).action_make_registration()
        action = self.env["ir.actions.actions"]._for_xml_id("event.event_registration_action_tree")
        action['domain'] = [('sale_order_id', 'in', self.sale_order_id.ids)]
        return action
