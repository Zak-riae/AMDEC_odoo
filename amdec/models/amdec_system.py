from odoo import _, api, fields, models


class AmdecSystem(models.Model):
    _name = "amdec.system"
    _description = "amdec_system"

    name = fields.Char()

    composante_ids = fields.One2many(
        comodel_name="amdec.composante",
        inverse_name="system_id",
        string="Composantes",
    )
