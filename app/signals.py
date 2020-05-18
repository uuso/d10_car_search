from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Car

@receiver(pre_save, sender=Car)
def check_color(sender, **kwargs):
    pass
    # if kwargs['instance'].color > 0xFFFFFF:
    #     kwargs['instance'].color = 0xFFFFFF    