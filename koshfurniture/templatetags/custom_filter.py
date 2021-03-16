from django import template

register = template.Library()

@register.filter(name="currency")
def currency(number):
    return "₹ " + str(number)
    
@register.filter(name="multiply")
def multiply(number,number1):
    return number * number1

@register.filter(name="length_check")
def length_check(products):
    if len(products) <= 0:
        return False
    else:
        return True