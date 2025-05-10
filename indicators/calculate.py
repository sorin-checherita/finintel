def calculate_ebitda_percentage(ebitda, revenue):
    """
    Calculate EBITDA as a percentage of revenue.

    Args:
        ebitda (float): EBITDA value.
        revenue (float): Revenue value.

    Returns:
        str: EBITDA percentage formatted as a string with 2 decimal places, or "N/A" if invalid.
    """
    if not ebitda or not revenue:
        return "N/A"
    percentage = (ebitda / revenue) * 100
    return f"{percentage:.2f}%"