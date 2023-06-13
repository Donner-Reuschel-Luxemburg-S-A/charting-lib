import datetime

def _generate_label(window: datetime.timedelta, action: str) -> str:
    """
    Generates a label for the specified window and action.

    Args:
        window (datetime.timedelta): The timedelta indicating the time window.
        action (str): The action performed on the time window.

    Returns:
        str: The generated label.

    Example:
        >>> _generate_label(datetime.timedelta(days=7), 'lag')
        '1 week lag'
        >>> _generate_label(datetime.timedelta(hours=2, minutes=30), 'lead')
        '2 hours 30 minutes lead'
    """
    total_seconds = int(window.total_seconds())
    weeks, remainder = divmod(total_seconds, 7 * 24 * 60 * 60)
    days, remainder = divmod(remainder, 24 * 60 * 60)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)

    years = window.days // 365
    months = (window.days % 365) // 30
    remaining_weeks = weeks - (months * 4)

    parts = []
    if years > 0:
        parts.append(f"{years} {'y' if years == 1 else 'y'}")
    if months > 0:
        parts.append(f"{months} {'m' if months == 1 else 'm'}")
    if remaining_weeks > 0:
        parts.append(f"{remaining_weeks} {'w' if remaining_weeks == 1 else 'w'}")
    if days > 0:
        parts.append(f"{days} {'d' if days == 1 else 'd'}")
    if hours > 0:
        parts.append(f"{hours} {'hrs' if hours == 1 else 'hrs'}")
    if minutes > 0:
        parts.append(f"{minutes} {'min' if minutes == 1 else 'min'}")
    if seconds > 0:
        parts.append(f"{seconds} {'sec' if seconds == 1 else 'sec'}")

    label = ' '.join(parts)

    return f"{label} {action}"
