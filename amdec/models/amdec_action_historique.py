from odoo import _, api, fields, models


class AmdecActionHistorique(models.Model):
    _name = "amdec.action.historique"
    _description = "amdec_action_historique"

    name = fields.Char()

    date_action = fields.Datetime()

    responsable_action_id = fields.Many2one(
        comodel_name="res.partner",
        string="Responsable",
    )

    action_corrige_panne = fields.Boolean(string="L'action a corrigé la panne")

    action_realise = fields.Boolean(string="L'action a été réalisé")

    action_reparation = fields.Many2one(
        comodel_name="amdec.reparation.type",
        string="Type réparation",
    )

    composante_id = fields.Many2one(
        comodel_name="amdec.composante",
        string="Composante",
    )

    system_id = fields.Many2one(
        related="composante_id.system_id",
        string="Système",
    )

    type_panne_id = fields.Many2one(
        comodel_name="amdec.panne.type",
        string="Type panne",
    )

    defaillance_id = fields.Many2one(
        comodel_name="amdec.defaillance",
        string="Défaillance",
    )
