def async_rendering(request):
    """
    Template tag async registers callbacks.
    Middleware AsyncMiddleware invokes callbacks.
    """
    request.async_renderings = []
    return {'async_renderings': request.async_renderings}
