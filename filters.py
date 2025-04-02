from datetime import datetime, timedelta
from markupsafe import Markup

def time_ago(timestamp):
    """Return a string representing how long ago a timestamp was."""
    if not timestamp:
        return "Unknown time"
    
    now = datetime.utcnow()
    diff = now - timestamp

    if diff < timedelta(seconds=60):
        return "Just now"
    elif diff < timedelta(minutes=60):
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif diff < timedelta(hours=24):
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = diff.days
        return f"{days} day{'s' if days > 1 else ''} ago"
