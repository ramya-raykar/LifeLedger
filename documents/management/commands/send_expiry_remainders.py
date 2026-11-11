from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from documents.models import Document

class Command(BaseCommand):
    help = "Send email remainders for documents nearing expiry"

    def add_arguments(self, parser):
        parser.add_argument("--recipient",required=True,help="Email address to receive expiry remainders",)

    def handle(self, *args, **options):
        recipient = options["recipient"]
        today = timezone.localdate()
        remainder_days = [30, 7, 1]
        sent_count = 0

        for days in remainder_days:
            target_date = today + timedelta(days=days)

            documents = Document.objects.filter(expiry_date=target_date)

            for document in documents:
                subject = f"LifeLedger:{document.title} expires in {days} day(s)"
                message = (f"Hello!\n\n"
                           f"Your document '{document.title}'" f"({document.document_type}) will expire on " f"{document.expiry_date:%d %B %Y}.\n\n"
                           f"Days remaining: {days}\n\n" "Please renew it if necessary.\n\n" "Regards,\nLifeLedger")
                try:
                    send_mail(subject, message, None, [options["recipient"]],fail_silently=False,)
                    sent_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Remainder sent: {document.title} ({days} days)"))
                except Exception as error:
                    self.stderr.write(self.style.ERROR(f"Failed for {document.title}: {error}"))
            self.stdout.write(self.style.SUCCESS(f"Remainder check complete. Emails sent: {sent_count}"))
        
