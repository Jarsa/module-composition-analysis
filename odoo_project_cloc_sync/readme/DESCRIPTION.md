Sync the list of installed modules (and their installed versions) of an Odoo
project from the `odoo_cloc` webhook exposed by the customer instance, instead
of importing them manually with the *Import modules* wizard.

A daily scheduled action keeps every project flagged for synchronization up to
date.

The lines of code (SLOC) of each custom module reported by the webhook are
stored on the project modules, and the project shows the total, so other
modules (e.g. invoicing) can consume this data without calling the webhook
again.
