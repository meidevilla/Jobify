import datetime
from django import template
from django.utils.timezone import now

register = template.Library()
@register.filter
def relative_date(value):
    if not value:
        return "Unknown date"
    today = now().date()
    delta = today - value.date()

    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Yesterday"
    elif delta.days > 1:
        return f"{delta.days} days ago"
    return value.strftime("%d %b %Y")
