def async(request):
    request.async_requests = []

    return {'async_requests': request.async_requests}
