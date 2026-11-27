# Copyright 2018 FOREST AND BIOMASS ROMANIA SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    # Stored m2o with the first tag of the core tag_ids m2m, to group and
    # search accounts by tag from the account side, like the account group
    # this module provided before Odoo 20.0. Computed, so it follows tag_ids
    # however it changes (account form, tag form, code-based tags) and is
    # filled on install and upgrade. Accounts with several tags only carry
    # the first one here; search on tag_ids to match any of them.
    tag_id = fields.Many2one(
        comodel_name="account.account.tag",
        string="Main Tag",
        compute="_compute_tag_id",
        store=True,
        index="btree",
    )

    @api.depends("tag_ids")
    def _compute_tag_id(self):
        for account in self:
            account.tag_id = account.tag_ids[:1]
