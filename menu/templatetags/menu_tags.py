from django import template
from ..models import MenuItem

register = template.Library()

class Menu:
    def __init__(self, menu_name):
        self.menu_name = menu_name
        self.items = MenuItem.objects.filter(menu_name=menu_name)

    def render(self, context):
        menu_html = "<ul>"
        for item in self.items:
            menu_html += self.render_menu_item(item, context)
        menu_html += "</ul>"
        return menu_html

    def render_menu_item(self, item, context):
        url = item.url
        if not url.startswith("/"):
            url = reverse(url)

        current_path = context['request'].path
        active = current_path.startswith(url)

        menu_html = f'<li class="{ "active" if active else "" }"><a href="{url}">{item.name}</a>'

        if item.children.exists():
            menu_html += '<ul>'
            for child in item.children.all():
                menu_html += self.render_menu_item(child, context)
            menu_html += '</ul>'

        menu_html += '</li>'
        return menu_html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu = Menu(menu_name)
    return menu.render(context)
