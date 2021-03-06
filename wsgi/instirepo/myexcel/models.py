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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tool_number + "-" + self.jw_number + "-" + self.product + "-" + self.target_date


class Details(models.Model):
    date = models.DateTimeField(auto_now=True, null=True)
    expected_date = models.TextField(null=True)
    actual_date = models.TextField(null=True)
    trial_date = models.TextField(null=True)
    qc_date = models.TextField(null=True)
    action_taken = models.TextField(null=True)
    status = models.TextField(null=True)
    cost = models.TextField(null=True)
    remarks = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    work = models.ForeignKey(Works, null=True)

    def __str__(self):
        return self.action_taken + "-" + self.status + "-" + self.remarks + "-" + self.expected_date
