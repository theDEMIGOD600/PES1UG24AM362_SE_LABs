"""Fixed and hardened income tax parser module.

Safely parses user-typed PAN numbers, monetary rupee amounts, and tax slab definitions
without crashing on malformed, unexpected, empty, or None inputs.
"""

import re


def clean_pan(pan):
    """
    Removes spaces from a PAN and converts it to upper-case.
    Safely handles None, non-string, and empty inputs without crashing.
    """
    if pan is None or not isinstance(pan, str):
        return ""
    return pan.strip().replace(" ", "").upper()


def parse_amount(text):
    """
    Converts an amount string such as 'Rs 12,50,000' or '₹ 50,000' into an integer.
    Safely handles None, non-strings, non-numeric characters, and empty inputs.
    Returns 0 if the input cannot be parsed into a valid integer.
    """
    if text is None or not isinstance(text, str):
        return 0
    try:
        # Remove common currency symbols and punctuation
        cleaned = text.replace("Rs", "").replace("rs", "").replace("₹", "").replace(",", "").strip()
        if not cleaned:
            return 0
        # Check if it represents an integer
        return int(cleaned)
    except (ValueError, TypeError, AttributeError):
        # Fallback to extracting digits if present
        digits = re.findall(r"-?\d+", text)
        if digits:
            try:
                return int("".join(digits))
            except ValueError:
                return 0
        return 0


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) integer tuple.
    Safely validates formatting, presence of delimiters, and integer conversions.
    Returns (0, 0, 0) if the input is malformed, missing, or invalid.
    """
    if line is None or not isinstance(line, str):
        return (0, 0, 0)
    try:
        if ":" not in line:
            return (0, 0, 0)
        parts = line.strip().split(":")
        if len(parts) != 2:
            return (0, 0, 0)
        limits, rate_str = parts[0].strip(), parts[1].strip()

        if "-" not in limits:
            return (0, 0, 0)
        lim_parts = limits.split("-")
        if len(lim_parts) != 2:
            return (0, 0, 0)
        low_str, high_str = lim_parts[0].strip(), lim_parts[1].strip()

        return int(low_str), int(high_str), int(rate_str)
    except (ValueError, TypeError, AttributeError):
        return (0, 0, 0)


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    print("Amount in rupees:", parse_amount(value))

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    print("Tax slab (low, high, rate):", parse_tax_slab(value))


if __name__ == "__main__":
    main()
