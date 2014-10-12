from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Problem, Contest


@receiver(post_save, sender=Problem)
def problem_update(sender, instance, **kwargs):
    cache.delete(make_template_fragment_key('problem_html', (instance.id,)))


@receiver(post_save, sender=Contest)
def problem_update(sender, instance, **kwargs):
    cache.delete(make_template_fragment_key('contest_html', (instance.id,)))
