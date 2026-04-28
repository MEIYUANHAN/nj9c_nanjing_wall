from django.db import models
from django.contrib.auth.models import User

class WallSection(models.Model):
    """南京城墙段落模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="贡献者", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="段落名称")
    location = models.CharField(max_length=200, verbose_name="地理位置")
    built_year = models.CharField(max_length=50, verbose_name="建造年代")
    length = models.CharField(max_length=50, verbose_name="长度")
    description = models.TextField(verbose_name="详细描述")
    event = models.TextField(verbose_name="相关历史事件", null=True, blank=True)
    image = models.ImageField(upload_to='static/', verbose_name="图片", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    objects = models.Manager()  # 默认管理器
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "城墙段落"
        verbose_name_plural = "城墙段落"

class HistoricalEvent(models.Model):
    """历史事件模型"""
    title = models.CharField(max_length=200, verbose_name="事件标题")
    year = models.CharField(max_length=20, verbose_name="发生年份")
    description = models.TextField(verbose_name="事件描述")
    wall_section = models.ForeignKey(WallSection, on_delete=models.CASCADE, 
                                     related_name='events', verbose_name="相关城墙段落")
    objects = models.Manager()  # 默认管理器
    
    def __str__(self):
        return f"{self.year} - {self.title}"
    
    class Meta:
        verbose_name = "历史事件"
        verbose_name_plural = "历史事件"


class Contribution(models.Model):
    """用户贡献内容模型"""
    

    def __str__(self):
        return self.title
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username



    def __str__(self):
        return self.title
class UserContribution(models.Model):
    """用户贡献内容模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="贡献者")
    name = models.CharField(max_length=100, verbose_name="段落名称", null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="地理位置", null=True, blank=True)
    built_year = models.CharField(max_length=50, verbose_name="建造年代", null=True, blank=True)
    length = models.CharField(max_length=50, verbose_name="长度", null=True, blank=True)
    description = models.TextField(verbose_name="详细描述",null=True, blank=True)
    image = models.ImageField(upload_to='static/', verbose_name="图片", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name if self.name else f"贡献者: {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "用户贡献"
        verbose_name_plural = "用户贡献"