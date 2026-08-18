import logging

from openai import OpenAI
from django.conf import settings

logger = logging.getLogger(__name__)


def check_content_with_deepseek(content, api_key=None):
    """
    使用DeepSeek API审核用户上传的内容
    
    Args:
        content: 要审核的内容字符串
        api_key: DeepSeek API密钥，如果为None则使用settings中的配置
    
    Returns:
        tuple: (is_approved, message)
            - is_approved: 内容是否通过审核
            - message: 审核结果说明
    """
    if api_key is None:
        api_key = settings.DEEPSEEK_API_KEY
    
    # 如果API密钥未配置
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        if getattr(settings, 'DEEPSEEK_MODERATION_FAIL_CLOSED', False):
            return False, "未配置审核密钥且处于严格模式，已拒绝提交（请配置 DEEPSEEK_API_KEY 或关闭严格模式）"
        return True, "API密钥未配置，已跳过审核（仅开发环境）"
    
    try:
        # 创建OpenAI客户端（DeepSeek兼容OpenAI API格式）
        client = OpenAI(
            api_key=api_key,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        
        # 调用DeepSeek API进行内容审核
        # 注意：DeepSeek 当前可用的对话模型是 deepseek-chat / deepseek-reasoner，
        # 并不存在 "deepseek-v4-flash"，使用错误模型名会导致 404 而使所有投稿被拒绝。
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个内容审核助手。请审核用户提交的内容是否合适发布在介绍南京明城墙的网站上。合适的内容应该：1）与南京明城墙相关 2）不包含暴力、色情、政治敏感等不当内容 3）不是垃圾信息或广告。请只回答'通过'或'不通过：原因'。"},
                {"role": "user", "content": f"请审核以下内容：\n{content}"}
            ],
            stream=False,
        )
        
        # 获取审核结果
        message = response.choices[0].message
        result = (message.content or "").strip()
        
        # 判断审核结果
        if result.startswith("通过"):
            return True, "内容审核通过"
        else:
            # 提取不通过的原因
            reason = result.replace("不通过：", "").replace("不通过:", "")
            return False, f"内容审核未通过：{reason}"
    
    except Exception as e:
        # API 调用失败（网络抖动、额度耗尽、密钥错误等）。
        # 行为受 settings.DEEPSEEK_MODERATION_FAIL_CLOSED 控制：
        #   - 严格模式(True)：直接拒绝提交，避免未审核内容流出（内容安全优先）；
        #   - 宽松模式(False，默认)：放行并告警，保证投稿功能在第三方抖动时仍可可用（依赖人工复核）。
        if getattr(settings, 'DEEPSEEK_MODERATION_FAIL_CLOSED', False):
            logger.warning("DeepSeek 审核服务调用失败，严格模式下已拒绝提交：%s", e)
            return False, "审核服务暂不可用，严格模式下已拒绝提交（请稍后重试或联系管理员）"
        logger.warning("DeepSeek 审核服务调用失败，已放行提交：%s", e)
        return True, "审核服务暂不可用，已放行（建议人工复核）"


def check_contribution_with_deepseek(contribution_data, api_key=None):
    """
    审核用户贡献的内容（包括名称、位置、描述等）
    
    Args:
        contribution_data: 包含贡献信息的字典，如：
            {
                'name': '段落名称',
                'location': '地理位置',
                'description': '详细描述',
                'built_year': '建造年代',
                'length': '长度'
            }
        api_key: DeepSeek API密钥
    
    Returns:
        tuple: (is_approved, message)
    """
    # 将所有相关内容组合成一个字符串进行审核
    content_parts = []
    if contribution_data.get('name'):
        content_parts.append(f"名称：{contribution_data['name']}")
    if contribution_data.get('location'):
        content_parts.append(f"位置：{contribution_data['location']}")
    if contribution_data.get('description'):
        content_parts.append(f"描述：{contribution_data['description']}")
    if contribution_data.get('built_year'):
        content_parts.append(f"建造年代：{contribution_data['built_year']}")
    if contribution_data.get('length'):
        content_parts.append(f"长度：{contribution_data['length']}")
    
    full_content = "\n".join(content_parts)
    
    # 调用内容审核函数
    return check_content_with_deepseek(full_content, api_key)
