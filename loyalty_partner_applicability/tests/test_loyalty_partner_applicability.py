# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import TestLoyaltyPartnerApplicabilityCase


class TestLoyaltyPartnerApplicability(TestLoyaltyPartnerApplicabilityCase):
    def _assertCheckValidPartner(self, program, partner, expected):
        self.assertEqual(
            program._is_partner_valid(partner),
            expected,
            f"Partner {partner.name} should be {'valid' if expected else 'invalid'} "
            f"for program {program.name} (_is_partner_valid)",
        )
        domain = program._get_partner_domain(partner)
        is_valid = partner.search_count(domain) > 0
        self.assertEqual(
            is_valid,
            expected,
            f"Partner {partner.name} should be {'valid' if expected else 'invalid'} "
            f"for program {program.name} (_get_partner_domain)",
        )

    def test_program_no_restriction(self):
        program = self.program_no_restriction
        self.assertFalse(program._is_coupon_sharing_allowed())
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, True)

    def test_restriction_on_partner_ids(self):
        program = self.program_restricted_to_partner_ids
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, False)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_restriction_on_partner_domain(self):
        program = self.program_restricted_to_partner_domain
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, False)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_restriction_on_partner_domain_and_partner_ids(self):
        program = self.program_restricted_to_partner_domain_and_partner_ids
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_restriction_on_partner_at_rule_level(self):
        program = self.program_and_rule_restricted
        # At program level the partner 1 and 2 are valid
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, False)
        # At rule level we have 1 rule for partner 1 and 2 and 1 rule for partner 2
        rule = program.rule_ids.filtered(lambda r: r._is_partner_valid(self.partner1))
        self.assertEqual(len(rule), 1)
        rule = program.rule_ids.filtered(lambda r: r._is_partner_valid(self.partner2))
        self.assertEqual(len(rule), 1)
        # even if a rule is allowed for partner 3, it's not valid since
        # the program is not valid for partner 3
        rule = program.rule_ids.filtered(lambda r: self.partner3 in r.partner_ids)
        self.assertEqual(len(rule), 1)
        rule = program.rule_ids.filtered(lambda r: r._is_partner_valid(self.partner3))
        self.assertEqual(len(rule), 0)
