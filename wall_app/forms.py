from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WallSection, HistoricalEvent, WallFeedback

class UserRegisterForm(UserCreationForm):
    """用户注册表单"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class UserContributionForm(forms.ModelForm):
    """用户贡献内容表单（含「慧问慧答」探究增强字段）"""
    class Meta:

        model = WallSection
        fields = [
            'name', 'location', 'built_year', 'length', 'description',
            'event', 'image',
            # 方案一：探究发现
            'discovery',
            # 方案二：双轨可信度
            'built_year_confidence', 'length_confidence',
            'built_year_reason', 'length_reason',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入段落名称'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '请输入段落描述'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入相关地址'
            }),
            'built_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入建造年代'
            }),
            'length': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入长度'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'event': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入相关历史事件'
            }),
            # 方案一：探究发现文本框
            'discovery': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '关于这段城墙，你有什么有趣的发现或猜想？（例如：城砖铭文很特别 / 为什么这里有个缺口？）'
            }),
            # 方案二：可信度单选 + 推测理由
            'built_year_confidence': forms.RadioSelect(attrs={
                'class': 'form-check-input confidence-radio',
            }),
            'length_confidence': forms.RadioSelect(attrs={
                'class': 'form-check-input confidence-radio',
            }),
            'built_year_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '请简述你的推测理由，例如：我推测是明代，因为砖的质地和中华门很像'
            }),
            'length_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '请简述你的推测理由，例如：我推测约 X 米，依据老地图比例估算'
            }),
        }

    def clean(self):
        """校验：选择「我推测」时必须填写推测理由"""
        cleaned = super().clean()
        if cleaned.get('built_year_confidence') == 'guess' and not cleaned.get('built_year_reason'):
            self.add_error('built_year_reason', '选择「我推测」时需填写建造年代推测理由')
        if cleaned.get('length_confidence') == 'guess' and not cleaned.get('length_reason'):
            self.add_error('length_reason', '选择「我推测」时需填写长度推测理由')
        return cleaned


class WallFeedbackForm(forms.ModelForm):
    """城墙段落的互证与质疑反馈表单（方案三）"""
    class Meta:
        model = WallFeedback
        fields = ['feedback_type', 'content', 'image']
        widgets = {
            'feedback_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请输入你的证据说明或不同看法……'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
class createhistoricaleventForm(forms.ModelForm):
    """创建历史事件表单"""
    class Meta:
        model = HistoricalEvent
        fields = ['title', 'year', 'description', 'wall_section']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入事件标题'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 2026,
                'placeholder': '请输入发生年份'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '请输入事件描述'
            }),
            'wall_section': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '请选择相关城墙段落'
            }),
        }
