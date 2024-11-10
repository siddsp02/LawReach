from datetime import datetime, timezone


def time_diff(date: datetime) -> str:
    now = datetime.now()
    diff = now - date
    secs = diff.total_seconds()
    if secs < 60:
        return "just now"
    elif secs < 3600:
        minutes = int(secs // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif secs < 86400:
        hours = int(secs // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif secs < 2592000:
        days = int(secs // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif secs < 31536000:
        months = int(secs // 2592000)
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = int(secs // 31536000)
        return f"{years} year{'s' if years > 1 else ''} ago"
