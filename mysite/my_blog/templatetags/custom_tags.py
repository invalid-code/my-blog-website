from django import template

register = template.Library()

@register.simple_tag
def mongo_id(tag_name):
    return tag_name["_id"]