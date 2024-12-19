from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from robots.models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def notify_customers_about_robot(sender, instance, created, **kwargs):
    if not created:
        return

    pending_orders = Order.objects.filter(
        robot_serial=f'{instance.model}-{instance.version}',
    ).select_related('customer')

    for order in pending_orders:
        send_mail(
            subject='Робот доступен',
            message=f'''Добрый день!
Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
        )
