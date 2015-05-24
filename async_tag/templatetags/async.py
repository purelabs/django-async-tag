import uuid
import copy
from django import template

register = template.Library()


@register.tag(name='async')
def do_async(parser, token):

    states = {}
    end_tag = 'endasync'
    default_states = ['async', 'await']

    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()

    return AsyncNode(states)


class AsyncNode(template.Node):

    def __init__(self, states):
        self.states = states
        self.uuid = uuid.uuid4().hex
        self.context = None


    def render(self, context, **kwargs):
        assert 'async_requests' in context, ("ContextProcessor 'async_tag.context_processors.async' required.")

        self.context = copy.copy(context)
        self.context['async_requests'].append(self.render_async)

        await = ''
        if self.states.get('await'):
            await = self.states['await'].render(context)

        return """
            <span id="async_begin_{uuid}"></span>
                {await}
            <span id="async_end_{uuid}"></span>
        """.format(
            uuid=self.uuid,
            await=await
        )


    def render_async(self):
        output = self.states['async'].render(self.context)

        return """
            <script type="text/javascript">
                console.log('foo', currentElement.parentNode);
                var currentElement = document.getElementById("async_begin_{uuid}");
                currentElement.parentNode.insertBefore(currentElement, "{output}");

                while (currentElement.id !== "async_end_{uuid}") {
                    var nextElement = currentElement.nextSibling;
                    currentElement.remove();
                    currentElement = nextElement;
                }
            </script>
        """.format(
            uuid=self.uuid,
            output=output.replace('"', '\\"').replace('\n', '\\\n')
        )
