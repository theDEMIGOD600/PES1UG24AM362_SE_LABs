"""Full test suite for income_tax module achieving 100% line and branch coverage."""

import pytest
from income_tax import taxable_income, tax_due, refund_status


def test_new_regime():
    """Initial starter test: standard deduction under new regime."""
    assert taxable_income(1000000, "new", 0) == 925000


def test_below_exemption():
    """Initial starter test: income below exemption threshold."""
    assert tax_due(200000, 30) == 0


def test_taxable_income_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_zero_gross():
    assert taxable_income(0, "new", 0) == 0


def test_taxable_income_old_regime_capped_investments():
    assert taxable_income(600000, "old", 200000) == 400000


def test_taxable_income_old_regime_uncapped_investments():
    assert taxable_income(600000, "old", 100000) == 450000


def test_taxable_income_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(600000, "unsupported", 0)


def test_taxable_income_deduction_exceeds():
    assert taxable_income(50000, "new", 0) == 0


def test_tax_due_negative():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-5, 30)


def test_tax_due_super_senior():
    assert tax_due(600000, 80) == 5000


def test_tax_due_senior():
    assert tax_due(400000, 60) == 5000


def test_tax_due_exact_exemption():
    assert tax_due(250000, 30) == 0


def test_tax_due_slab_1():
    assert tax_due(400000, 30) == 7500


def test_tax_due_slab_2():
    assert tax_due(600000, 30) == 32500


def test_refund_status_refund():
    assert refund_status(50000, 30000, True) == "refund"


def test_refund_status_refund_delayed():
    assert refund_status(50000, 30000, False) == "refund delayed"


def test_refund_status_pay_balance():
    assert refund_status(20000, 30000, True) == "pay balance"


def test_refund_status_pay_balance_penalty():
    assert refund_status(20000, 30000, False) == "pay balance with penalty"


def test_refund_status_settled():
    assert refund_status(30000, 30000, True) == "settled"
