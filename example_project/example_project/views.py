import time

from django.shortcuts import render


def test(request):
    def get_name():
        time.sleep(2)
        return 'Seb'

    return render(request, 'test.html', {
        'my_name': get_name,
        'products': [
            Product('Phone'),
            Product('TV'),
            Product('Car'),
        ]
    })


class Product(object):

    def __init__(self, name):
        self.name = name

    @property
    def rating(self):
        time.sleep(1)
        return len(self.name)
