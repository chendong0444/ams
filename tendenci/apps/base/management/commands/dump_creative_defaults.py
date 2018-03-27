from __future__ import print_function
import os
from optparse import make_option
from random import randint
from boto.s3.connection import S3Connection

from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Dump default data"

    option_list = BaseCommand.option_list + (
        make_option('--reset-nav',
            action="store_true", dest='reset_nav', default=False,
            help='Reset the navigation'),
    )

    def handle(self, **options):
        """
        Load data and from non profit fixtures
        and download images from s3 location.
        """
        reset_nav = options.get('reset_nav', None)
        self.number_used = []

        self.call_dumpdata(reset_nav)

    # def copy_files(self):
    #     """
    #     Copy files from default S3 location
    #     into websites S3 or local directory.
    #     """
    #     if settings.USE_S3_STORAGE:
    #         self.copy_to_s3()
    #     else:
    #         self.copy_to_local()

    def call_dumpdata(self, reset_nav=False):
        """
        This calls the dumpdata command on all creative fixtures.
        """
        from tendenci.apps.files.models import File

        if reset_nav:
            from tendenci.apps.navs.models import NavItem
            try:
                main_nav_items = NavItem.objects.filter(nav_id=1)
                main_nav_items.delete()
            except:
                pass

        path = os.path.join(settings.TENDENCI_ROOT, 'apps') + '/%s/fixtures/%s'
        print(path)
        print('creative_default_auth_user.json')
        call_command('dumpdata', 'auth.user', output=path % ('profiles', 'creative_default_auth_user.json'), indent=4)
        print('creative_default_auth_groups.json')
        call_command('dumpdata', 'auth.group', output=path % ('user_groups', 'creative_default_auth_groups.json'), indent=4)
        print('creative_default_entities.json')
        call_command('dumpdata', 'entities.entity', output=path % ('entities', 'creative_default_entities.json'), indent=4)
        print('creative_default_user_groups.json')
        call_command('dumpdata', 'user_groups', output=path % ('user_groups', 'creative_default_user_groups.json'), indent=4)
        print('creative_default_files.json')
        call_command('dumpdata', 'files.file', output=path % ('files', 'creative_default_files.json'), indent=4)
        print('load creative_default_paymentmethod.json')
        call_command('dumpdata', 'payments.paymentmethod', output=path % ('payments', 'creative_default_paymentmethod.json'), indent=4)
        print('load creative_default_regions_region.json')
        call_command('dumpdata', 'regions.region', output=path % ('regions', 'creative_default_regions_region.json'), indent=4)
        print('load creative_default_directories_pricings.json')
        call_command('dumpdata', 'directories.directorypricing', output=path % ('directories', 'creative_default_directories_pricings.json'), indent=4)
        print('load creative_default_forms.json')
        call_command('dumpdata', 'forms', output=path % ('forms_builder/forms', 'creative_default_forms.json'), indent=4)
        print('load creative_default_events.json')
        # event_list = [
        #     'events.customregfield',
        #     'events.customregform',
        #     "events.event",
        #     "events.organizer",
        #     "events.paymentmethod",
        #     "events.regconfpricing",
        #     "events.registrationconfiguration",
        #     "events.place",
        #     "events.type",
        #     "events.typecolorset",
        # ]
        # call_command('dumpdata', ' '.join(event_list), output=path % ('events', 'creative_default_events.json'), indent=4)

        suffix_list = [
            'events.customregfield',
            'events.customregform',
            "events.event",
            "events.organizer",
            "events.paymentmethod",
            "events.regconfpricing",
            "events.registrationconfiguration",
            "events.place",
            "events.type",
            "events.typecolorset",
            'profiles.profile',
            'jobs',
            'memberships',
            'corporate_memberships',
            'articles',
            'forums',
            'news',
            'photos',
            'boxes',
            'pages',
            'navs',
            'stories',
            'videos',
        ]

        # call loaddata on fixtures
        for suffix in suffix_list:
            filename = 'creative_default_%s.json' % suffix.replace('.', '_')
            tmp = suffix.split('.')
            app_label = suffix
            if len(tmp) > 0:
                app_label = tmp[0]

            print(filename)
            call_command('dumpdata', suffix, output=path % (app_label, filename), indent=4)
