from django.db.models import Q, Max, Min
from django.shortcuts import render
from django.views.generic import ListView
from .models import Car
from .colors import color_palette, rgb_to_web

# функция для отображения django_debug_toolbox у всех
def truefunc(*args, **kwargs): return True



class CarsList(ListView):
    # model = Car
    paginate_by=15

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

        query = Q()
        for key, value in dict(self.request.GET).items():
            if value != ['',] and key in vars(Car):
                if key == 'model':
                    query &= Q(**{f'{key}__contains': value[0]})
                elif key =='year':
                    query &=Q(**{f'{key}__in': [x for x in value[0].split(',') if str(x).isdigit()]})
                else:
                    query &= Q(**{f'{key}__in': value})

        return output.filter(query).order_by('id')

        # if all([
        #     'vendor' in self.request.GET, 
        #     'model' in self.request.GET,
        #     'year' in self.request.GET and self.request.GET['year'],
        #     'gearbox' in self.request.GET,
        #     not 'color' in self.request.GET]):
            
        #     output = output.filter(
        #         Q(vendor__in=self.request.GET.getlist('vendor')) &
        #         Q(model__contains=self.request.GET.get('model')) &
        #         Q(year__in=self.request.GET.get('year').split(',')) &
        #         Q(gearbox__in=self.request.GET.getlist('gearbox'))
        #     )



        # else:
        #     if 'vendor' in self.request.GET:
        #         output = output.filter(vendor__in=self.request.GET.getlist('vendor'))
        #     if 'model' in self.request.GET:
        #         output = output.filter(model__contains=self.request.GET.get('model'))
        #     if 'year' in self.request.GET and self.request.GET['year']:                
        #         output = output.filter(year__in=self.request.GET.get('year').split(','))
        #     if 'gearbox' in self.request.GET:
        #         output = output.filter(gearbox__in=self.request.GET.getlist('gearbox'))
        #     if 'color' in self.request.GET:
        #         # нельзя применять ORM для самописных методов модели
        #         # output = output.filter(nearest_color__in=self.request.GET.getlist('color'))
        #         color_filter = [ item.id for item in output \
        #             if item.nearest_color() in self.request.GET.getlist('color')]                
        #         output = output.filter(id__in=color_filter)
        
        # return output
