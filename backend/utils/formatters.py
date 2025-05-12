def format_price(price):
    """
    Format price with a dollar sign and 2 decimal places.

    Args:
        price (float): Price value.

    Returns:
        str: Formatted price, or "N/A" if invalid.
    """
    return f"${price:.2f}" if price is not None else "N/A"


def format_pe_ratio(pe_ratio):
    """
    Format P/E ratio with 2 decimal places.

    Args:
        pe_ratio (float): P/E ratio value.

    Returns:
        str: Formatted P/E ratio, or "N/A" if invalid.
    """
    return f"{pe_ratio:.2f}" if pe_ratio is not None else "N/A"


def format_number(num):
    """
    Format large numbers with commas and a dollar sign.

    Args:
        num (int or float): Number to format.

    Returns:
        str: Formatted number, or "N/A" if invalid.
    """
    return f"${num:,}" if num else "N/A"