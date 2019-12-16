from django import template

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val
@register.filter
def isequal(num, val):
    return num == val

@register.filter
def divide(value, arg):
    try:
        return int(value/ arg)
    except (ValueError, ZeroDivisionError):
        return None
@register.filter
def minus(num, val):
    return num - val
@register.filter
def getchar(ch, val):
    return ch[val]
@register.filter
def getchar2(ch, val):
    return ch[val-1]
@register.filter
def isIn(val):
    return val in '1234567890'
@register.filter
def char(ch,val):
    return ch[val-1][0]
@register.filter
def char2(ch,val):
    return ch[val-1][1]
@register.filter
def unzip1(ch,val):
    return ch[val-1][0]
@register.filter
def unzip2(ch,val):
    return ch[val-1][1]
@register.filter
def unzip3(ch,val):
    return ch[val-1][2]
@register.filter
def getid(ch):
    return ch.id
