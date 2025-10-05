from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import (
    HeroSection, Service, Project, ProjectCarousel, ProjectDetails, 
    GalleryImage, Press, PressItem, Architect, Review, ContactInfo, 
    Zayavka, Order, OrderTask
)


class HeroSectionResource(resources.ModelResource):
    class Meta:
        model = HeroSection
        fields = ('id', 'title', 'description', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'title', 'description', 'is_active', 'created_at', 'updated_at')


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        fields = ('id', 'title', 'description', 'image', 'order', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'title', 'description', 'image', 'order', 'is_active', 'created_at', 'updated_at')


class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'image', 'model_3d_file', 'order', 'is_featured', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'title', 'description', 'image', 'model_3d_file', 'order', 'is_featured', 'is_active', 'created_at', 'updated_at')


class ProjectCarouselResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project', widget=ForeignKeyWidget(Project, 'title'))
    
    class Meta:
        model = ProjectCarousel
        fields = ('id', 'project', 'image', 'order', 'is_active', 'created_at')
        export_order = ('id', 'project', 'image', 'order', 'is_active', 'created_at')


class ProjectDetailsResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project', widget=ForeignKeyWidget(Project, 'title'))
    
    class Meta:
        model = ProjectDetails
        fields = ('id', 'project', 'title', 'description', 'image', 'url', 'order', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'project', 'title', 'description', 'image', 'url', 'order', 'is_active', 'created_at', 'updated_at')


class GalleryImageResource(resources.ModelResource):
    class Meta:
        model = GalleryImage
        fields = ('id', 'title', 'image', 'order', 'css_classes', 'is_active', 'created_at')
        export_order = ('id', 'title', 'image', 'order', 'css_classes', 'is_active', 'created_at')


class PressResource(resources.ModelResource):
    class Meta:
        model = Press
        fields = ('id', 'title', 'image', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'title', 'image', 'is_active', 'created_at', 'updated_at')


class PressItemResource(resources.ModelResource):
    class Meta:
        model = PressItem
        fields = ('id', 'title', 'description', 'order', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'title', 'description', 'order', 'is_active', 'created_at', 'updated_at')


class ArchitectResource(resources.ModelResource):
    class Meta:
        model = Architect
        fields = ('id', 'name', 'position', 'description', 'photo', 'order', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'name', 'position', 'description', 'photo', 'order', 'is_active', 'created_at', 'updated_at')


class ReviewResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project', widget=ForeignKeyWidget(Project, 'title'))
    
    class Meta:
        model = Review
        fields = ('id', 'project', 'first_name', 'last_name', 'comment', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'project', 'first_name', 'last_name', 'comment', 'is_active', 'created_at', 'updated_at')


class ContactInfoResource(resources.ModelResource):
    class Meta:
        model = ContactInfo
        fields = ('id', 'email', 'phone', 'address', 'map_embed_url', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'email', 'phone', 'address', 'map_embed_url', 'is_active', 'created_at', 'updated_at')


class ZayavkaResource(resources.ModelResource):
    class Meta:
        model = Zayavka
        fields = ('id', 'name', 'email', 'phone', 'created_at', 'is_processed')
        export_order = ('id', 'name', 'email', 'phone', 'created_at', 'is_processed')


class OrderResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget('accounts.CustomUser', 'email'))
    project = fields.Field(column_name='project', attribute='project', widget=ForeignKeyWidget(Project, 'title'))
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user', 'project', 'project_image', 'status', 'start_date', 'end_date', 'created_at', 'updated_at')
        export_order = ('id', 'order_number', 'user', 'project', 'project_image', 'status', 'start_date', 'end_date', 'created_at', 'updated_at')


class OrderTaskResource(resources.ModelResource):
    order = fields.Field(column_name='order', attribute='order', widget=ForeignKeyWidget(Order, 'order_number'))
    
    class Meta:
        model = OrderTask
        fields = ('id', 'order', 'title', 'description', 'start_date', 'end_date', 'status', 'order_num')
        export_order = ('id', 'order', 'title', 'description', 'start_date', 'end_date', 'status', 'order_num')
