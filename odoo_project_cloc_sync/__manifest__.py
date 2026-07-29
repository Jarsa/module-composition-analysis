# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Odoo Project Cloc Sync",
    "summary": "Sync installed modules and versions from the odoo_cloc webhook.",
    "version": "19.0.1.0.0",
    "category": "Tools",
    "author": "Jarsa",
    "website": "https://www.jarsa.com",
    "data": [
        "data/ir_cron.xml",
        "views/odoo_project.xml",
    ],
    "depends": [
        "odoo_project",
    ],
    "license": "AGPL-3",
}
