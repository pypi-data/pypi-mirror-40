import uuid
from django.shortcuts import redirect
from django.urls import reverse

from alipay.models import AlipayPayment


def example_alipay_create_view(request):
    payment = AlipayPayment.objects.create(
        out_no=uuid.uuid4(),
        subject='充值',
        body='1年365元',
        amount_total=0.01,
        expire='30m',
        # reference_id='1' # 可选
    )
    redirect_url = reverse('alipay_redirect', kwargs=dict(out_no=payment.out_no)) + '?ua=auto'
    return redirect(redirect_url)
