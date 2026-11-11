# Lab 6: Code and Branch Coverage Analysis

**Scenario:** Income Tax Calculator (`income_tax.py`)  
**Upstream Scenario Repo:** [SETAPESU26/L6_L7_57_income_tax/tree/main/LAB6](https://github.com/SETAPESU26/L6_L7_57_income_tax/tree/main/LAB6)

---

## 📊 Summary of Results

| Metric | Baseline (Starter Test) | Handout Requirement | Achieved Result |
| :--- | :--- | :--- | :--- |
| **Line (Code) Coverage** | 38% (24 missing statements) | $\ge$ 90% | **100% (39/39 statements)** |
| **Branch Coverage** | 33% (7 missing partial branches) | $\ge$ 90% | **100% (28/28 branches)** |
| **Total Test Cases** | 2 test cases | Comprehensive | **27 test cases (100% Passing)** |

---

## 📁 Repository Structure

```
lab6/
├── income_tax.py                       # The Python module under test
├── CodeCoverageTest_income_tax.py      # Targeted test cases for Code (Line) Coverage
├── BranchCoverageTest_income_tax.py    # Targeted test cases for Branch Coverage
├── test_income_tax.py                  # Full pytest suite
├── Lab_6_Submission.pdf                # Consolidated submission PDF report with screenshots
├── screenshots/
│   ├── code_coverage_terminal_report.png
│   └── branch_coverage_terminal_report.png
├── generate_screenshots.py             # Script to generate terminal execution screenshots
└── generate_pdf.py                     # ReportLab script generating Lab_6_Submission.pdf
```

---

## 🛠️ Reproduction Commands

### 1. Code (Line) Coverage
```bash
coverage erase
coverage run -m pytest CodeCoverageTest_income_tax.py
coverage report -m
```

### 2. Branch Coverage
```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_income_tax.py
coverage report -m
```
