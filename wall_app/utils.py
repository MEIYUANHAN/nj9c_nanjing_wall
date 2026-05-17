from openai import OpenAI
from django.conf import settings


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
    
    # 如果API密钥未配置，则跳过审核（仅用于开发测试）
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        return True, "API密钥未配置，已跳过审核（仅开发环境）"
    
    try:
        # 创建OpenAI客户端（DeepSeek兼容OpenAI API格式）
        client = OpenAI(
            api_key=api_key,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        
        # 调用DeepSeek API进行内容审核
        response = client.chat.completions.create(
            model="deepseek-v4-flash",  # 使用flash模型，速度快成本低
            messages=[
                {"role": "system", "content": "你是一个内容审核助手。请审核用户提交的内容是否合适发布在介绍南京明城墙的网站上。合适的内容应该：1）与南京明城墙相关 2）不包含暴力、色情、政治敏感等不当内容 3）不是垃圾信息或广告。请只回答'通过'或'不通过：原因'。"},
                {"role": "user", "content": f"请审核以下内容：\n{content}"}
            ],
            stream=False,
            reasoning_effort="low"  # 低推理 effort，快速响应
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
        # API调用失败，为了不影响用户体验，可以选择通过审核或返回错误
        # 这里选择返回错误，让用户可以稍后重试
        return False, f"审核服务调用失败：{str(e)}"


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
