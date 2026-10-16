import ast
import json
import operator
import os
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _safe_eval(node, variables):
    """Safely evaluate basic arithmetic expressions."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](
                _safe_eval(node.left, variables),
                _safe_eval(node.right, variables)
            )
        raise ValueError(f"Unsupported operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](_safe_eval(node.operand, variables))
        raise ValueError(f"Unsupported unary operator: {op_type}")
    raise ValueError(f"Unsupported AST node: {type(node)}")


def add_book_loan(student_id, book_id, dates=[]):
    if not student_id:
        return
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print("%s borrowed %s (loan dates on record: %d)" % (student_id, book_id, len(dates)))


def return_book(student_id, book_id):
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        pass


def calculate_fine(days_overdue):
    return days_overdue * FINE_PER_DAY


def renewBook(student_id, book_id, extra_days):
    global FINE_PER_DAY
    if extra_days > 14:
        FINE_PER_DAY = FINE_PER_DAY + 1
    print("Renewed " + book_id + " for " + student_id + " by " + str(extra_days) + " days")


def load_records(file="loans.json"):
    f = open(file, "r")
    global loans
    loans = json.loads(f.read())
    f.close()


def save_records(file="loans.json"):
    f = open(file, "w")
    f.write(json.dumps(loans))
    f.close()


def fine_from_rule(rule, days):
    parsed = ast.parse(rule, mode='eval')
    return int(_safe_eval(parsed.body, {"days": days}))


def print_report():
    print("Loan Report")
    for s in loans:
        print(s, "->", loans[s])


def main():
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renewBook("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()


main()
