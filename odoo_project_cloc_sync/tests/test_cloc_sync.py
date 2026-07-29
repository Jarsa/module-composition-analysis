# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from unittest import mock

from odoo.tests.common import TransactionCase


class FakeResponse:
    def __init__(self, result):
        self.result = result

    def raise_for_status(self):
        pass

    def json(self):
        return {"jsonrpc": "2.0", "result": self.result}


class TestClocSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.branch = cls.env["odoo.branch"].create({"name": "19.0", "sequence": 190})
        cls.project = cls.env["odoo.project"].create(
            {
                "name": "Test Customer",
                "odoo_version_id": cls.branch.id,
                "cloc_sync": True,
                "cloc_url": "https://customer.example.com",
            }
        )

    def _sync(self, result):
        with mock.patch(
            "odoo.addons.odoo_project_cloc_sync.models.odoo_project.requests.post",
            return_value=FakeResponse(result),
        ) as post:
            self.project.action_sync_cloc_modules()
        return post

    def test_sync_with_versions(self):
        post = self._sync(
            {
                "modules": {"custom_module": 100},
                "versions": {
                    "custom_module": "19.0.1.0.0",
                    "sale": "19.0.1.2",
                },
            }
        )
        url = post.call_args[0][0]
        self.assertEqual(url, "https://customer.example.com/odoo_cloc/webhook/")
        self.assertTrue(post.call_args[1]["json"]["params"]["with_versions"])
        modules = self.project.project_module_ids
        self.assertEqual(len(modules), 2)
        custom = modules.filtered(
            lambda pm: pm.module_branch_id.module_id.name == "custom_module"
        )
        self.assertEqual(custom.installed_version, "19.0.1.0.0")
        self.assertTrue(self.project.cloc_last_sync)

    def test_sync_legacy_response(self):
        # Webhook viejo: solo {module: sloc}, sin versiones
        self._sync({"custom_module": 100})
        modules = self.project.project_module_ids
        self.assertEqual(len(modules), 1)
        self.assertFalse(modules.installed_version)

    def test_sync_error_does_not_break(self):
        with mock.patch(
            "odoo.addons.odoo_project_cloc_sync.models.odoo_project.requests.post",
            side_effect=OSError("boom"),
        ):
            self.project.action_sync_cloc_modules()
        self.assertFalse(self.project.project_module_ids)
        self.assertFalse(self.project.cloc_last_sync)

    def test_cron(self):
        with mock.patch(
            "odoo.addons.odoo_project_cloc_sync.models.odoo_project.requests.post",
            return_value=FakeResponse(
                {"modules": {}, "versions": {"base": "19.0.1.3"}}
            ),
        ):
            self.env["odoo.project"]._cron_sync_cloc_modules()
        self.assertEqual(len(self.project.project_module_ids), 1)
