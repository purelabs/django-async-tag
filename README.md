# Installation

- Add async_tag to your installed apps:
```python
INSTALLED_APPS = (
    # ...
    'async_tag',
)
```

- Add async_tag middleware:
```python
MIDDLEWARE_CLASSES = (
    # ...
    'async_tag.middlewares.AsyncMiddleware',
)
```

- Add async_tag context_processor:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ...
        'OPTIONS': {
            'context_processors': [
                # ...
                'async_tag.context_processors.async',
            ],
        },
    },
]
```

- Enjoy async_tag:
```html
{% load async %}
<!doctype html>
<html>
    <body>
        <p>
        {% templatetag openvariable %} products {% templatetag closevariable %} can be a callable or an iterator loading products from database.<br>
        </p>
        <ul>
        {% async %}
            {% for product in products %}
                <li>{{ product.name }}</li>
            {% endfor %}
        {% await %}
            <li>Products are loaded...</li>
        {% endasync %}
        </ul>
    </body>
</html>
```


# Usage

```
{% load async %}

{% async %}
    content that should be rendered asynchronously goes here.
{% endasync %}

{% async %}
    content that should be rendered asynchronously goes here.
{% await %}
    content that should be displayed until async content is rendered goes here.
{% endasync %}
```
