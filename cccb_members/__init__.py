from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'cccb_members'
    verbose_name = 'CCCB Members'

    class ByroPluginMeta:
        name = ugettext_lazy('CCCB Members')
        author = 'Matthias'
        description = ugettext_lazy('Membership extensions for byro')
        visible = True
        version = '0.0.1'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'cccb_members.PluginApp'
