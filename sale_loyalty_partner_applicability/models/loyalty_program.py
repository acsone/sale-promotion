# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    def _get_valid_products(self, products):
        current_so = self.env.context.get("order")
        # The order is set into the context by the sale order line
        # when the method _program_check_compute_points is called.
        # This allows to check the partner of the order and filter
        # the rules based on the partner domain.
        valid_programs = self
        if current_so:
            # The applicable partner is resolved per program (not once for
            # the whole batch): a module can define a beneficiary partner
            # that depends on the specific program (e.g. the commercial
            # entity for one program, the invoiced partner for another),
            # so a single partner for every program in self would check the
            # wrong partner for those programs.
            valid_programs = self.filtered(
                lambda p: p._is_partner_valid(
                    current_so._get_applicable_partner_for_loyalty_program(p)
                )
            )
        return super(LoyaltyProgram, valid_programs)._get_valid_products(products)
