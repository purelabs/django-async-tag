from django import template
from functools import partial

import copy
import uuid


register = template.Library()


@register.tag
def async(parser, token):
    nodelist_async = parser.parse(('await', 'endasync',))
    token = parser.next_token()

    if token.contents == 'await':
        nodelist_await = parser.parse(('endasync',))
        parser.delete_first_token()
    else:
        nodelist_await = None

    return AsyncNode(nodelist_async, nodelist_await)


class AsyncNode(template.Node):
    child_nodelists = ('nodelist_async', 'nodelist_await')

    def __init__(self, nodelist_async, nodelist_await=None):
        self.nodelist_async = nodelist_async
        self.nodelist_await = nodelist_await if nodelist_await is not None else template.NodeList()


    def __iter__(self):
        for node in self.nodelist_async:
            yield node
        for node in self.nodelist_await:
            yield node


    def render(self, context):
        if not 'async_renderings' in context:
            raise Exception("ContextProcessor 'async_tag.context_processors.async' required.")

        _uuid = uuid.uuid4().hex
        _context = copy.copy(context) # Copy instance attributes
        _context.dicts = [_context.flatten()] # Copy context data
        _context['async_renderings'].append(partial(self.render_async, _uuid, _context))

        return '<span id="async_begin_{uuid}"></span>{await}<span id="async_end_{uuid}"></span>'.format(
            uuid=_uuid,
            await=self.nodelist_await.render(context)
        )


    def render_async(self, uuid, context):
        output = self.nodelist_async.render(context)

        return """
            <script type="text/javascript">
                var startElement = document.getElementById("async_begin_{uuid}");
                var endElement = document.getElementById("async_end_{uuid}");
                var element = startElement;
                while (element !== endElement) {{
                    var nextElement = element.nextSibling;
                    element.remove();
                    element = nextElement;
                }}
                endElement.outerHTML = "{output}";
            </script>
        """.format(
            uuid=uuid,
            output=output.replace('\\', '\\\\').replace('/', '\\/').replace('"', '\\"').replace('\n', '\\n')
        )
