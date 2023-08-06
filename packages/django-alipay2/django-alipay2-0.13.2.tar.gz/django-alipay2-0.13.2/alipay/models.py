import re
from datetime import timedelta

import pytz
from django.conf import settings
from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from model_utils import FieldTracker

from alipay.signals import payment_succeed


class AlipayPayment(models.Model):
    TRADE_INIT = 'INIT'
    TRADE_WAIT_BUYER_PAY = 'WAIT_BUYER_PAY'
    TRADE_PENDING = 'TRADE_PENDING'
    TRADE_SUCCESS = 'TRADE_SUCCESS'  # 交易成功，且可对该交易做操作，如：多级分润、退款等。
    TRADE_CLOSED = 'TRADE_CLOSED'  # 超时未支付或者全额退款成功
    TRADE_FINISHED = 'TRADE_FINISHED'  # 交易成功且结束，即不可再做任何操作。
    TRADE_MANUAL_SUCCESS = 'MANUAL_SUCCESS'  # 由管理员手动成功

    STATUSES = (
        (TRADE_INIT, '已创建'),
        (TRADE_WAIT_BUYER_PAY, '等待付款'),
        (TRADE_PENDING, '确认中'),
        (TRADE_SUCCESS, '成功'),
        (TRADE_CLOSED, '关闭'),
        (TRADE_FINISHED, '完成'),
        (TRADE_MANUAL_SUCCESS, '手动成功'),  # 设为这个状态时，要注意把expired设为False
    )

    reference_id = models.CharField(max_length=256, null=True, blank=True)  # 业务相关id, 用来对应业务

    subject = models.CharField(max_length=256)
    body = models.TextField()  # max_length=1000

    amount_total = models.DecimalField(max_digits=10, decimal_places=2)

    seller_email = models.EmailField(max_length=100)
    buyer_email = models.CharField(max_length=100, blank=True, null=True)
    buyer_id = models.CharField(max_length=16, blank=True, null=True)

    status = models.CharField(choices=STATUSES, default=TRADE_INIT, max_length=20)
    out_no = models.CharField(max_length=64, unique=True)  # 商户订单号
    no = models.CharField(max_length=64, blank=True, null=True)  # alipay订单号
    expire = models.CharField(max_length=10, default='15m')  # {n} m|h|d, 1c, 1m-15d
    must_pay_before = models.DateTimeField()

    # customized ==================================================================
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tracker = FieldTracker(fields=['status'])

    def is_succeed(self):
        return self.is_succeed_status(self.status)

    is_succeed.boolean = True

    @classmethod
    def get_expire_delta(cls, expire, created_at):
        if expire == '1c':
            created_at = created_at.astimezone(pytz.timezone('Asia/Shanghai'))
            the_day_end = created_at.replace(hour=23, minute=59, second=59, microsecond=0)
            delta = the_day_end - created_at
        else:
            r = re.match(r"(\d+)([mhd])$", expire)
            assert r, 'AlipayPayment.expire not valid'
            count = int(r.group(1))
            unit = r.group(2)
            if unit == 'm':
                delta = timedelta(minutes=count)
            elif unit == 'h':
                delta = timedelta(hours=count)
            else:  # d for day
                delta = timedelta(days=count)

        assert timedelta(minutes=1) <= delta <= timedelta(days=10), 'AlipayPayment.expire should between 1m and 10d'
        return delta

    @classmethod
    def is_succeed_status(cls, status):
        return status in cls.success_statuses()

    @classmethod
    def success_statuses(cls):
        return [cls.TRADE_SUCCESS,
                cls.TRADE_FINISHED,
                cls.TRADE_MANUAL_SUCCESS]

    @classmethod
    def status_weight(cls, status):
        for i, (choice, _) in enumerate(cls.STATUSES):
            if choice == status:
                return i
        return -1

    @classmethod
    def on_pre_save(cls, instance: 'AlipayPayment', raw=None, **kwargs):
        if raw:  # 导入fixture时不运行
            return

        if not instance.must_pay_before:
            created_at = instance.created_at or timezone.now()
            instance.must_pay_before = created_at + cls.get_expire_delta(instance.expire, created_at)

    @classmethod
    def on_post_save(cls, instance: 'AlipayPayment', raw=None, **kwargs):
        if raw:  # 导入fixture时不运行
            return

        # 只有未成功到成功才发信息
        if not instance.is_succeed_status(instance.tracker.previous('status')) and instance.is_succeed():
            payment_succeed.send(AlipayPayment, instance=instance)


post_save.connect(AlipayPayment.on_post_save, AlipayPayment)
pre_save.connect(AlipayPayment.on_pre_save, AlipayPayment)
