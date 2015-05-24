import uuid
import copy
from django import template

register = template.Library()


@register.tag(name='async')
def do_async(parser, token):
    nodelist = parser.parse(('endasync',))
    parser.delete_first_token()
    return AsyncNode(nodelist)


class AsyncNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.uuid = uuid.uuid4().hex
        self.context = None


    def render(self, context, **kwargs):
        assert 'async_requests' in context, ("ContextProcessor 'async_tag.context_processors.async' required.")

        self.context = copy.copy(context)
        self.context['async_requests'].append(self.render_async)

        return '<span id="async_{uuid}"></span>'.format(
            uuid=self.uuid
        )


    def render_async(self):
        output = self.nodelist.render(self.context)

        return """
            <script type="text/javascript">
                document.getElementById("async_{uuid}").innerHTML = "{output}";
            </script>
        """.format(
            uuid=self.uuid,
            output=output.replace('"', '\\"').replace('\n', '\\\n')
        )
