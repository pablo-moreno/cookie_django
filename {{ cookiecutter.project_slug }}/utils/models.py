from django.db import models
from django.utils.timezone import now


class TimestampedModel(models.Model):
    creation_date = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.updated = now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class SoftDeleteableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)


class SoftDeleteableModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = SoftDeleteableManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True
