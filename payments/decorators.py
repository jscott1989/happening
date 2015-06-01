"""Payment decorators."""
from payments.models import Payment
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


def payment_decorator(func):
    """Ensure that the method is only called once for a payment.

    Also ensure that it is only called on payments which have
    been attempted, and only called for the correct user.

    This will only mark a payment as "complete" if the return value
    has a status of 200, 201, or 304.

    If you status does not match these - you should update the payment
    manually by setting "complete" to True and saving.
    """
    def inner(request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        if not payment.user == request.user:
            return HttpResponseForbidden()
        if payment.complete:
            return HttpResponseForbidden()
        if payment.status == "PENDING":
            return HttpResponseForbidden()
        response = func(request, payment)
        if response.status_code in [200, 201, 304]:
            payment.complete = True
            payment.save()
        return response
    return inner
