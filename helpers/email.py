from django.core.mail import EmailMessage
from django.template import loader
from django.template.loader import get_template
from django.conf import settings


class EmailHandler:
    subject_template_name = 'subject.html'
    html_body_template_name = 'transaction_alert.html'
    cc = []

    def create_email(self, **ctx):
        subject = loader.render_to_string(self.subject_template_name, ctx)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(self.html_body_template_name, ctx)
        cc = ctx['cc'] if ctx.get('cc') else []

        email_message = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [ctx['email']],
            cc=cc
        )

        email_message.content_subtype = 'html'
        email_message.send(fail_silently=True)