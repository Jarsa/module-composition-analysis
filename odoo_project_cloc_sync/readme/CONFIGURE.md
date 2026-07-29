On each project (Odoo MCA > Projects):

1. Set **Odoo Cloc URL** to the base URL of the customer instance (it must have
   the `odoo_cloc` module installed).
2. Optionally set **Cloc Token** if the customer instance defines the
   `odoo_cloc.webhook_token` system parameter.
3. Enable **Sync Modules from Odoo Cloc** to include the project in the daily
   scheduled action *Odoo Projects - Sync modules from Odoo Cloc*.
