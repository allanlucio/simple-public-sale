from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def exceptions_to_messages(function):
    def wrap(request, *args, **kwargs):
        try:

            return function(request, *args, **kwargs)

        except ValidationError as error:
            message=error.message
            messages.error(request,message)
            prenda_id=kwargs.get("prenda_id")
            evento_id=kwargs.get("evento_id")
            return redirect(
                reverse(viewname='manage-event', kwargs={'evento_id': evento_id}) + "?prenda=%s" % prenda_id)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap