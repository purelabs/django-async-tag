from django.http import StreamingHttpResponse


class AsyncMiddleware(object):

    def process_response(self, request, response):
        if hasattr(request, 'async_requests'):
            return StreamingHttpResponse(self.stream(request, response))
        else:
            return response


    def stream(self, request, response):
        content = response.content
        content += """
            <script type="text/javascript">
                document.dispatchEvent(new Event("DOMContentLoaded"));
            </script>
        """

        yield content + '\n'

        for async_request in request.async_requests:
            yield async_request() + '\n'
