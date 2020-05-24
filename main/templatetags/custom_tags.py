from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def check(arg):
    return arg or "Не указано"
