from django import template

register = template.Library()

@register.filter # 필터로 등록
def sub(value, arg):
    return value - arg
