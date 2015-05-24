import time

from django.shortcuts import render


def test(request):
    def get_name():
        time.sleep(2)
        return 'Seb'

    return render(request, 'test.html', {
        'my_name': get_name
    })
