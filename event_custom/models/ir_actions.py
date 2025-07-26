# -*- coding: utf-8 -*-

from odoo import fields, models


class IrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report'

    default_print = fields.Boolean()

    def _get_readable_fields(self):
        data = super()._get_readable_fields()
        data.add('default_print')
        return data

    def report_action(self, docids, data=None, config=True):
        data = super(IrActionsReportXml, self).report_action(docids, data, config)
        data['id'] = self.id
        data['default_print'] = self.default_print
        return data
