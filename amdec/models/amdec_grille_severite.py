from odoo import _, api, fields, models


class AmdecGrilleSeverite(models.Model):
    _name = "amdec.grille.severite"
    _description = "amdec_grille_severite"
    _order = "value,id"

    name = fields.Char()

    value = fields.Integer()
