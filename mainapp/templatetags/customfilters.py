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
def isequal2(num, val):
    if num == "":
        return True
    n = str(num.score)
    return float(n) == float(val)

@register.filter
def suporequal(num, val):
    print("num: ",num," val: ", val)
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
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val]
@register.filter
def getcharplus1(ch, val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val]+1
@register.filter
def getchar2(ch, val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1]
@register.filter
def isIn(val):
    return val in '1234567890'
@register.filter
def char(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1][0]
@register.filter
def char2(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1][1]
@register.filter
def unzip1(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1][0]
@register.filter
def unzip2(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1][1]
@register.filter
def unzip3(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1][2]
@register.filter
def getid(ch):
    return ch.id
@register.filter
def getlibelle(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1]['libelle']
@register.filter
def getid2(ch,val):
    if len(ch) == 0 or val >= len(ch):
        return ""
    else:
        return ch[val-1]['id']
@register.filter
def split0(ch):
    nb = len(ch.split("h"))
    if nb > 1:
        k = 0
        return ch.split("h")[0]
    else:
        k = 1
        return ""

@register.filter
def split1(ch):
    nb = len(ch.split("h"));
    if nb > 1:
        return ch.split("h")[1]
    else:
        return ""

@register.filter
def correct_format(ch):
    nb = len(ch.split("h"));
    h= ""
    if nb > 1:
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

@register.filter
def islower(num, val):
    return num < val

@register.filter
def in_list(ch, val):
    if len(ch) == 0 or val >= len(ch):
        return False
    else:
        return str(val) in ch[0]
@register.filter
def add_nombre(n, val):
    print(n)
    return n+val

@register.filter
def float_format(n):
    nbre = n.score
    i = int(nbre)
    
    if nbre - i == 0:
        return i
    else:
       return float("{0:.2f}".format(nbre))

@register.filter
def float_format2(n):
    i = int(n)
    
    if n - i == 0:
        return i
    else:
       return float("{0:.2f}".format(n))
