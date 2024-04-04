from odoo import _, api, fields, models


class AmdecProject(models.Model):
    _name = "amdec.project"
    _description = "amdec_project"

    name = fields.Char()

    amdec_ids = fields.One2many(
        comodel_name="amdec.amdec",
        inverse_name="amdec_project_id",
        string="AMDEC",
    )

    period_ids = fields.Many2many(
        comodel_name="amdec.period", string="Périodes", help="COMPUTE"
    )

    grille_occurence_ids = fields.Many2many(
        comodel_name="amdec.grille.occurence",
        string="Grilles occurence",
        help="COMPUTE",
    )

    general_amdec_seuil_rpn = fields.Integer(
        string="Seuil RPN",
        help="Default value from configuration.",
        default=100,
    )

    description = fields.Text(
        string="Périmètre d'étude",
        help="Quel est la portée de ce projet d'AMDEC.",
    )

    @api.multi
    def action_update_all_occurence(self):
        self.ensure_one()
        for amdec_id in self.amdec_ids:
            amdec_id.action_update_occurence()
