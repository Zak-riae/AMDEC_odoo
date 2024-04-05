from odoo import _, api, fields, models


class AmdecContextType(models.Model):
    _name = "amdec.context.type"
    _description = (
        "Help to understand what type of the context is the failure."
    )
    _order = "sequence, id"

    name = fields.Char()

    active = fields.Boolean(default=True)

    sequence = fields.Integer(default=10)
