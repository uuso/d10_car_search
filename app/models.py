from django.db import models
from random import randint
from .colors import color_palette, rgb_to_web, nearest

# def random_color():
#     return randint(0,0xFFFFFF)


class Car(models.Model):
    vendor = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.SmallIntegerField()
    GEARBOX = (
        (0, "механика"),
        (1, "автомат"),
        (2, "робот"),
    )
    gearbox = models.SmallIntegerField(choices=GEARBOX, default=0)
    # color = models.PositiveIntegerField(default=random_color)
    color = models.CharField(max_length=20, default=tuple(color_palette)[0])

    def web_color(self):
        return rgb_to_web(self.color)

    # def nearest_color(self):
    #     return nearest(self.color)['color']['name']