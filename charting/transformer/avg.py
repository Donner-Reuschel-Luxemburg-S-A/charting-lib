import datetime
import arrow

from pandas import Series

from charting.transformer.transformer import Transformer


class Avg(Transformer):
    def __init__(self, window: datetime.timedelta):
        super().__init__()
        self.window = window

    def transform(self, x: Series, y: Series) -> (Series, Series):
        window = int(self.window.total_seconds() / (60 * 60 * 24))
        return x, y.rolling(window=window).mean()

    def label(self) -> str:
        total_seconds = int(self.window.total_seconds())
        weeks, remainder = divmod(total_seconds, 7 * 24 * 60 * 60)
        days, remainder = divmod(remainder, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if weeks > 0:
            parts.append(f"{weeks} {'week' if weeks == 1 else 'weeks'}")
        if days > 0:
            parts.append(f"{days} {'day' if days == 1 else 'days'}")
        if hours > 0:
            parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        if minutes > 0:
            parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        if seconds > 0:
            parts.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")

        label = ' '.join(parts)

        return f"{label} avg"
