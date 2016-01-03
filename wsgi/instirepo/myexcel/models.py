from django.db import models


class Works(models.Model):
    tool_number = models.TextField(null=True)
    jw_number = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)
    product = models.TextField(null=True)
    description = models.TextField(null=True)
    start_date = models.TextField(null=True)
    target_date = models.TextField(null=True)
    done_by = models.TextField(null=True)
    actual_date = models.TextField(null=True)
    cost = models.TextField(null=True)
    status = models.TextField(null=True)
    remarks = models.TextField(null=True)


class Details(models.Model):
    date = models.TextField(null=True)
    expected_date = models.TextField(null=True)
    actual_date = models.TextField(null=True)
    trial_date = models.TextField(null=True)
    qc_date = models.TextField(null=True)
    action_taken = models.TextField(null=True)
    status = models.TextField(null=True)
    cost = models.TextField(null=True)
    remarks = models.TextField(null=True)
