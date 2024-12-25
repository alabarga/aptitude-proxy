from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def log(value):
    for i in value:
        print(i.field.bloque)
    return value


@register.filter
def bloques(value):
    bloques = list(dict.fromkeys([i.field.bloque for i in value]))
    if 'Auditivo' in bloques:
        bloques.remove('Auditivo')  # Remove 'Auditivo' from its current position
        bloques.append('Auditivo')  # Append it to the end of the list

    return bloques

@register.filter
def bloque(value, nombre):
    return [i for i in value if i.field.bloque == nombre]
