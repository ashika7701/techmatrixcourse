# your_app/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return the value from dictionary for the given key, or None if not found."""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None
