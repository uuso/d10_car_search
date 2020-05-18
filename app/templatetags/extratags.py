import urllib
from django import template
from app.colors import nearest, rgb_to_web, color_palette

register = template.Library()

# <a href="?{% url_replace page=paginator.next_page_number %}">
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()

    # проблемки с обновлением данных:
        # QueryDict.update() может только дополнить список новым элементом:
        #   косяк при переходе на другую страницу, дублирует ключи в запросе
        #   решил использованием urllib.parse.urlencode(QueryDict) хз, все равно что-то не то
        #   теперь при работе с несколькими параметрами запроса она оставляет только один

        # короче, чтобы заменить значение внутри QueryDict, нужно сначала его удалить, а затем установить новое по ключу
        # а потом использовать QueryDict.urlencode() т.к. именно он корректно отрабатывает задвоенные get-параметры:
        # urllib.parse.urlencode(QueryDict) при {'vendor': ['Cadillac', 'BMW'] ...} получит только 'BMW'

    if 'page' in kwargs and 'page' in query:
        query.pop('page')
        
    query.update(kwargs)

    return query.urlencode()

@register.simple_tag(takes_context=True)
def mark_selected(context, **kwargs):
    query = context['request'].GET
    # import q; q.d()
    for key, value in kwargs.items():        
        if key in query and value in query.getlist(key):
            return 'selected'

# @register.filter
# def nearest_color(color):
#     return nearest(color)['color']['web']

@register.filter
def name_to_web(color):
    return rgb_to_web(color_palette[color])

@register.filter
def web_color(color):
    return rgb_to_web(color)