from sigauth.helpers import RequestSigner

from django.conf import settings


request_signer = RequestSigner(
    settings.UPSTREAM_SIGNATURE_SECRET,
    sender_id=settings.UPSTREAM_SIGNATURE_SENDER_ID,
)
