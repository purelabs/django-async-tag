import uuid
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

        if getattr(context, 'is_async', False):
            self.context = context

            return '<span id="async_{uuid}"></span>'.format(
                uuid=self.uuid
            )
        else:
            return self.nodelist.render(context)



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
