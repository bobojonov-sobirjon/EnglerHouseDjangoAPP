from import_export import resources
from .models import CustomUser


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'last_name', 'first_name', 'patronymic', 'is_deleted', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
        export_order = ('id', 'email', 'last_name', 'first_name', 'patronymic', 'is_deleted', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
