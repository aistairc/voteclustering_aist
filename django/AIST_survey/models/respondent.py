from django.db import models
from . import Enquete
from django.utils import timezone
import hashlib


class Respondent(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    finishTime = models.DateTimeField(default=timezone.now)
    # startTimeが未設定の場合startTimeと同時刻に設定
    startTime = models.DateTimeField(blank=True, null=True)
    hashedIpAddress = models.CharField(max_length=130)

    def save(self, *args, **kwargs):
        if not self.startTime:
            self.startTime = self.finishTime
        super().save(*args, **kwargs)

    def __str__(self):
        if self.attribute is not None:
            respondent_info = self.attribute
        else:
            respondent_info = str(self.id)

        return respondent_info

    @staticmethod
    def hash_ip_address(ip):
        return hashlib.sha3_512(ip.encode('utf-8')).hexdigest()
