"""Unit test cases for Branch Coverage of income_tax application.

Systematically validates all decision branches, truth combinations,
boundary conditions, and edge cases.
"""

import pytest
from income_tax import taxable_income, tax_due, refund_status


class TestTaxableIncomeBranches:
    """Branch testing for taxable_income decision points."""

    def test_branch_gross_negative(self):
        """Branch: gross < 0 evaluates to True."""
        with pytest.raises(ValueError, match="invalid income"):
            taxable_income(-1, "new", 0)

    def test_branch_gross_non_negative(self):
        """Branch: gross < 0 evaluates to False (boundary: gross = 0)."""
        assert taxable_income(0, "new", 0) == 0

    def test_branch_regime_new(self):
        """Branch: regime == 'new' evaluates to True."""
        assert taxable_income(500000, "new", 0) == 425000

    def test_branch_regime_old_investment_above_cap(self):
        """Branch: regime == 'old' AND investments > 150000 (True)."""
        # Capped at 150,000 + 50,000 deduction = 200,000
        assert taxable_income(600000, "old", 250000) == 400000

    def test_branch_regime_old_investment_at_cap(self):
        """Branch: regime == 'old' AND investments == 150000 (Boundary)."""
        assert taxable_income(600000, "old", 150000) == 400000

    def test_branch_regime_old_investment_below_cap(self):
        """Branch: regime == 'old' AND investments < 150000 (False)."""
        # Deduction = 50,000 + 80,000 = 130,000
        assert taxable_income(600000, "old", 80000) == 470000

    def test_branch_regime_unknown(self):
        """Branch: regime neither 'new' nor 'old' (else branch)."""
        with pytest.raises(ValueError, match="unknown regime"):
            taxable_income(600000, "flat_tax", 0)

    def test_branch_taxable_negative_clamped_to_zero(self):
        """Branch: taxable < 0 evaluates to True (returns 0)."""
        assert taxable_income(40000, "new", 0) == 0

    def test_branch_taxable_exactly_zero(self):
        """Branch: taxable == 0 boundary (gross == deduction)."""
        assert taxable_income(75000, "new", 0) == 0

    def test_branch_taxable_positive(self):
        """Branch: taxable < 0 evaluates to False (returns positive taxable)."""
        assert taxable_income(100000, "new", 0) == 25000


class TestTaxDueBranches:
    """Branch testing for tax_due decision points and age brackets."""

    def test_branch_taxable_negative(self):
        """Branch: taxable < 0 evaluates to True."""
        with pytest.raises(ValueError, match="invalid amount"):
            tax_due(-1, 45)

    def test_branch_age_super_senior_above_80(self):
        """Branch: age > 80 (exempt = 500,000)."""
        assert tax_due(500000, 85) == 0

    def test_branch_age_super_senior_exact_80(self):
        """Branch: age == 80 boundary (exempt = 500,000)."""
        assert tax_due(500000, 80) == 0

    def test_branch_age_senior_exact_60(self):
        """Branch: age == 60 boundary (exempt = 300,000)."""
        assert tax_due(300000, 60) == 0

    def test_branch_age_senior_between_60_and_80(self):
        """Branch: 60 <= age < 80 (exempt = 300,000)."""
        assert tax_due(350000, 70) == 2500  # (350000-300000)*5%

    def test_branch_age_below_60_boundary_59(self):
        """Branch: age < 60 boundary (age = 59, exempt = 250,000)."""
        assert tax_due(250000, 59) == 0

    def test_branch_taxable_less_than_exempt(self):
        """Branch: taxable < exempt evaluates to True (returns 0)."""
        assert tax_due(150000, 25) == 0

    def test_branch_taxable_equal_exempt(self):
        """Branch: taxable == exempt evaluates to True (returns 0)."""
        assert tax_due(250000, 25) == 0

    def test_branch_slab_below_or_equal_250k(self):
        """Branch: slab <= 250,000 evaluates to True."""
        # taxable = 450,000; exempt = 250,000; slab = 200,000 <= 250,000
        # tax = 200,000 * 5 // 100 = 10,000
        assert tax_due(450000, 35) == 10000

    def test_branch_slab_exact_250k_boundary(self):
        """Branch: slab == 250,000 boundary."""
        # taxable = 500,000; exempt = 250,000; slab = 250,000
        # tax = 250,000 * 5 // 100 = 12,500
        assert tax_due(500000, 35) == 12500

    def test_branch_slab_above_250k(self):
        """Branch: slab > 250,000 evaluates to False for (slab <= 250,000)."""
        # taxable = 750,000; exempt = 250,000; slab = 500,000
        # tax = 12500 + (500000 - 250000) * 20 // 100 = 12500 + 50000 = 62500
        assert tax_due(750000, 35) == 62500


class TestRefundStatusBranches:
    """Branch testing for refund_status difference and filing time conditions."""

    def test_branch_diff_positive_filed_on_time(self):
        """Branch: difference > 0 AND filed_on_time == True."""
        assert refund_status(100000, 80000, True) == "refund"

    def test_branch_diff_positive_filed_late(self):
        """Branch: difference > 0 AND filed_on_time == False."""
        assert refund_status(100000, 80000, False) == "refund delayed"

    def test_branch_diff_negative_filed_on_time(self):
        """Branch: difference < 0 AND filed_on_time == True."""
        assert refund_status(60000, 80000, True) == "pay balance"

    def test_branch_diff_negative_filed_late(self):
        """Branch: difference < 0 AND filed_on_time == False."""
        assert refund_status(60000, 80000, False) == "pay balance with penalty"

    def test_branch_diff_zero_settled_on_time(self):
        """Branch: difference == 0 (neither > 0 nor < 0)."""
        assert refund_status(50000, 50000, True) == "settled"

    def test_branch_diff_zero_settled_late(self):
        """Branch: difference == 0 with filed_on_time False."""
        assert refund_status(50000, 50000, False) == "settled"
