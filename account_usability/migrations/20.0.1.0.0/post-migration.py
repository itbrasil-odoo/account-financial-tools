# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Fill the new account.account.tag_id on databases coming from 19.0.

    The field mirrors the first tag of the core tag_ids m2m and is only kept
    in sync by create/write, so existing accounts would stay empty.
    """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    accounts = (
        env["account.account"]
        .with_context(active_test=False)
        .search([("tag_ids", "!=", False)])
    )
    accounts._sync_tag_id_values()
