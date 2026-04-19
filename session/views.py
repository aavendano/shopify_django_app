from datetime import datetime

from django.views.generic import DetailView

from .models import Session


def _mask_secret(value):
    if not value:
        return "Sin valor"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def _format_value(value):
    if value in {None, ""}:
        return "Sin valor"
    if isinstance(value, bool):
        return "Si" if value else "No"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


class SessionDetailView(DetailView):
    model = Session
    template_name = "session/session_detail.html"
    context_object_name = "session"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = context["session"]
        context["detail_rows"] = [
            ("ID", _format_value(session.id)),
            ("Shop", _format_value(session.shop)),
            ("State", _format_value(session.state)),
            ("Online", _format_value(session.isonline)),
            ("Scope", _format_value(session.scope)),
            ("Expires", _format_value(session.expires)),
            ("Access token", _mask_secret(session.accesstoken)),
            ("User ID", _format_value(session.userid)),
            ("First name", _format_value(session.firstname)),
            ("Last name", _format_value(session.lastname)),
            ("Email", _format_value(session.email)),
            ("Account owner", _format_value(session.accountowner)),
            ("Locale", _format_value(session.locale)),
            ("Collaborator", _format_value(session.collaborator)),
            ("Email verified", _format_value(session.emailverified)),
            ("Refresh token", _mask_secret(session.refreshtoken)),
            (
                "Refresh token expires",
                _format_value(session.refreshtokenexpires),
            ),
        ]
        return context
