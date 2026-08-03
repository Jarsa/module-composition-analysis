# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class OdooProjectModule(models.Model):
    _inherit = "odoo.project.module"

    sloc = fields.Integer(
        string="SLOC",
        help="Lines of code reported by the odoo_cloc webhook of the customer "
        "instance (only custom modules are counted).",
    )
