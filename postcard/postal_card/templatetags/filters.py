from django import template

register = template.Library()

digits_map = {
    "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴",
    "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹",
}

@register.filter
def to_persian(value):
    return ''.join(digits_map.get(ch, ch) for ch in str(value))
