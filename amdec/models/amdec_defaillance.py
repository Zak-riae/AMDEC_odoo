from odoo import _, api, fields, models


class AmdecDefaillance(models.Model):
    _name = "amdec.defaillance"
    _description = "AMDEC failure"

    name = fields.Char()

    cause = fields.Text()

    effet = fields.Text()

    action_entreprendre = fields.Text()

    inspection_ids = fields.One2many(
        comodel_name="amdec.inspection",
        inverse_name="defaillance_id",
        string="Inspections",
    )

    action_historique_ids = fields.One2many(
        comodel_name="amdec.action.historique",
        inverse_name="defaillance_id",
        string="Actions historique",
    )

    amdec_line_ids = fields.One2many(
        comodel_name="amdec.line",
        inverse_name="defaillance_id",
        string="AMDEC lines",
    )

    composantes_ids = fields.Many2many(
        comodel_name="amdec.composante",
        relation="amdec_composante_defaillance_rel",
    )
