from django import template

register = template.Library()

def ellipsis_line(value, arg):
    lines = value.splitlines()
    if len(lines) > arg:
        return '\n'.join(lines[:arg+1] + ['...'])
    return value