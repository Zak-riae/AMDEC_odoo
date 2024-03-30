from odoo import _, api, fields, models


class AmdecGrilleDetectabilite(models.Model):
    _name = "amdec.grille.detectabilite"
    _description = "amdec_grille_detectabilite"
    _order = "value,id"

    name = fields.Char()

    value = fields.Integer()
