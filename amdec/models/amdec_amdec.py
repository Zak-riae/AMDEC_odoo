import logging
import random

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class AmdecAmdec(models.Model):
    _name = "amdec.amdec"
    _description = "amdec_amdec"

    name = fields.Char()

    amdec_precedent_id = fields.Many2one(
        comodel_name="amdec.amdec",
        string="AMDEC précédent",
    )

    amdec_project_id = fields.Many2one(
        comodel_name="amdec.project",
        string="Project",
    )

    date_debut = fields.Date(string="Date début")

    date_fin = fields.Date(string="Date fin")

    amdec_line_ids = fields.One2many(
        comodel_name="amdec.line",
        inverse_name="amdec_id",
        string="Modes de défaillance",
    )

    has_missing_data = fields.Boolean(
        store=True, compute="_compute_has_missing_data"
    )

    @api.multi
    def action_clear_occ_lines(self):
        self.ensure_one()
        for line_id in self.amdec_line_ids:
            line_id.occurence = 0
            line_id.grille_occurence_id = 0
            line_id.inspection_ids = [(6, 0, [])]

    @api.multi
    def action_update_occurence(self):
        self.ensure_one()
        _logger.info(
            f"Execute algorithme to search occurence into AMDEC '{self.name}'"
        )
        period_ids = self.env["amdec.period"].search(
            [
                ("date_debut", ">=", self.date_debut),
                ("date_fin", "<=", self.date_fin),
            ]
        )
        # Force date_debut et date_fin des périodes et non du AMDEC
        # date_debut_period = self.date_debut
        # date_fin_period = self.date_fin
        date_debut_period = min([a.date_debut for a in period_ids])
        date_fin_period = max([a.date_fin for a in period_ids])
        # TODO this not work if period not follow
        #  (S'il manque des dates entre et qu'il y a une inspection entre, il sera considéré)
        # inspection_ids = self.env["amdec.inspection"].search(
        #     [
        #         ("date_action", ">=", date_debut_period),
        #         ("date_action", "<=", date_fin_period),
        #     ]
        # )

        # Exemple
        for line_id in self.amdec_line_ids:
            # Trouver le nombre d'inspection pour la période désiré
            # TODO bug global seuil RPN default value not working
            # TODO problème de logique, le tableau d'occurence est prévu pour 1 an,
            #  mais l'AMDEC peut être différent d'un an.
            inspection_ids = self.env["amdec.inspection"].search(
                [
                    ("date_action", ">=", date_debut_period),
                    ("date_action", "<=", date_fin_period),
                    ("defaillance_id", "=", line_id.defaillance_id.id),
                ]
            )
            freq = sum([a.frequence for a in inspection_ids])
            occ_ids = self.env["amdec.grille.occurence"].search(
                [
                    ("frequence", "<", freq),
                ],
                order="frequence desc, value desc",
                limit=1,
            )
            if not occ_ids:
                _logger.warning(
                    f"Cannot find occurence for AMDEC line {line_id.id}"
                )
                line_id.occurence = 0
                line_id.grille_occurence_id = 0
                line_id.inspection_ids = [(6, 0, [])]
            else:
                line_id.occurence = occ_ids.value
                line_id.grille_occurence_id = occ_ids.id
                line_id.inspection_ids = [(6, 0, inspection_ids.ids)]

    @api.multi
    def action_execute_algo_2(self):
        self.ensure_one()
        _logger.error("Execute algo 2")

    # @api.multi
    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     self.ensure_one()
    #     default = dict(default or {})
    #     if 'name' not in default:
    #         default['name'] = _("%s (copy)") % (self.name)
    #     return super(AmdecAmdec, self).copy(default=default)

    @api.depends("amdec_line_ids", "amdec_line_ids.rpn")
    def _compute_has_missing_data(self):
        for rec in self:
            # If an AMDEC line missing a rpn, it's True
            if rec.amdec_line_ids:
                rec.has_missing_data = not [
                    a for a in rec.amdec_line_ids if not a.rpn
                ]
            else:
                rec.has_missing_data = False
