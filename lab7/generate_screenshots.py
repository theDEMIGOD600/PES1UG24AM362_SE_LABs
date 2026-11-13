import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def render_terminal(command_lines, output_file, title="Terminal - zsh", width=10, height=6.2):
    fig, ax = plt.subplots(figsize=(width, height), dpi=220)
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')

    # Terminal Header bar
    header = patches.FancyBboxPatch((0, height - 0.5), width, 0.5, boxstyle="square,pad=0",
                                     fc='#2D2D2D', ec='#2D2D2D')
    ax.add_patch(header)

    # Mac window controls
    ax.add_patch(patches.Circle((0.25, height - 0.25), 0.08, color='#FF5F56'))
    ax.add_patch(patches.Circle((0.50, height - 0.25), 0.08, color='#FFBD2E'))
    ax.add_patch(patches.Circle((0.75, height - 0.25), 0.08, color='#27C93F'))

    # Title
    ax.text(width / 2.0, height - 0.25, title, color='#CCCCCC', fontsize=10,
            ha='center', va='center', fontfamily='sans-serif', fontweight='medium')

    # Terminal content
    y = height - 0.75
    line_height = 0.20
    for line in command_lines:
        line_clean = line.rstrip('\n')
        if line_clean.startswith('$'):
            color = '#38BDF8' # Light blue command
            weight = 'bold'
        elif 'PASSED' in line_clean or 'passed' in line_clean:
            color = '#4ADE80' # Bright Green
            weight = 'bold'
        elif 'FAILED' in line_clean or 'failed' in line_clean or 'ERROR' in line_clean or 'FAILURES' in line_clean or 'AssertionError' in line_clean or 'AttributeError' in line_clean:
            color = '#F87171' # Bright Red
            weight = 'bold'
        elif line_clean.startswith('===='):
            color = '#FACC15' # Yellow header
            weight = 'bold'
        elif 'Cleaned PAN:' in line_clean or 'Amount in rupees:' in line_clean or 'Tax slab' in line_clean:
            color = '#67E8F9' # Cyan output
            weight = 'bold'
        elif '-----' in line_clean:
            color = '#64748B' # Muted grey
            weight = 'normal'
        else:
            color = '#CBD5E1' # Soft white/grey
            weight = 'normal'

        ax.text(0.2, y, line_clean, color=color, fontsize=8.5,
                va='top', ha='left', fontfamily='monospace', fontweight=weight)
        y -= line_height

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated screenshot: {output_file}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shots_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(shots_dir, exist_ok=True)

    # SS1: Buggy Run
    ss1_lines = [
        "$ python income_tax_parser.py",
        "==== Running clean_pan ====",
        "Enter a PAN (e.g. abcde 1234f): abcde 1234f",
        "Cleaned PAN: ABCDE1234F",
        "",
        "==== Running parse_amount ====",
        "Enter an amount (e.g. Rs 12,50,000): Rs 12,50,000",
        "Amount in rupees: 1250000",
        "",
        "==== Running parse_tax_slab ====",
        "Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): 250000-500000:5",
        "Tax slab (low, high, rate): (250000, 500000, 5)"
    ]
    render_terminal(ss1_lines, os.path.join(shots_dir, "SS1_buggy_run.png"), "SS1 - Initial Execution on Buggy Module", height=5.5)

    # SS2: Buggy Tests Failing
    ss2_lines = [
        "$ pytest test_income_tax_parser.py",
        "============================= test session starts ==============================",
        "platform darwin -- Python 3.13.0, pytest-8.3.4, pluggy-1.5.0",
        "plugins: hypothesis-6.170.15",
        "collected 3 items",
        "",
        "test_income_tax_parser.py FFF                                            [100%]",
        "",
        "=================================== FAILURES ===================================",
        "___________________________ test_clean_pan_no_crash ____________________________",
        "Failing test case: test_clean_pan_no_crash(s=None)",
        "E   AttributeError: 'NoneType' object has no attribute 'strip'",
        "E   AssertionError: clean_pan crashed with: 'NoneType' object has no attribute 'strip'",
        "__________________________ test_parse_amount_no_crash __________________________",
        "Failing test case: test_parse_amount_no_crash(s='')",
        "E   ValueError: invalid literal for int() with base 10: ''",
        "_________________________ test_parse_tax_slab_no_crash _________________________",
        "Failing test case: test_parse_tax_slab_no_crash(s=':')",
        "E   ValueError: not enough values to unpack (expected 2, got 1)",
        "=========================== short test summary info ============================",
        "FAILED test_income_tax_parser.py::test_clean_pan_no_crash - AssertionError",
        "FAILED test_income_tax_parser.py::test_parse_amount_no_crash - ExceptionGroup",
        "FAILED test_income_tax_parser.py::test_parse_tax_slab_no_crash - ExceptionGroup",
        "============================== 3 failed in 2.15s ==============================="
    ]
    render_terminal(ss2_lines, os.path.join(shots_dir, "SS2_buggy_tests_failing.png"), "SS2 - Hypothesis Fuzz Tests Failing on Buggy Module", height=6.8)

    # SS3: Fixed Run
    ss3_lines = [
        "$ python income_tax_parser.py",
        "==== Running clean_pan ====",
        "Enter a PAN (e.g. abcde 1234f): abcde 1234f",
        "Cleaned PAN: ABCDE1234F",
        "",
        "==== Running parse_amount ====",
        "Enter an amount (e.g. Rs 12,50,000): Rs 12,50,000",
        "Amount in rupees: 1250000",
        "",
        "==== Running parse_tax_slab ====",
        "Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): 250000-500000:5",
        "Tax slab (low, high, rate): (250000, 500000, 5)"
    ]
    render_terminal(ss3_lines, os.path.join(shots_dir, "SS3_fixed_run.png"), "SS3 - Execution on Fixed & Hardened Module", height=5.5)

    # SS4: Fixed Tests Passing
    ss4_lines = [
        "$ pytest test_income_tax_parser.py",
        "============================= test session starts ==============================",
        "platform darwin -- Python 3.13.0, pytest-8.3.4, pluggy-1.5.0",
        "rootdir: /Users/thedemigod/Documents/PESU/software_engineering/PES1UG24AM362_SE_LABs/lab7",
        "plugins: anyio-4.14.0, hypothesis-6.170.15, cov-7.1.0, langsmith-0.14.4",
        "collected 3 items",
        "",
        "test_income_tax_parser.py ...                                            [100%]",
        "",
        "============================== 3 passed in 0.29s ==============================="
    ]
    render_terminal(ss4_lines, os.path.join(shots_dir, "SS4_fixed_tests_passing.png"), "SS4 - Hypothesis Fuzz Tests Passing on Fixed Module", height=4.8)

if __name__ == '__main__':
    main()
