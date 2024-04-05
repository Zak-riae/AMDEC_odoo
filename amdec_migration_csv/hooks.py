# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import csv
import datetime
import logging
import os
import sys

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Database
        dct_system = {}
        dct_component = {}
        dct_mode_defaillance = {}
        dct_database = {
            "system": dct_system,
            "component": dct_component,
            "mode_defaillance": dct_mode_defaillance,
        }

        # INIT AMDEC
        project_id = env["amdec.project"].create({"name": "Demo from CSV"})
        dct_database["project_id"] = project_id
        amdec_id = env["amdec.amdec"].create(
            {
                "name": "CSV AMDEC 2023",
                "amdec_project_id": project_id.id,
                "date_debut": datetime.datetime.strptime(
                    "01/01/2023", "%d/%m/%Y"
                ),
                "date_fin": datetime.datetime.strptime(
                    "31/12/2023", "%d/%m/%Y"
                ),
            }
        )
        dct_database["amdec_id"] = amdec_id

        # System
        csv_file_name = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "data", "System.csv")
        )
        read_csv(
            env,
            csv_file_name,
            "id_system,name",
            dct_system,
            cb_read_system,
            dct_database,
        )
        # Component
        csv_file_name = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "data", "Composantes.csv")
        )
        read_csv(
            env,
            csv_file_name,
            "id_system,id_composante,Composante",
            dct_component,
            cb_read_component,
            dct_database,
        )
        # Mode defaillance
        csv_file_name = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), "data", "Mode de defaillance.csv"
            )
        )
        read_csv(
            env,
            csv_file_name,
            "id_system,id_composante,Mode de défaillance",
            dct_mode_defaillance,
            cb_read_mode_defaillance,
            dct_database,
        )
        # sys.exit(1)


def read_csv(env, csv_file_name, expected_header, dct_value, cb, dct_database):
    with open(csv_file_name) as file:
        first_line = file.readline().strip("\n")
        if first_line != expected_header:
            raise ValueError(
                f"Reading CSV '{csv_file_name}'. Expect header like"
                f" '{expected_header}' and receive '{first_line}'."
            )
        # Move cursor at 0
        file.seek(0)
        for line in csv.DictReader(file):
            try:
                cb(env, line, dct_value, dct_database)
            except Exception as e:
                # Easy debug!
                raise e


def cb_read_system(env, line, dct_value, dct_database):
    id_system = line.get("id_system").strip()
    name = line.get("name").strip()
    value = {"name": name}
    system_id = env["amdec.system"].create(value)
    dct_value[id_system] = {
        "obj_id": system_id,
        "name": name,
        "id": id_system,
    }


def cb_read_component(env, line, dct_value, dct_database):
    id_system = line.get("id_system").strip()
    id_component = line.get("id_composante").strip()
    dct_system = dct_database.get("system", {}).get(id_system)
    name = line.get("Composante").strip()
    value = {"name": name, "system_id": dct_system.get("obj_id").id}
    component_id = env["amdec.composante"].create(value)
    dct_value[id_component] = {
        "obj_id": component_id,
        "name": name,
        "id": id_component,
    }


def cb_read_mode_defaillance(env, line, dct_value, dct_database):
    id_system = line.get("id_system").strip()
    id_component = line.get("id_composante").strip()
    dct_system = dct_database.get("system", {}).get(id_system)
    dct_component = dct_database.get("component", {}).get(id_component)
    name = line.get("Mode de défaillance").strip()
    value = {
        "name": name,
        # "system_id": dct_system.get("obj_id").id,
        # "composante_id": dct_component.get("obj_id").id,
    }
    value_id = env["amdec.defaillance"].create(value)
    dct_value[name] = {
        "obj_id": value_id,
        "name": name,
        "id": name,
    }
