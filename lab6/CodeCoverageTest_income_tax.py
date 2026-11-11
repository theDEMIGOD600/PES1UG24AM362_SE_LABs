"""Unit test cases for Code (Line) Coverage of income_tax application."""

import pytest
from income_tax import taxable_income, tax_due, refund_status


def test_taxable_income_negative_gross():
    """Test invalid negative gross income raises ValueError."""
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-50000, "new", 0)


def test_taxable_income_new_regime():
    """Test standard deduction for new tax regime."""
    assert taxable_income(1000000, "new", 0) == 925000


def test_taxable_income_old_regime_high_investments():
    """Test old regime where investments exceed 150,000 cap."""
    assert taxable_income(800000, "old", 200000) == 600000


def test_taxable_income_old_regime_low_investments():
    """Test old regime where investments are below cap."""
    assert taxable_income(800000, "old", 50000) == 700000


def test_taxable_income_invalid_regime():
    """Test unrecognized tax regime raises ValueError."""
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "invalid_regime", 0)


def test_taxable_income_deduction_exceeds_gross():
    """Test that taxable income returns 0 when deduction exceeds gross."""
    assert taxable_income(50000, "new", 0) == 0


def test_tax_due_negative_amount():
    """Test negative taxable amount raises ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1000, 30)


def test_tax_due_super_senior_citizen():
    """Test super senior citizen (age >= 80) tax exemption and calculation."""
    assert tax_due(600000, 85) == 5000


def test_tax_due_senior_citizen():
    """Test senior citizen (age 60 to 79) tax calculation."""
    assert tax_due(400000, 65) == 5000


def test_tax_due_regular_below_exemption():
    """Test regular age (< 60) income below or equal to exemption limit."""
    assert tax_due(200000, 30) == 0


def test_tax_due_regular_first_slab():
    """Test tax calculation within the first taxable slab (<= 250,000)."""
    assert tax_due(400000, 30) == 7500


def test_tax_due_regular_second_slab():
    """Test tax calculation exceeding first slab (> 250,000)."""
    assert tax_due(600000, 30) == 32500


def test_refund_status_overpaid_on_time():
    """Test refund when tax is overpaid and filed on time."""
    assert refund_status(50000, 30000, True) == "refund"


def test_refund_status_overpaid_delayed():
    """Test refund when tax is overpaid and filed late."""
    assert refund_status(50000, 30000, False) == "refund delayed"


def test_refund_status_underpaid_on_time():
    """Test pay balance when underpaid and filed on time."""
    assert refund_status(20000, 30000, True) == "pay balance"


def test_refund_status_underpaid_delayed():
    """Test pay balance with penalty when underpaid and filed late."""
    assert refund_status(20000, 30000, False) == "pay balance with penalty"


def test_refund_status_settled():
    """Test settled status when tax paid equals tax due."""
    assert refund_status(30000, 30000, True) == "settled"
