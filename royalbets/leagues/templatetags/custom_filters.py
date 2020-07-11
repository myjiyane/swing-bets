# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='map')
@stringfilter
def map(val):
    con_val = ''

    if val == 'PEND':
     con_val = 'Pending'
    elif val == 'CORR':
     con_val = 'Correct'
    elif val == 'INCO':
     con_val = 'Incorrect'
    elif val == 'CANC':
     con_val = 'Cancelled'
    elif val =='NRES':
     con_val = 'No results'
    elif val == None:
     con_val = '' 
    else:
     con_val = val
    return con_val


@register.filter
@stringfilter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'

    return 'form-control {}'.format(css_class)


@register.filter
@stringfilter    
def disable_field(val, arg):
    css_field = 'enabled'
    
    if val == arg:
        css_field = 'disabled'
     
    return css_field