import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework import filters

from orders_app.models import OrderProducts


class CustomFilter(filters.BaseFilterBackend):
    parameter = None
    type_cast = int


    def get_schema_operation_parameters(self, view):
        return [
            self.parameter
        ]

    def get_schema_fields(self, view):
        return [
            self.parameter
        ]

    def get_param(self, request, param_name: 'str'):
        params = request.query_params.get(param_name, None)
        if params is None:
            return None

        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        try:
            value = self.type_cast(params)
        except:
            return None
        return value

    def get_parameter_value(self, request):
        user = self.get_param(request, self.parameter)
        return user


class FilterUser(CustomFilter):
    parameter = 'user_id'
    type_cast = int

    def filter_queryset(self, request, queryset, view):
        user = self.get_parameter_value(request)
        if user is None:
            return queryset
        return queryset.filter(order__created_by_id=user)


class FilterDateGte(CustomFilter):
    parameter = 'created_start'
    type_cast = str

    def filter_queryset(self, request, queryset, view):
        date = self.get_parameter_value(request)
        if date is None:
            return queryset
        return queryset.filter(order__created__gte=date)

class FilterDateLte(CustomFilter):
    parameter = 'created_end'
    type_cast = str

    def filter_queryset(self, request, queryset, view):
        date = self.get_parameter_value(request)
        if date is None:
            return queryset
        return queryset.filter(order__created__lte=date)
