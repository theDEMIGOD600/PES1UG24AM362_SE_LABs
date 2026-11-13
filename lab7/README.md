# Lab 7: Fuzzing for Input Validation Bugs

**Scenario:** Income Tax Parser (`income_tax_parser.py`)  
**Student Name:** Dhruvanth  
**SRN:** PES1UG24AM362  
**Upstream Scenario Repo:** [SETAPESU26/L6_L7_57_income_tax/tree/main/LAB7](https://github.com/SETAPESU26/L6_L7_57_income_tax/tree/main/LAB7)

---

## 📊 Summary of Fuzz Testing

Using property-based testing with **Hypothesis**, all functions in `income_tax_parser.py` were fuzz-tested with arbitrary text, `NoneType`, and boundary inputs:

| Function | Initial Status (Buggy) | Hypothesis Counterexample | Fixed Status (Hardened) |
| :--- | :--- | :--- | :--- |
| `clean_pan(pan)` | ❌ Crashes on `None` (`AttributeError`) | `s=None` | ✅ Safely returns `""` |
| `parse_amount(text)` | ❌ Crashes on empty / non-numeric (`ValueError`) | `s=''` or `s='Rs '` | ✅ Safely returns `0` |
| `parse_tax_slab(line)` | ❌ Crashes on malformed delimiters (`ValueError`) | `s=':'` or `s=''` | ✅ Safely returns `(0, 0, 0)` |

---

## 📸 Screenshots Overview

| Screenshot | Description | File |
| :--- | :--- | :--- |
| **SS1** | `python income_tax_parser.py` run on the buggy module | `screenshots/SS1_buggy_run.png` |
| **SS2** | `pytest test_income_tax_parser.py` with Hypothesis tests failing on buggy module | `screenshots/SS2_buggy_tests_failing.png` |
| **SS3** | `python income_tax_parser.py` run on fixed module | `screenshots/SS3_fixed_run.png` |
| **SS4** | `pytest test_income_tax_parser.py` with all tests passing on fixed module | `screenshots/SS4_fixed_tests_passing.png` |

---

## 📁 Repository Structure

```
lab7/
├── income_tax_parser.py               # Fixed & hardened module
├── income_tax_parser_buggy.py         # Original buggy reference module
├── test_income_tax_parser.py          # Completed Hypothesis property-based fuzz tests
├── PES1UG24AM362_Dhruvanth_LAB7.pdf   # Submission PDF with screenshots & reflection answers
├── Lab_7_Submission.pdf               # Copy of submission PDF
├── screenshots/
│   ├── SS1_buggy_run.png
│   ├── SS2_buggy_tests_failing.png
│   ├── SS3_fixed_run.png
│   └── SS4_fixed_tests_passing.png
├── generate_screenshots.py            # Screenshot rendering script
├── generate_pdf.py                    # PDF generation script
└── README.md
```

---

## 🛠️ Reproduction Commands

```bash
# 1. Run Hypothesis tests on fixed module (All 3 Pass)
pytest test_income_tax_parser.py

# 2. Run the interactive CLI
python income_tax_parser.py
```
