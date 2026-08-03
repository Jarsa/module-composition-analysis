# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Odoo Project Cloc Sync",
    "summary": "Sync installed modules and versions from the odoo_cloc webhook.",
    "version": "19.0.1.1.0",
    "category": "Tools",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/module-composition-analysis",
    "data": [
        "data/ir_cron.xml",
        "views/odoo_project.xml",
    ],
    "depends": [
        "odoo_project",
    ],
    "license": "AGPL-3",
}
