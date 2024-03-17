from django.db import models
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from django.utils import formats

from User.models import User, Bemor


class Tashxis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='uchirilgan user', related_name='tashxis_user')
    bemor = models.ForeignKey(Bemor, on_delete=models.SET_DEFAULT, default='uchirilgan bemor', related_name='tashxis_user')
    diagnoz = models.TextField(null=True, blank=True)
    tashxis = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    narx = models.PositiveIntegerField(default=0)
    tuladi = models.PositiveIntegerField(default=0)
    qoldi = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.diagnoz}/{self.narx}'

# @receiver(post_save, sender=Tashxis)
# def create_payment(sender, instance, created=False, **kwargs):
#     if created:
#         instance.qoldi = instance.narx - instance.tuladi
#         instance.save()