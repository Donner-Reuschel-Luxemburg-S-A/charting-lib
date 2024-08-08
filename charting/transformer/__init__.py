import pandas as pd
from pandas import DateOffset


def _generate_label(offset: DateOffset, action: str, language: str) -> str:
    """
    Generates a label for the specified window and action.

    Args:
        offset (pd.DateOffset): The offset indicating the time window.
        action (str): The action performed on the time window.

    Returns:
        str: The generated label.
    """
    if language == 'en':
        units = {
            "years": "Y",
            "months": "M",
            "weeks": "W",
            "days": "D",
            "hours": "H",
            "minutes": "M",
            "seconds": "S"
        }
    elif language == 'de':
        units = {
            "years": "J",
            "months": "M",
            "weeks": "W",
            "days": "T",
            "hours": "S",
            "minutes": "M",
            "seconds": "Sek"
        }

    priority_order = ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]
    parts = []
    for component in priority_order:
        if component in offset.kwds:
            value = offset.kwds[component]
            unit = units[component]
            label = f"{value}{unit}"
            parts.append(label)

    label = ' '.join(parts)

    return f"{label} {action}"
