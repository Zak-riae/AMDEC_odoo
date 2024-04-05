{
    "name": "AMDEC",
    "category": "Uncategorized",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": ["base", "web_group_expand"],
    "data": [
        "security/ir.model.access.csv",
        "views/amdec_action_historique.xml",
        "views/amdec_amdec.xml",
        "views/amdec_composante.xml",
        "views/amdec_defaillance.xml",
        "views/amdec_grille_detectabilite.xml",
        "views/amdec_grille_occurence.xml",
        "views/amdec_grille_severite.xml",
        "views/amdec_inspection.xml",
        "views/amdec_line.xml",
        "views/amdec_panne_type.xml",
        "views/amdec_period.xml",
        "views/amdec_project.xml",
        "views/amdec_reparation_type.xml",
        "views/amdec_system.xml",
        "views/res_config_settings.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
