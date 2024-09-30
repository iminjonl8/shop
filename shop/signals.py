from django.conf import settings
from django.dispatch import receiver 
from django.db.models.signals import post_save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_post_save(created, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f'polzovatel {instance.username} bil sozdon.')
    else:
        print(f'polzovatel {instance.username} bil obnovlenya')