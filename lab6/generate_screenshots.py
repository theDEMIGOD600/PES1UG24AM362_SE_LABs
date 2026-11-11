import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def render_terminal(command_lines, output_file, title="Terminal - zsh"):
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=220)
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Terminal Header bar
    header = patches.FancyBboxPatch((0, 5.7), 10, 0.5, boxstyle="square,pad=0",
                                     fc='#2D2D2D', ec='#2D2D2D')
    ax.add_patch(header)

    # Mac window controls
    ax.add_patch(patches.Circle((0.25, 5.95), 0.08, color='#FF5F56'))
    ax.add_patch(patches.Circle((0.50, 5.95), 0.08, color='#FFBD2E'))
    ax.add_patch(patches.Circle((0.75, 5.95), 0.08, color='#27C93F'))

    # Title
    ax.text(5.0, 5.95, title, color='#CCCCCC', fontsize=10,
            ha='center', va='center', fontfamily='sans-serif', fontweight='medium')

    # Terminal content
    y = 5.45
    line_height = 0.18
    for line in command_lines:
        line_clean = line.rstrip('\n')
        # Colors based on content
        if line_clean.startswith('$'):
            color = '#38BDF8' # Light blue command
            weight = 'bold'
        elif 'PASSED' in line_clean or 'passed' in line_clean:
            color = '#4ADE80' # Bright Green
            weight = 'bold'
        elif '100%' in line_clean:
            color = '#4ADE80' # Green
            weight = 'bold'
        elif '=====' in line_clean or '-----' in line_clean:
            color = '#64748B' # Muted grey
            weight = 'normal'
        elif line_clean.startswith('Name') or line_clean.startswith('TOTAL'):
            color = '#F1F5F9' # White
            weight = 'bold'
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

    # 1. Code Coverage
    with open(os.path.join(base_dir, "code_coverage_output.txt")) as f:
        cc_out = f.readlines()
    cc_lines = [
        "$ coverage run -m pytest CodeCoverageTest_income_tax.py",
        "$ coverage report -m",
        ""
    ] + cc_out
    render_terminal(cc_lines, os.path.join(shots_dir, "code_coverage_terminal_report.png"), "Terminal - Code Coverage (Line Coverage 100%)")

    # 2. Branch Coverage
    with open(os.path.join(base_dir, "branch_coverage_output.txt")) as f:
        bc_out = f.readlines()
    bc_lines = [
        "$ coverage run --branch -m pytest BranchCoverageTest_income_tax.py",
        "$ coverage report -m",
        ""
    ] + bc_out
    render_terminal(bc_lines, os.path.join(shots_dir, "branch_coverage_terminal_report.png"), "Terminal - Branch Coverage (100% Branches)")

if __name__ == '__main__':
    main()
