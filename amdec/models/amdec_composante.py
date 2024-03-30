from odoo import _, api, fields, models


class AmdecComposante(models.Model):
    _name = "amdec.composante"
    _description = "amdec_composante"

    name = fields.Char()

    system_id = fields.Many2one(
        comodel_name="amdec.system",
        string="Système",
    )

    amdec_line_ids = fields.One2many(
        comodel_name="amdec.line",
        inverse_name="composante_id",
        string="Modes de défaillance",
    )
