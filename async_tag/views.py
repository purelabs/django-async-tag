from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, StreamingHttpResponse
from async_tag.templatetags.async import AsyncNode

def render_async(request, template_name, context):
    template = get_template(template_name)

    is_async = request.GET.get('async', '1') == '1'

    if not isinstance(context, Context):
        context = Context(context)

    context.is_async = is_async

    def do_async():
        html = template.render(context)

        html = html.replace('</body>', '').replace('</html>', '')
        html += """
            <script type="text/javascript">
                document.dispatchEvent(new Event("DOMContentLoaded"));
            </script>
        """

        yield html + '\n'


        for async_node in template.nodelist.get_nodes_by_type(AsyncNode):
            yield async_node.render_async() + '\n'

        yield '</body></html>\n'


    if is_async:
        return StreamingHttpResponse(do_async())
    else:
        return HttpResponse(template.render(context))
