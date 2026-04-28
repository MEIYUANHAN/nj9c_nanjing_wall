from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WallSection, HistoricalEvent

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
    """用户贡献内容表单"""
    class Meta:
        
        model = WallSection
        fields = ['name', 'location', 'built_year', 'length', 'description','event', 'image']  # 将'address'字段添加到字段列表中
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
