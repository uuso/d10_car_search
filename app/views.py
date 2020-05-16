from django.db.models import Q, Max, Min
from django.shortcuts import render
from django.views.generic import ListView
from .models import Car
from .colors import color_palette, rgb_to_web

# функция для отображения django_debug_toolbox у всех
def truefunc(*args, **kwargs): return True



class CarsList(ListView):
    # model = Car
    paginate_by=20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # список кнопок управления паджинацией
        current_page = context['page_obj'].number
        total_pages = context['paginator'].num_pages
        nearest = 2

        context['page_list'] = [x for x in range(
            current_page-nearest, current_page+nearest+1) if x > 0 and x <= total_pages]

        # список производителей авто и разброс лет для работы с формами        
        # context['vendor_list'] = Car.objects.values_list('vendor', flat=True).distinct().order_by('vendor')
        
        # в таком виде работает в 3 раза быстрее:
        all_the_cars = Car.objects.values_list('vendor', 'year', named=True)
        context['vendor_list'] = sorted(set([x.vendor for x in all_the_cars]))

        # список доступных цветов для фильтрации списка
        context['colors'] = [{'name': key, 'web': rgb_to_web(value)} for key, value in color_palette.items()]
        return context

    def get_queryset(self, **kwargs):        
        output = Car.objects.all()


        # с Q показывает то же время, всё равно лишний запрос во время работы встроенного паджинатора
        # оставил лишь с целью "в задании же было"
        # не знаю, как делать запросы с Q, не проверяя заранее наличия GET-параметра
        # то есть, мне нужно добавить или удалить выражение с Q в зависимости от наличия параметра в GET запросе
        # думал, что если можно в Q передать какой-нибудь None чтобы он не модифицировал выход, то
        # можно будет написать что-то вроде .filter(Q('vendor' in self.request.GET if ... else None ))
        # или типа такого пробовал, но это шлак
        # Car.objects.filter(Q(
        #   eval("vendor__exact='Aptera'") if True 
        #   else eval("vendor__exact='Bugatti'")
        # )).values_list('vendor', 'model')

        # если знаете и есть желание поделиться - чирканите @ualexey в телеграм
        if all([
            'vendor' in self.request.GET, 
            'model' in self.request.GET,
            'year' in self.request.GET and self.request.GET['year'],
            'gearbox' in self.request.GET,
            not 'color' in self.request.GET]):
            
            output = output.filter(
                Q(vendor__in=self.request.GET.getlist('vendor')) &
                Q(model__contains=self.request.GET.get('model')) &
                Q(year__in=self.request.GET.get('year').split(',')) &
                Q(gearbox__in=self.request.GET.getlist('gearbox'))
            )



        else:
            if 'vendor' in self.request.GET:
                output = output.filter(vendor__in=self.request.GET.getlist('vendor'))
            if 'model' in self.request.GET:
                output = output.filter(model__contains=self.request.GET.get('model'))
            if 'year' in self.request.GET and self.request.GET['year']:                
                output = output.filter(year__in=self.request.GET.get('year').split(','))
            if 'gearbox' in self.request.GET:
                output = output.filter(gearbox__in=self.request.GET.getlist('gearbox'))
            if 'color' in self.request.GET:
                # нельзя применять ORM для самописных методов модели
                # output = output.filter(nearest_color__in=self.request.GET.getlist('color'))
                color_filter = [ item.id for item in output \
                    if item.nearest_color() in self.request.GET.getlist('color')]                
                output = output.filter(id__in=color_filter)
        
        return output
