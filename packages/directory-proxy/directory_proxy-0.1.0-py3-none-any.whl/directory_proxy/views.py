import revproxy.views

from directory_proxy import helpers

from django.conf import settings


class ProxyView(revproxy.views.ProxyView):
    upstream = settings.UPSTREAM_DOMAIN

    def get_request_headers(self):
        headers = super().get_request_headers()
        # revproxy default behaviour copies X-Forwarded-For, which we
        # don't want in order to only populate if we have both
        # X-Forwarded-For and REMOTE_ADDR to keep the number of cases we
        # _do_ populate X-Forwarded-For down
        headers.pop('X-Forwarded-For', None)
        meta = self.request.META
        has_x_forward_for = 'HTTP_X_FORWARDED_FOR' in meta
        has_remote_addr = 'REMOTE_ADDR' in meta
        if has_x_forward_for and has_remote_addr:
            headers['X-Forwarded-For'] = (
                meta['HTTP_X_FORWARDED_FOR'] + ', ' + meta['REMOTE_ADDR']
            )
        if not has_x_forward_for:
            self.log.error(
                'HTTP_X_FORWARDED_FOR was missing from the request %s. '
                'This is not expected: later IP whitelisting will fail.',
                self.request,
            )
        if not has_remote_addr:
            self.log.error(
                'REMOTE_ADDR was missing from the request %s. '
                'This is not expected: later IP whitelisting will fail.',
                self.request,
            )
        headers["X-Forwarded-Host"] = self.request.get_host()
        return headers

    def _created_proxy_response(self, request, path):
        full_path = request.get_full_path().lstrip('/')
        signature_headers = helpers.request_signer.get_signature_headers(
            url=self.get_upstream(path=path) + (full_path or '/'),
            body=request.body,
            method=request.method,
            content_type=self.request_headers.get('Content-Type'),
        )
        self.request_headers.update(signature_headers)
        return super()._created_proxy_response(request, path)
