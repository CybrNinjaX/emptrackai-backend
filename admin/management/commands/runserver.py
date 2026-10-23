from django.core.management import call_command
from django.core.management.commands.runserver import Command as DjangoRunserverCommand


class Command(DjangoRunserverCommand):
    """Apply saved schema migrations before starting the development server."""

    def handle(self, *args, **options):
        call_command(
            'migrate',
            fake_initial=True,
            interactive=False,
            verbosity=options.get('verbosity', 1),
        )
        return super().handle(*args, **options)
