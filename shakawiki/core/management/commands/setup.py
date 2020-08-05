from django.core.management.base import BaseCommand
from django.conf import settings
import os
import secrets

class Command(BaseCommand):
  help = """setup shakawiki
"""

  def handle(self, *args, **options):
    envfile = os.path.join(settings.BASE_DIR, '.env')
    with open(envfile, 'w') as f:
      f.write('DJANGO_SECRET={}'.format(secrets.token_urlsafe(nbytes=64)))
    self.stdout.write(self.style.SUCCESS('generated'))
