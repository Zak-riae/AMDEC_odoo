from odoo import _, api, fields, models


class AmdecGrilleOccurence(models.Model):
    _name = "amdec.grille.occurence"
    _description = "amdec_grille_occurence"
    _order = "value,frequence,id"

    name = fields.Char()

    active = fields.Boolean(default=True)

    value = fields.Integer()

    frequence = fields.Integer(
        string="Fréquence",
        help=(
            "Fréquence maximum par période, l'algorithme va chercher le plus"
            " petit."
        ),
    )

    period_id = fields.Many2one(
        comodel_name="amdec.period", string="Période", help="Not supported"
    )
