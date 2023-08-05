from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
    
                
class BaseDao:
    __queryset = None
    
    def save(self, objeto):
        objeto.save()
    
    @property
    def queryset(self):
        return self.__queryset
    
    @queryset.setter
    def queryset(self, queryset):
        self.__queryset = queryset
    
    def get_all(self):
        return self.queryset.all()
    
    def get_all_by_fields(self, **fields):
        return self.queryset.filter(**fields)
