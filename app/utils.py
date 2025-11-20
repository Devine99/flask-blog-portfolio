from flask import render_template, request
from flask_mail import Message
from datetime import datetime
from .extensions import mail, db
from .models import ContactSubmission
import logging

logger = logging.getLogger(__name__)


def send_contact_email(form, app):
    try:
        name = form.data.get("name")
        email = form.data.get("email")
        message = form.data.get("message")
        number = form.data.get("number") or "Not provided"

        subject = f"New Contact: {name}"
        msg = Message(
            subject=subject,
            sender=app.config.get("MAIL_DEFAULT_SENDER"),
            recipients=[app.config.get("MAIL_USERNAME")],
            reply_to=email,
        )
        msg.html = render_template(
            "email/contact_notification.html",
            name=name,
            email=email,
            message=message,
            number=number,
            submission_date=datetime.now(),
        )
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False


def save_contact_to_database(form):
    try:
        submission = ContactSubmission(
            name=form.data.get("name"),  # type: ignore
            email=form.data.get("email"),  # type: ignore
            message=form.data.get("message"),  # type: ignore
            number=form.data.get("number"),  # type: ignore
            ip_address=request.remote_addr,  # type: ignore
            user_agent=request.headers.get("User-Agent"),  # type: ignore
        )
        db.session.add(submission)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"DB Save error: {e}")
        return False
