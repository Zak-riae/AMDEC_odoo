from odoo import _, api, fields, models


class AmdecDefaillance(models.Model):
    _name = "amdec.defaillance"
    _description = "amdec_defaillance"

    name = fields.Char()

    cause = fields.Text()

    effet = fields.Text()

    action_entreprendre = fields.Text()
