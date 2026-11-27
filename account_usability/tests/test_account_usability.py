from odoo import Command
from odoo.tests import TransactionCase


class TestAccountUsability(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = cls.env["account.account.tag"].create(
            {"name": "Test Tag", "applicability": "accounts"}
        )
        cls.account_1 = cls.env["account.account"].create(
            {"name": "Test Account 1", "code": "1001"}
        )
        cls.account_2 = cls.env["account.account"].create(
            {"name": "Test Account 2", "code": "2000"}
        )

    def test_search_accounts_on_tag(self):
        # The m2o follows the core account_ids <-> tag_ids m2m.
        self.account_1.tag_ids = [Command.set(self.tag.ids)]
        self.assertEqual(self.account_1.tag_id, self.tag)

        accounts = self.env["account.account"].search([("tag_id", "=", self.tag.id)])
        self.assertEqual(accounts, self.account_1)

        # Dotted search through the m2o, like the account group search
        # this module provided before Odoo 20.0.
        accounts = self.env["account.account"].search(
            [("tag_id.name", "=", "Test Tag")]
        )
        self.assertEqual(accounts, self.account_1)

        # Removing the tag from the core m2m clears the m2o too.
        self.account_1.tag_ids = [Command.clear()]
        accounts = self.env["account.account"].search([("tag_id", "=", self.tag.id)])
        self.assertFalse(accounts)

    def test_tag_id_follows_the_tag_form(self):
        self.tag.account_ids = [Command.link(self.account_1.id)]
        self.assertEqual(self.account_1.tag_id, self.tag)
        self.tag.account_ids = [Command.unlink(self.account_1.id)]
        self.assertFalse(self.account_1.tag_id)

    def test_accounting_groups_are_selectable(self):
        privilege = self.env.ref("account.res_groups_privilege_accounting")
        for xmlid in ("account.group_account_readonly", "account.group_account_user"):
            self.assertEqual(self.env.ref(xmlid).privilege_id, privilege)
