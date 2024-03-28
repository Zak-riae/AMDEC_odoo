# Copyright 2023 TechnoLibre inc. - Mathieu Benoit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models

DEFAULT_GENERAL_AMDEC_SEUIL_RPN = 100


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    default_general_amdec_seuil_rpn = fields.Integer(
        default=DEFAULT_GENERAL_AMDEC_SEUIL_RPN,
        default_model="amdec.project",
        string="Seuil de composante AMDEC par défaut",
        help="Default seuil for a AMDEC composante.",
    )

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env["ir.config_parameter"].sudo()
        param.set_param(
            "amdec.default_general_amdec_seuil_rpn",
            self.default_general_amdec_seuil_rpn,
        )
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            default_general_amdec_seuil_rpn=int(
                params.get_param(
                    "amdec.default_general_amdec_seuil_rpn",
                    DEFAULT_GENERAL_AMDEC_SEUIL_RPN,
                )
            )
        )
        return res
