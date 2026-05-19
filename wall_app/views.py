from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import WallSection, UserContribution, HistoricalEvent
from .forms import UserRegisterForm, UserContributionForm, createhistoricaleventForm
from .utils import check_contribution_with_deepseek  # 导入内容审核函数

def home(request):
    """首页视图"""
    sections = WallSection.objects.all()
    contributions = UserContribution.objects.all()
    return render(request, 'home.html', {
        'sections': sections,
        'contributions': contributions
    })

def section_detail(request, section_id):
    """城墙段落详情视图"""
    section = WallSection.objects.get(id=section_id)
    events = HistoricalEvent.objects.filter(wall_section=section)
    return render(request, 'section_detail.html', {
        'section': section,
        'events': events
    })

def about_page(request):
    return render(request, 'about.html')

def interactive_map(request):
    """交互式地图页面"""
    sections = WallSection.objects.all()
    return render(request, 'interactive_map.html', {'sections': sections})

def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户 {username} 创建成功！现在可以登录了。')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '用户名或密码错误，请重试。')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def user_logout(request):
    #用户注销视图
    logout(request)
    return redirect('home')

@login_required
def create_contribution(request):
    if request.method!= 'POST':
        form = UserContributionForm()
        return render(request, 'create_contribution.html', {'form': form})
    else:
        form = UserContributionForm(data=request.POST, files=request.FILES)  # 注意这里要加上 files=request.FILES，因为有文件上传
        if form.is_valid():
            # 准备审核数据
            contribution_data = {
                'name': form.cleaned_data.get('name', ''),
                'location': form.cleaned_data.get('location', ''),
                'description': form.cleaned_data.get('description', ''),
                'built_year': form.cleaned_data.get('built_year', ''),
                'length': form.cleaned_data.get('length', '')
            }
            
            # 调用DeepSeek API审核内容
            is_approved, message = check_contribution_with_deepseek(contribution_data)
            
            if is_approved:
                # 审核通过，保存贡献
                contribution = form.save(commit=False)
                contribution.user = request.user
                contribution.save()
                messages.success(request, '贡献提交成功！内容已通过审核。')
                return redirect('home')
            else:
                # 审核未通过，返回错误信息
                messages.error(request, f'内容审核未通过：{message}')
                return render(request, 'create_contribution.html', {'form': form})
        else:
            return render(request, 'create_contribution.html', {'form': form})
            

@login_required
def user_contributions(request):
    """用户贡献列表视图"""
    contributions = UserContribution.objects.filter(user=request.user)
    sections = WallSection.objects.filter(user=request.user)
    return render(request, 'user_contributions.html', {'contributions': contributions, 'sections': sections})

@login_required
def user_profile(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    contributions = UserContribution.objects.filter(user=user)
    return render(request, 'user_profile.html', {'user': user, 'contributions': contributions})
def map_view(request):
    """地图视图"""
    sections = WallSection.objects.all()
    return render(request, 'map.html', {'sections': sections})
def history_view(request):
    """历史事件视图"""
    history=HistoricalEvent.objects.all().order_by('-year')
    return render(request, 'history.html', {'history': history})
def picture_gallery(request):
    """图片画廊视图"""
    sections = WallSection.objects.all()
    return render(request, 'picture_gallery.html', {'sections': sections, 'contributions': UserContribution.objects.all()})
def contribution_detail(request, contribution_id):
    """用户贡献详情视图"""
    contribution = get_object_or_404(UserContribution, id=contribution_id)
    return render(request, 'contribution_detail.html', {'contribution': contribution})
def create_historical_event(request):
    """创建历史事件视图"""
    if request.method != 'POST':
        form = createhistoricaleventForm()
        return render(request, 'create_historical_event.html', {'form': form})
    else:
        form = createhistoricaleventForm(request.POST)
        if form.is_valid():
            form.save()  # wall_section 已由表单字段携带，直接保存
            return redirect('home')
        else:
            return render(request, 'create_historical_event.html', {'form': form})
def custom_404(request, exception):
    """自定义404错误页面视图"""
    return render(request, 'errors/404.html', status=404)
def custom_500(request):
    """自定义500错误页面视图"""
    return render(request, 'errors/500.html', status=500)
def custom_403(request, exception):
    """自定义403错误页面视图"""
    return render(request, 'errors/403.html', status=403)
def custom_400(request, exception):
    """自定义400错误页面视图"""
    return render(request, 'errors/400.html', status=400)