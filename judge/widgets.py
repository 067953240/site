from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldError


class CheckboxSelectMultipleWithSelectAll(forms.CheckboxSelectMultiple):
    _all_selected = False

    def render(self, *args, **kwargs):
        empty = False
        if not self.choices:
            empty = True
        has_id = kwargs and ('attrs' in kwargs) and ('id' in kwargs['attrs'])
        if not has_id:
            raise FieldError('id required')
        select_all_id = kwargs['attrs']['id'] + '_all'
        select_all_name = args[0] + '_all'
        renderer = super(CheckboxSelectMultipleWithSelectAll, self).get_renderer(*args, **kwargs)
        template = get_template('widgets/select_all.jade')
        context = Context({'original_widget': renderer.render(),
                           'select_all_id': select_all_id,
                           'select_all_name': select_all_name,
                           'all_selected': all(choice[0] in renderer.value for choice in renderer.choices),
                           'empty': empty})
        return mark_safe(template.render(context))

    def value_from_datadict(self, *args, **kwargs):
        original = super(CheckboxSelectMultipleWithSelectAll, self).value_from_datadict(*args, **kwargs)
        select_all_name = args[2] + '_all'
        if select_all_name in args[0]:
            self._all_selected = True
        else:
            self._all_selected = False
        return original

try:
    from pagedown.widgets import PagedownWidget, AdminPagedownWidget
except ImportError:
    PagedownWidget = None
    AdminPagedownWidget = None
    MathJaxPagedownWidget = None
    MathJaxAdminPagedownWidget = None
else:
    class MathJaxPagedownWidget(PagedownWidget):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('css', (staticfiles_storage.url('pagedown_widget.css'),))
            self._load_math = kwargs.pop('load_math', True)
            super(MathJaxPagedownWidget, self).__init__(*args, **kwargs)

        def _media(self):
            media = super(MathJaxPagedownWidget, self)._media()
            if self._load_math:
                media.add_js([
                    staticfiles_storage.url('mathjax_config.js'),
                    '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
                    staticfiles_storage.url('pagedown_math.js'),
                ])
            return media
        media = property(_media)

    class MathJaxAdminPagedownWidget(MathJaxPagedownWidget, admin_widgets.AdminTextareaWidget):
        def _media(self):
            media = super(MathJaxAdminPagedownWidget, self)._media()
            media.add_css({'all': [
                staticfiles_storage.url('content-description.css'),
                staticfiles_storage.url('admin/css/pagedown.css'),
            ]})
            media.add_js([staticfiles_storage.url('admin/js/pagedown.js')])
            return media
        media = property(_media)