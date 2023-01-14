from django import template

register = template.Library()


@register.filter(name="update_variable")
def update_variable(value):
    print(value)
    value = 0
    return value
    
