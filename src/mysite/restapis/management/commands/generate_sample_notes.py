from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from restapis.models import Note


class Command(BaseCommand):
    help = "Generates samples notes for the given users"

    def add_arguments(self, parser):
        parser.add_argument("--user_emails", nargs="+")
        parser.add_argument("--notes_count", type=int, required=False, default=3)

    def handle(self, *args, **options):
        notes_generation_count = options.get("notes_count", 3)
        user_emails = list(set(options.get("user_emails", [])))

        # perform validation on emails
        invalid_emails = []
        for email in user_emails:
            try:
                validate_email(email)
            except ValidationError as ve:
                invalid_emails.append(email)

        if invalid_emails:
            raise CommandError('one or more provided emails are invalid: %s' % invalid_emails)

        # user, auth-token, notes generation
        for email in user_emails:
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                user.set_password("000")
                user.save()

            token, _ = Token.objects.get_or_create(user=user)

            nc = Note.objects.filter(owner=user).count()
            user_notes = Note.objects.bulk_create(
                [
                    Note(title=f"#{nc+i} note", body=f"#{nc+i} lorem ipsum", owner=user)
                    for i in range(1, notes_generation_count+1)
                ]
            )

            notes_pk = [ n.pk for n in user_notes ]
            self.stdout.write(
                self.style.SUCCESS('Notes (pk: %s) generated successfully! user: %s, auth token: %s' % (notes_pk, email, token))
            )
