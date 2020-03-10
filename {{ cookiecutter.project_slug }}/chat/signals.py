from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chat


@receiver(post_save, sender=Chat)
def post_save_chat(sender, instance, created, **kwargs):
    if created:
        instance.members.add(instance.admin)
