from django.http import StreamingHttpResponse

import re


re_end_body = re.compile('</body>', re.IGNORECASE)
re_end_html = re.compile('</html>', re.IGNORECASE)


class AsyncMiddleware(object):

    def process_response(self, request, response):
        if hasattr(request, 'async_renderings') and request.async_renderings:
            if not 200 <= response.status_code < 300:
                return response

            if response.streaming:
                raise Exception('async template tag only allowed for non streaming response')

            if not response.get('Content-Type', '').startswith('text/html'):
                raise Exception("async template tag only allowed for response with Content-Type 'text/html'")

            streaming_response = StreamingHttpResponse(self.stream(request, response))
            streaming_response.__dict__.update(response.__dict__)

            return streaming_response

        return response


    def process_exception(self, request, exception):
        if hasattr(request, 'async_renderings'):
            del request.async_renderings


    def stream(self, request, response):
        content = response.content
        content = re_end_body.sub('', content)
        content = re_end_html.sub('', content)

        content += """
            <script type="text/javascript">
                document.dispatchEvent(new Event("DOMContentLoaded"));
            </script>
        """

        yield content + '\n'

        for async_rendering in request.async_renderings:
            yield async_rendering() + '\n'

        yield '</body></html>'
