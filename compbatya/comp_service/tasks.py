from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task



@shared_task
def send_mail_to_managers(phone: str, name: str,
                          client_mail: str = None) -> None:
    Users = get_user_model()
    emails = Users.objects.filter(is_staff=True, is_superuser=False).values_list('email')
    emails = [i[0] for i in emails if i[0]]
    msg_text = f"Новая заявка!!!\n\nТелефон: {phone}\nКак обращаться: {name}\n" \
        f"E-mail: {client_mail if client_mail else '-'}"
        
    send_mail(
        subject='Заявка на ремонт',
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=msg_text,
        recipient_list=emails,
        fail_silently=False,
    )