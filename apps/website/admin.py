from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import HeroSection, Service, Project, ProjectCarousel, ProjectDetails, GalleryImage, Press, PressItem, Architect, Review, ContactInfo, Zayavka, Order, OrderTask
from .resources import (
    HeroSectionResource, ServiceResource, ProjectResource, ProjectCarouselResource,
    ProjectDetailsResource, GalleryImageResource, PressResource, PressItemResource,
    ArchitectResource, ReviewResource, ContactInfoResource, ZayavkaResource,
    OrderResource, OrderTaskResource
)

# Configure admin site
admin.site.site_header = 'ENGLER House - Административная панель'
admin.site.site_title = 'ENGLER House Admin'
admin.site.index_title = 'Управление сайтом'


@admin.register(HeroSection)
class HeroSectionAdmin(ImportExportModelAdmin):
    resource_class = HeroSectionResource
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Контент', {
            'fields': ('title', 'description'),
            'description': 'Основной контент для hero секции на главной странице'
        }),
        ('Настройки', {
            'fields': ('is_active',),
            'description': 'Может быть активна только одна hero секция'
        }),
        ('Информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion if it's the only active hero section
        if obj and obj.is_active:
            if HeroSection.objects.filter(is_active=True).count() == 1:
                return False
        return super().has_delete_permission(request, obj)


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProjectCarouselInline(admin.TabularInline):
    model = ProjectCarousel
    extra = 1
    fields = ('image', 'order', 'is_active')
    ordering = ('order',)


class ProjectDetailsInline(admin.StackedInline):
    model = ProjectDetails
    extra = 1
    fields = ('title', 'description', 'image', 'url', 'order', 'is_active')
    ordering = ('order',)


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ('title', 'order', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_featured', 'is_active')
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectCarouselInline, ProjectDetailsInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'image', 'model_3d_file'),
            'description': '<strong>Важно!</strong> Для 3D модели используйте только форматы <strong>.glb</strong> или <strong>.gltf</strong>. Другие форматы не будут отображаться онлайн.'
        }),
        ('Настройки', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectCarousel)
class ProjectCarouselAdmin(ImportExportModelAdmin):
    resource_class = ProjectCarouselResource
    list_display = ('project', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'project')
    search_fields = ('project__title',)
    list_editable = ('order', 'is_active')
    ordering = ('project', 'order', '-created_at')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('project', 'image'),
            'description': 'Изображения для карусели проекта'
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectDetails)
class ProjectDetailsAdmin(ImportExportModelAdmin):
    resource_class = ProjectDetailsResource
    list_display = ('project', 'title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'project')
    search_fields = ('project__title', 'title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('project', 'order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('project', 'title', 'description', 'image', 'url')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(ImportExportModelAdmin):
    resource_class = GalleryImageResource
    list_display = ('title', 'order',  'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active',)
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'image'),
            'description': 'Загрузите изображение для галереи'
        }),
        ('Позиция', {
            'fields': ('order', 'css_classes'),
            'description': 'Order от 1 до 10. Каждая позиция автоматически получает свое расположение на странице'
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show count of active images
        return qs
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(Press)
class PressAdmin(ImportExportModelAdmin):
    resource_class = PressResource
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'image'),
            'description': 'Заголовок и изображение секции "Пресса о нас"'
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting if it's the only active Press"""
        if obj and obj.is_active:
            if Press.objects.filter(is_active=True).count() <= 1:
                return False
        return super().has_delete_permission(request, obj)


@admin.register(PressItem)
class PressItemAdmin(ImportExportModelAdmin):
    resource_class = PressItemResource
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Architect)
class ArchitectAdmin(ImportExportModelAdmin):
    resource_class = ArchitectResource
    list_display = ('name', 'position', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'position', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'position', 'description', 'photo')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
    list_display = ('full_name', 'project', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'project')
    search_fields = ('first_name', 'last_name', 'comment', 'project__title')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('first_name', 'last_name')
        }),
        ('Отзыв', {
            'fields': ('project', 'comment')
        }),
        ('Настройки', {
            'fields': ('is_active',),
            'description': 'Отзыв будет виден на сайте только после модерации'
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Имя"


@admin.register(ContactInfo)
class ContactInfoAdmin(ImportExportModelAdmin):
    resource_class = ContactInfoResource
    list_display = ('phone', 'email', 'is_active')


@admin.register(Zayavka)
class ZayavkaAdmin(ImportExportModelAdmin):
    resource_class = ZayavkaResource
    list_display = ('name', 'email', 'phone', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    list_editable = ('is_processed',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Статус', {
            'fields': ('is_processed', 'created_at')
        }),
    )


class OrderTaskInline(admin.TabularInline):
    model = OrderTask
    extra = 1
    fields = ('title', 'start_date', 'end_date', 'status', 'order_num')
    ordering = ('order_num',)


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('order_number', 'get_client_name', 'status', 'start_date', 'end_date', 'get_progress_percentage', 'created_at')
    list_filter = ('status', 'created_at', 'start_date', 'user')
    search_fields = ('order_number', 'user__first_name', 'user__last_name', 'user__email')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'get_progress_percentage')
    inlines = [OrderTaskInline]
    date_hierarchy = 'created_at'
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order_number', 'user', 'project', 'project_image', 'status')
        }),
        ('Сроки', {
            'fields': ('start_date', 'end_date')
        }),
        ('Прогресс', {
            'fields': ('get_progress_percentage',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_client_name(self, obj):
        return obj.user.full_name
    get_client_name.short_description = "Клиент"
    get_client_name.admin_order_field = 'user__last_name'
    
    def get_progress_percentage(self, obj):
        return f"{obj.get_progress_percentage()}%"
    get_progress_percentage.short_description = "Прогресс"


@admin.register(OrderTask)
class OrderTaskAdmin(ImportExportModelAdmin):
    resource_class = OrderTaskResource
    list_display = ('order', 'title', 'start_date', 'end_date', 'status', 'order_num', 'get_duration_days')
    list_filter = ('status', 'start_date', 'order')
    search_fields = ('title', 'description', 'order__order_number')
    list_editable = ('status', 'order_num')
    ordering = ('order', 'order_num')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order', 'title', 'description', 'order_num')
        }),
        ('Сроки', {
            'fields': ('start_date', 'end_date', 'status')
        }),
    )
    
    def get_duration_days(self, obj):
        return f"{obj.get_duration_days()} дней"
    get_duration_days.short_description = "Длительность"
    