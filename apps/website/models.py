from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class HeroSection(models.Model):
    """Hero section content for homepage"""
    title = models.CharField(max_length=500, verbose_name="Заголовок", 
                            help_text="Основной заголовок на главной странице")
    description = models.TextField(verbose_name="Описание",
                                  help_text="Текст описания под заголовком")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Hero секция"
        verbose_name_plural = "01. Hero секция"
        ordering = ['-created_at']

    def __str__(self):
        return f"Hero: {self.title[:50]}"

    def save(self, *args, **kwargs):
        """Ensure only one active hero section exists"""
        if self.is_active:
            # Deactivate all other hero sections
            HeroSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Design services offered by Engler House"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='services/', verbose_name="Изображение")
    order = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Услуга"
        verbose_name_plural = "02. Услуги"

    def __str__(self):
        return self.title


class Project(models.Model):
    """Interior design projects portfolio"""
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='projects/', verbose_name="Изображение")
    model_3d_file = models.FileField(
        upload_to='projects/3d/', 
        verbose_name="3D модель",
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Избранный")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Проект"
        verbose_name_plural = "03. Проекты"

    def __str__(self):
        return self.title


class ProjectCarousel(models.Model):
    """Carousel images for project detail page"""
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='carousel_images',
        verbose_name="Проект"
    )
    image = models.ImageField(upload_to='projects/carousel/', verbose_name="Изображение")
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Изображение карусели проекта"
        verbose_name_plural = "03.1 Карусель проектов"

    def __str__(self):
        return f"{self.project.title} - Изображение {self.order}"


class ProjectDetails(models.Model):
    """Detail sections for project page"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name="Проект"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='projects/details/', verbose_name="Изображение")
    url = models.URLField(
        max_length=500,
        verbose_name="Ссылка",
        blank=True,
        help_text="Дополнительная ссылка (необязательно)"
    )
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Детали проекта"
        verbose_name_plural = "03.2 Детали проектов"

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class GalleryImage(models.Model):
    """Gallery images for luxury interior showcase"""
    title = models.CharField(max_length=200, verbose_name="Название", blank=True)
    image = models.ImageField(upload_to='gallery/', verbose_name="Изображение")
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Порядок отображения",
        help_text="От 1 до 10. Каждая позиция имеет свое расположение"
    )
    css_classes = models.CharField(
        max_length=200,
        verbose_name="CSS классы",
        blank=True,
        help_text="Дополнительные CSS классы для позиционирования (необязательно)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Изображение галереи"
        verbose_name_plural = "05. Галерея"

    def __str__(self):
        return self.title or f"Изображение {self.order}"
    
    def get_position_classes(self):
        """Get CSS classes based on order position for masonry layout"""
        position_map = {
            1: 'md:mt-[-70px] md:w-auto',
            2: 'md:w-auto',
            3: 'md:mb-[70px] md:w-auto',
            4: 'md:mb-[-65px] md:mt-[30px] md:w-auto',
            5: 'md:mb-[-55px] md:mt-[-70px] md:w-auto',
            6: 'md:w-auto',
            7: 'md:mb-[80px] md:w-auto',
            8: 'md:mt-[-70px] md:w-auto',
            9: 'md:mt-[65px] md:mb-[16px] md:w-auto',
            10: 'md:mt-[65px] md:mb-[16px] md:w-auto',
        }
        return self.css_classes or position_map.get(self.order, 'md:w-auto')


class Press(models.Model):
    """Press section with title and image"""
    title = models.CharField(max_length=200, verbose_name="Заголовок", default="Пресса о нас")
    image = models.ImageField(upload_to='press/', verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Секция пресса"
        verbose_name_plural = "06. Пресса (секция)"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Ensure only one active Press section exists"""
        if self.is_active:
            Press.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class PressItem(models.Model):
    """Press mentions and quality features"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Элемент пресса"
        verbose_name_plural = "07. Пресса (элементы)"

    def __str__(self):
        return self.title


class Architect(models.Model):
    """Team architects information"""
    name = models.CharField(max_length=200, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='architects/', verbose_name="Фото")
    position = models.CharField(max_length=200, verbose_name="Должность", blank=True)
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок отображения"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Архитектор"
        verbose_name_plural = "04. Архитекторы"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Client reviews for projects"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Проект"
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    comment = models.TextField(verbose_name="Комментарий")
    is_active = models.BooleanField(default=False, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Отзыв"
        verbose_name_plural = "08. Отзывы"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.project.title}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class ContactInfo(models.Model):
    """Contact information for the company"""
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    map_embed_url = models.TextField(verbose_name="Код встраивания карты")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "09. Контактная информация"

    def __str__(self):
        return f"{self.phone} - {self.email}"
    
    def save(self, *args, **kwargs):
        """Ensure only one active ContactInfo exists"""
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Zayavka(models.Model):
    """Feedback/Application form submissions"""
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "10. Заявки"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"


class Order(models.Model):
    """Client project orders"""
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заказа")
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='orders', verbose_name="Клиент")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Проект")
    project_image = models.ImageField(upload_to='orders/', verbose_name="Изображение проекта")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "11. Заказы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.order_number} - {self.user.full_name}"
    
    def get_progress_percentage(self):
        """Calculate project progress based on completed tasks"""
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='completed').count()
        return int((completed_tasks / total_tasks) * 100)


class OrderTask(models.Model):
    """Tasks/stages for orders (for Gantt chart)"""
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tasks', verbose_name="Заказ")
    title = models.CharField(max_length=200, verbose_name="Название этапа")
    description = models.TextField(blank=True, verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    order_num = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Этап заказа"
        verbose_name_plural = "12. Этапы заказов"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.title}"
    
    def get_duration_days(self):
        """Calculate task duration in days"""
        return (self.end_date - self.start_date).days + 1
