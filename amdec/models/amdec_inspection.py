from odoo import _, api, fields, models


class AmdecInspection(models.Model):
    _name = "amdec.inspection"
    _description = "amdec_inspection"

    active = fields.Boolean(default=True)

    name = fields.Char(store=True, compute="_compute_name")

    date_action = fields.Date()

    defaillance_id = fields.Many2one(
        comodel_name="amdec.defaillance",
        string="Défaillance",
    )

    responsable_action_id = fields.Many2one(
        comodel_name="res.partner",
        string="Responsable",
    )

    frequence = fields.Integer(help="Par défaut, devrait être 0 ou 1")

    @api.depends(
        "date_action",
        "defaillance_id",
        "responsable_action_id",
        "frequence",
    )
    def _compute_name(self):
        for rec in self:
            rec.name = (
                f"{rec.date_action} {rec.defaillance_id.name} {rec.responsable_action_id.name} {rec.frequence}"
            )
