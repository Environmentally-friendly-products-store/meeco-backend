from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = "Create a superuser with a password non-interactively"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Specifies the password for the superuser.",
        )

    def handle(self, *args, **options):
        options.setdefault("interactive", False)
        database = options.get("database")
        password = options.get("password")
        email = options.get("email")
        first_name = options.get("first_name")
        last_name = options.get("last_name")

        if not password or not email or not first_name or not last_name:
            raise CommandError(
                "--email, --password, --first_name"
                "and --last_name are required options"
            )

        user_data = {
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }

        self.UserModel._default_manager.db_manager(database).create_superuser(
            **user_data
        )

        if options.get("verbosity", 0) >= 1:
            self.stdout.write("Superuser created successfully.")
