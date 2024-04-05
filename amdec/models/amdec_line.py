from odoo import _, api, fields, models


class AmdecLine(models.Model):
    _name = "amdec.line"
    _description = "amdec_line"
    _rec_name = "defaillance_id"
    _order = "sequence,id"

    amdec_id = fields.Many2one(
        comodel_name="amdec.amdec",
        string="AMDEC",
    )

    defaillance_id = fields.Many2one(
        comodel_name="amdec.defaillance",
        string="Défaillance",
    )

    failure_mode_id = fields.Many2one(
        comodel_name="amdec.panne.type",
        string="Failure Mode",
    )

    historique_action_ids = fields.Many2many(
        comodel_name="amdec.action.historique",
        string="Historique Action",
    )

    effet = fields.Text(related="defaillance_id.effet")

    cause = fields.Text(related="defaillance_id.cause")

    action_entreprendre = fields.Text(
        related="defaillance_id.action_entreprendre"
    )

    general_amdec_seuil_rpn = fields.Integer(
        string="Seuil RPN",
        related="amdec_id.amdec_project_id.general_amdec_seuil_rpn",
    )

    is_seuil_superior = fields.Boolean(
        compute="_compute_rpn",
        store=True,
    )

    inspection_ids = fields.Many2many(
        comodel_name="amdec.inspection",
        string="Inspections",
    )

    occurence = fields.Integer(
        readonly=True,
        help=(
            "Calcul du nombre de fréquence sur l'ensemble des inspections par"
            " période de temps en appliquant la grille des seuils d'occurences"
            " dynamiques. La valeur par défaut est 0, ce qui annule le calcul."
            " Il doit être calculé par l'algorithme dans AMDEC."
        ),
    )

    grille_occurence_id = fields.Many2one(
        comodel_name="amdec.grille.occurence",
        readonly=True,
        string="Choix grille",
        help="Selected grille occurence to calcul RPN.",
    )

    detectabilite_id = fields.Many2one(
        comodel_name="amdec.grille.detectabilite",
        string="Detectabilite",
    )

    severite_id = fields.Many2one(
        comodel_name="amdec.grille.severite",
        string="Severite",
    )

    rpn = fields.Integer(
        compute="_compute_rpn",
        store=True,
    )

    composante_id = fields.Many2one(
        comodel_name="amdec.composante",
        string="Composante",
    )

    sequence = fields.Integer(default=10)

    system_id = fields.Many2one(
        related="composante_id.system_id",
        string="System",
    )

    @api.depends(
        "occurence",
        "detectabilite_id",
        "severite_id",
        "general_amdec_seuil_rpn",
    )
    def _compute_rpn(self):
        for rec in self:
            if rec.detectabilite_id and rec.severite_id and rec.occurence:
                rec.rpn = (
                    rec.occurence
                    * rec.detectabilite_id.value
                    * rec.severite_id.value
                )
                rec.is_seuil_superior = rec.rpn > rec.general_amdec_seuil_rpn
            else:
                rec.rpn = False
                rec.is_seuil_superior = False
