import django_filters
from .models import * 
from django_filters import DateFilter


class OderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", )
    class Meta:
        model = Order
        fields = '__all__'
        exclude =['customer','date_created']
