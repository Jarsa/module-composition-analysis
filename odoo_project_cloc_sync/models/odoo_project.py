# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

import requests

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/odoo_cloc/webhook/"


class OdooProject(models.Model):
    _inherit = "odoo.project"

    cloc_sync = fields.Boolean(
        string="Sync Modules from Odoo Cloc",
        help="Sync daily the installed modules and their versions from the "
        "odoo_cloc webhook of the customer instance.",
    )
    cloc_url = fields.Char(
        string="Odoo Cloc URL",
        help="Base URL of the customer instance exposing the odoo_cloc webhook, "
        "e.g. https://customer.odoo.com",
    )
    cloc_token = fields.Char(
        help="Mandatory token, must match the 'odoo_cloc.webhook_token' "
        "system parameter of the customer instance.",
    )
    cloc_last_sync = fields.Datetime(readonly=True)
    sloc_total = fields.Integer(
        string="Total SLOC",
        compute="_compute_sloc_total",
        help="Sum of the lines of code of the custom modules reported by the "
        "odoo_cloc webhook.",
    )

    @api.depends("project_module_ids.sloc")
    def _compute_sloc_total(self):
        for rec in self:
            rec.sloc_total = sum(rec.project_module_ids.mapped("sloc"))

    def action_sync_cloc_modules(self):
        for rec in self:
            data = rec._fetch_cloc_data()
            versions = data.get("versions")
            if not versions:
                continue
            lines = [
                f"{name} {version or ''}".strip()
                for name, version in sorted(versions.items())
            ]
            wizard = self.env["odoo.project.import.modules"].create(
                {
                    "odoo_project_id": rec.id,
                    "modules_list": "\n".join(lines),
                }
            )
            wizard.action_import()
            modules_sloc = data.get("modules") or {}
            for module in rec.project_module_ids:
                module.sloc = modules_sloc.get(module.module_id.name, 0)
            rec.cloc_last_sync = fields.Datetime.now()
        return True

    def _fetch_cloc_data(self):
        """Return {"modules": {name: sloc}, "versions": {name: version}}."""
        self.ensure_one()
        url = (self.cloc_url or "").rstrip("/") + WEBHOOK_PATH
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {"with_versions": True, "token": self.cloc_token or None},
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json().get("result") or {}
        except (OSError, ValueError) as exc:
            _logger.warning("Cloc sync failed for %s: %s", self.display_name, exc)
            return {}
        if "versions" not in result:
            # Old webhook without versions: plain {module: sloc} mapping
            return {"modules": result, "versions": dict.fromkeys(result, False)}
        return result

    def _cron_sync_cloc_modules(self):
        projects = self.search([("cloc_sync", "=", True), ("cloc_url", "!=", False)])
        for project in projects:
            try:
                project.action_sync_cloc_modules()
            except Exception:
                _logger.exception(
                    "Cloc sync failed for project %s", project.display_name
                )
        return True
