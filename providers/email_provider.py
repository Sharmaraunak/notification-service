from models.model import Email


class EmailProvider:

    _sender = "noreply@example.com"
    async def send_email(self, email: Email):
        print(f"""
            To: {email.to}
            Subject: {email.subject}
            body: {email.body}
            from: {self._sender}
        """)
