from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)
    
@register.filter
def modulo(num, val):
    return num % val
@register.filter

@register.filter
def is_in(num, val):
    return val in num
@register.filter

def isequal(num, val):
    return num == val

@register.filter
def suporequal(num, val):
    # print("num: ",num," val: ", val)
    return num >= val
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
@register.filter
def getlibelle(ch,val):
    return ch[val-1]['libelle']
@register.filter
def getid2(ch,val):
    return ch[val-1]['id']
@register.filter
def split0(ch):
    return ch.split("h")[0]
@register.filter
def split1(ch):
    return ch.split("h")[1]

@register.filter
def correct_format(ch):
    elt = ch.split("h");
    h = elt[0];
    m = elt[1];
    h_ = int(h);
    m_ = int(m);

    if (h_ < 10):
        h = "0"+ h +"h";
    else:
        h = h +"h";

    if (m_ < 10):
        h += "0"+m;
    else:
        h += m;
    return h;

