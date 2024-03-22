from django import template
from django.utils.safestring import mark_safe

from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context["request"]
    active_url = request.path
    three = MenuItem.get_entity_parents(menu_name, active_url)

    def render_menu(menu_node):
        menu_html = "<ul>"
        active_class = "active" if active_url == menu_node.url else ""
        menu_html += f"<li>"
        menu_html += (
            f'<a href="{menu_node.url}" class="{active_class}">{menu_node.title}</a>'
        )
        children = [child for child in three if child.parent_id == menu_node.id]
        if children:
            for child in children:
                menu_html += render_menu(child)
        menu_html += "</li></ul>"
        return menu_html

    if three:
        menu_html = render_menu(three[0])
        return mark_safe(menu_html)
    return ""
