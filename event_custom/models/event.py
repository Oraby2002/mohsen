# -*- coding: utf-8 -*-

import os
from odoo import _, api, Command, fields, models, tools
from odoo.tools.misc import formatLang
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import UserError


class EventEvent(models.Model):
    _inherit = 'event.event'

    from_location_id = fields.Many2one("event.track.location", "From Location")
    to_location_id = fields.Many2one("event.track.location", "To Location")
    sequence = fields.Char(string="Event Sequence", copy=True)

    @api.model
    def create(self, vals):
        if not vals.get("sequence"):
            vals["sequence"] = self.env["ir.sequence"].next_by_code("event.event") or "/"
        return super(EventEvent, self).create(vals)

    def write(self, vals):
        # منع تغيير sequence تلقائيًا عند تغيير الـ state
        if "sequence" in vals and not self.env.context.get("manual_sequence_edit"):
            for rec in self:
                next_seq = self.env["ir.sequence"].next_by_code("event.event") or "/"
                if vals["sequence"] == next_seq and rec.sequence and vals["sequence"] != rec.sequence:
                    vals.pop("sequence")
                    break
        return super(EventEvent, self).write(vals)

    @api.depends('event_registrations_sold_out', 'seats_limited', 'seats_max', 'seats_available')
    @api.depends_context('name_with_seats_availability')
    def _compute_display_name(self):
        """Adds ticket seats availability if requested by context."""
        if not self.env.context.get('name_with_seats_availability'):
            return super()._compute_display_name()
        for event in self:
            # event or its tickets are sold out
            if event.event_registrations_sold_out:
                name = _('%(event_name)s (Sold out)', event_name=event.name)
            elif event.seats_limited and event.seats_max:
                name = _(
                    '%(event_name)s (%(count)s seats remaining) %(date_begin)s To %(date_end)s',
                    event_name=event.name,
                    count=formatLang(self.env, event.seats_available, digits=0),
                    date_begin=event.date_begin.strftime(DF),
                    date_end=event.date_end.strftime(DF),
                )
            else:
                name = event.name
            event.display_name = name


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    no_of_luggage = fields.Integer()
    luggage_weight = fields.Float()

    @api.model
    def _get_random_barcode(self):
        """Generate a string representation of a pseudo-random 8-byte number for barcode
        generation.

        A decimal serialisation is longer than a hexadecimal one *but* it
        generates a more compact barcode (Code128C rather than Code128A).

        Generate 8 bytes (64 bits) barcodes as 16 bytes barcodes are not
        compatible with all scanners.
         """
        return str(int.from_bytes(os.urandom(3), 'little'))

    def default_get(self, fields):
        ret_vals = super().default_get(fields)
        if ret_vals.get("event_id"):
            event = self.env['event.event'].browse(ret_vals.get("event_id"))
            answers = []
            for question in event.question_ids:
                answers.append((0, 0, {
                    'question_id': question.id,
                }))
            ret_vals['registration_answer_ids'] = answers
        return ret_vals

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("sale_order_line_id"):
                event = self.env['sale.order.line'].browse(values.get("sale_order_line_id")).event_id
                answers = []
                for question in event.question_ids:
                    answers.append((0, 0, {
                        'question_id': question.id,
                        'value_text_box': ' ',
                    }))
                values['registration_answer_ids'] = answers
        registrations = super(EventRegistration, self).create(vals_list)
        return registrations

    def action_clone_data(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return

        all_records = self.env['event.registration'].browse(active_ids)

        sale_order_ids = all_records.mapped("sale_order_id.id")

        if len(sale_order_ids) > 1:
            raise UserError("Selected records must belong to the same Sale Order.")

        if any(record.state == 'cancel' for record in all_records):
            raise UserError("Cannot clone data for records in 'cancel' state.")

        source_record = all_records.filtered(lambda rec: any(
            (ans.value_text_box and ans.value_text_box.strip()) or ans.value_answer_id
            for ans in rec.registration_answer_ids
        ))[:1]

        if not source_record:
            raise UserError("No valid source record found for cloning.")

        source_record = source_record[0]
        target_records = all_records - source_record

        if not target_records:
            raise UserError("No target records available for cloning.")

        new_answers = [
            (0, 0, {
                'question_id': ans.question_id.id,
                'question_type': ans.question_type,
                'value_text_box': ans.value_text_box,
                'value_answer_id': ans.value_answer_id.id if ans.value_answer_id else False,
            })
            for ans in source_record.registration_answer_ids
        ]

        for target in target_records:
            target.write({'registration_answer_ids': [(5, 0, 0)] + new_answers})
