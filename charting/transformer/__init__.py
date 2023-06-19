import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DateOffset


def _generate_label(offset: DateOffset, action: str) -> str:
    """
    Generates a label for the specified window and action.

    Args:
        offset (pd.DateOffset): The offset indicating the time window.
        action (str): The action performed on the time window.

    Returns:
        str: The generated label.
    """
    priority_order = ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]
    parts = []
    for component in priority_order:
        if component in offset.kwds:
            value = offset.kwds[component]
            label = f"{value} {'y' if value == 1 else component[0]}"
            parts.append(label)

    label = ' '.join(parts)

    return f"{label} {action}"
