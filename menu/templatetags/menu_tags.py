from django import template
from django.urls import reverse
from ..models import MenuItem

register = template.Library()

# Создаем пользовательский тег для отображения меню
@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    # Получаем все элементы меню по имени
    menu_items = MenuItem.objects.filter(menu_name=menu_name)

    # Создаем словарь элементов меню
    menu_items_dict = {}
    # Создаем список корневых элементов
    root_items = []

    # Проходим по всем элементам меню
    for item in menu_items:
        # Добавляем элемент в словарь
        menu_items_dict[item.id] = {"name": item.name, "url": item.url, "children": []}
        # Если элемент не имеет родительского элемента, то добавляем его в список корневых элементов
        if not item.parent_id:
            root_items.append(item.id)
        # Иначе добавляем его в список дочерних элементов родительского элемента
        else:
            menu_items_dict[item.parent_id]["children"].append(item.id)

    # Создаем строку HTML кода для меню
    menu_html = "<ul>"
    # Проходим по всем корневым элементам
    for item_id in root_items:
        # Добавляем HTML код элемента в меню
        menu_html += render_menu_item(item_id, menu_items_dict, context)
    menu_html += "</ul>"

    # Возвращаем HTML код меню
    return menu_html

# Функция для рендеринга элемента меню
def render_menu_item(item_id, menu_items_dict, context):
    # Получаем информацию о элементе меню
    item = menu_items_dict[item_id]
    # Получаем ссылку на элемент меню
    url = item["url"]
    # Если ссылка не начинается со знака "/", то создаем ее с помощью reverse
    if not url.startswith("/"):
        url = reverse(url)
    # Получаем текущий путь страницы
    current_path = context['request'].path
    # Проверяем, является ли элемент меню активным
    active = current_path.startswith(url)
    # Создаем HTML код элемента меню
    menu_html = f'<li class="{ "active" if active else "" }"><a href="{url}">{item["name"]}</a>'
    # Если элемент имеет дочерние элементы, то добавляем их в меню
    if item["children"]:
        menu_html += '<ul>'
        for child_id in item["children"]:
            menu_html += render_menu_item(child_id, menu_items_dict, context)
        menu_html += '</ul>'
    menu_html += '</li>'
    # Возвращаем HTML код элемента меню
    return menu_html
