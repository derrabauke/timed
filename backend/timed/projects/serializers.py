"""Serializers for the projects app."""
from datetime import timedelta

from django.db.models import Sum
from django.utils.duration import duration_string
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import ModelSerializer

from timed.projects import models
from timed.tracking.models import Report


class CustomerSerializer(ModelSerializer):
    """Customer serializer."""

    class Meta:
        """Meta information for the customer serializer."""

        model  = models.Customer
        fields = [
            'name',
            'email',
            'website',
            'comment',
            'archived',
        ]


class BillingTypeSerializer(ModelSerializer):
    class Meta:
        model  = models.BillingType
        fields = ['name']


class ProjectSerializer(ModelSerializer):
    """Project serializer."""

    customer = ResourceRelatedField(queryset=models.Customer.objects.all())
    billing_type = ResourceRelatedField(
        queryset=models.BillingType.objects.all()
    )

    included_serializers = {
        'customer': 'timed.projects.serializers.CustomerSerializer',
        'billing_type': 'timed.projects.serializers.BillingTypeSerializer'
    }

    def get_root_meta(self, resource, many):
        if not many:
            queryset = Report.objects.filter(task__project=self.instance)
            data = queryset.aggregate(spent_time=Sum('duration'))
            data['spent_time'] = duration_string(
                data['spent_time'] or timedelta(0)
            )
            return data

        return {}

    class Meta:
        """Meta information for the project serializer."""

        model  = models.Project
        fields = [
            'name',
            'comment',
            'estimated_time',
            'archived',
            'customer',
            'billing_type'
        ]


class TaskSerializer(ModelSerializer):
    """Task serializer."""

    project = ResourceRelatedField(queryset=models.Project.objects.all())

    included_serializers = {
        'activities': 'timed.tracking.serializers.ActivitySerializer',
        'project':    'timed.projects.serializers.ProjectSerializer'
    }

    def get_root_meta(self, resource, many):
        if not many:
            queryset = Report.objects.filter(task=self.instance)
            data = queryset.aggregate(spent_time=Sum('duration'))
            data['spent_time'] = duration_string(
                data['spent_time'] or timedelta(0)
            )
            return data

        return {}

    class Meta:
        """Meta information for the task serializer."""

        model  = models.Task
        fields = [
            'name',
            'estimated_time',
            'archived',
            'project',
        ]
