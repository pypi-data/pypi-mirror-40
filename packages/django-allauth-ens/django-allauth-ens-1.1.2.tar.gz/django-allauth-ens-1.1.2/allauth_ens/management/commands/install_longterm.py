# coding: utf-8
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialAccount

from allauth_ens.adapter import install_longterm_adapter


class Command(BaseCommand):
    help = 'Manages the transition from an older django_cas' \
           'or an allauth_ens installation without ' \
           'LongTermClipperAccountAdapter'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fake',
            action='store_true',
            default=False,
            help=('Does not save the models created/updated,'
                  'only shows the list'),
        )
        parser.add_argument(
            '--use-socialaccounts',
            action='store_true',
            default=False,
            help=('Use the existing SocialAccounts rather than all the Users'),
        )
        parser.add_argument(
            '--keep-usernames',
            action='store_true',
            default=False,
            help=('Do not apply the username template (e.g. clipper@promo) to'
                  'the existing account, only populate the SocialAccounts with'
                  'ldap informations'),
        )
        parser.add_argument(
            '--clipper-field',
            default=None,
            type=str
        )
        pass

    def handle(self, *args, **options):
        fake = options.get("fake", False)
        keep_usernames = options.get("keep_usernames", False)

        if options.get('use_socialaccounts', False):
            accounts = {account.uid: account.user for account in
                        (SocialAccount.objects.filter(provider="clipper")
                         .prefetch_related("user"))}
        elif options.get('clipper_field', None):
            fields = options['clipper_field'].split('.')
            User = get_user_model()

            def get_subattr(obj, fields):
                # Allows to follow OneToOne relationships
                if len(fields) == 1:
                    return getattr(obj, fields[0])
                return get_subattr(getattr(obj, fields[0]), fields[1:])

            accounts = {get_subattr(account, fields): account for account in
                        User.objects.all()}
        else:
            accounts = None

        logs = install_longterm_adapter(fake, accounts, keep_usernames)

        self.stdout.write("Social accounts created : %d"
                          % len(logs["created"]))
        self.stdout.write("  ".join(("%s -> %s" % s) for s in logs["created"]))
        self.stdout.write("Social accounts displaced : %d"
                          % len(logs["updated"]))
        self.stdout.write("  ".join(("%s -> %s" % s) for s in logs["updated"]))
        self.stdout.write("User accounts unmodified : %d"
                          % len(logs["unmodified"]))
        self.stdout.write("   ".join(logs["unmodified"]))

        self.stdout.write(self.style.SUCCESS(
            "LongTermClipper migration successful"))
