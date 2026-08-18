from django.db import models
from django.contrib.auth.models import User

class WallSection(models.Model):
    """南京城墙段落模型"""
    CONFIDENCE_CHOICES = [
        ('confirmed', '我确定'),
        ('guess', '我推测'),
    ]
    DISPUTE_CHOICES = [
        ('normal', '正常'),
        ('pending', '待考证'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="贡献者", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="段落名称")
    location = models.CharField(max_length=200, verbose_name="地理位置")
    built_year = models.CharField(max_length=50, verbose_name="建造年代")
    length = models.CharField(max_length=50, verbose_name="长度")
    description = models.TextField(verbose_name="详细描述")
    event = models.TextField(verbose_name="相关历史事件", null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name="图片", blank=True)

    # ===== 「慧问慧答」探究能力增强字段 =====
    # 方案一：探究发现（用户的发现/猜想，非必填）
    discovery = models.TextField(verbose_name="探究发现", blank=True, null=True,
                                 help_text="关于这段城墙，你有什么有趣的发现或猜想？")

    # 方案二：双轨可信度输入（区分“我确定”与“我推测”）
    built_year_confidence = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES,
                                            default='confirmed', verbose_name="建造年代可信度")
    length_confidence = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES,
                                         default='confirmed', verbose_name="长度可信度")
    built_year_reason = models.TextField(verbose_name="建造年代推测理由", blank=True, null=True)
    length_reason = models.TextField(verbose_name="长度推测理由", blank=True, null=True)

    # 方案三：互证与质疑机制（统计与争议状态）
    challenge_count = models.IntegerField(default=0, verbose_name="质疑人数")
    evidence_count = models.IntegerField(default=0, verbose_name="补充证据人数")
    dispute_status = models.CharField(max_length=10, choices=DISPUTE_CHOICES,
                                      default='normal', verbose_name="争议状态")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    objects = models.Manager()  # 默认管理器
    def __str__(self):
        return self.name

    @property
    def is_pending(self):
        """是否为待考证状态（用于首页/列表高亮）"""
        return self.dispute_status == 'pending'

    @property
    def has_discovery(self):
        """是否存在探究发现"""
        return bool(self.discovery and self.discovery.strip())

    class Meta:
        verbose_name = "城墙段落"
        verbose_name_plural = "城墙段落"


class WallFeedback(models.Model):
    """城墙段落的互证与质疑反馈（方案三）"""
    FEEDBACK_TYPES = [
        ('evidence', '补充证据'),
        ('challenge', '不同看法'),
    ]
    wall_section = models.ForeignKey(WallSection, on_delete=models.CASCADE,
                                     related_name='feedbacks', verbose_name="城墙段落")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="提交者")
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPES, verbose_name="反馈类型")
    content = models.TextField(verbose_name="内容")
    image = models.ImageField(upload_to='feedback_images/', verbose_name="图片", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.user.username}"

    class Meta:
        verbose_name = "城墙反馈"
        verbose_name_plural = "城墙反馈"
        ordering = ['-created_at']

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
class UserContribution(models.Model):
    """用户贡献内容模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="贡献者")
    name = models.CharField(max_length=100, verbose_name="段落名称", null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="地理位置", null=True, blank=True)
    built_year = models.CharField(max_length=50, verbose_name="建造年代", null=True, blank=True)
    length = models.CharField(max_length=50, verbose_name="长度", null=True, blank=True)
    description = models.TextField(verbose_name="详细描述",null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name="图片", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name if self.name else f"贡献者: {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "用户贡献"
        verbose_name_plural = "用户贡献"