# DeepSeek API 配置说明

## 步骤1：注册DeepSeek并获取API密钥

1. 访问 DeepSeek 平台：https://platform.deepseek.com/
2. 注册账号（可以使用邮箱或手机号注册）
3. 登录后，进入 API 密钥管理页面：https://platform.deepseek.com/api_keys
4. 点击"创建API密钥"按钮
5. 复制生成的API密钥（注意：密钥只显示一次，请妥善保管）

## 步骤2：配置API密钥到Django项目

### 方法1：使用环境变量（推荐）

在项目根目录创建 `.env` 文件（如果已存在则跳过）：

```bash
# 在项目根目录（nanjing_wall）创建.env文件
```

在 `.env` 文件中添加：

```
DEEPSEEK_API_KEY=你的API密钥
```

然后安装 `python-dotenv` 来加载环境变量：

```bash
pip install python-dotenv
```

在 `settings.py` 开头添加：

```python
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件中的环境变量
```

### 方法2：直接设置环境变量

**Windows (CMD):**
```cmd
set DEEPSEEK_API_KEY=你的API密钥
```

**Windows (PowerShell):**
```powershell
$env:DEEPSEEK_API_KEY="你的API密钥"
```

**Linux/Mac:**
```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

### 方法3：临时测试（不推荐用于生产环境）

直接在 `settings.py` 中修改：

```python
DEEPSEEK_API_KEY = '你的API密钥'  # 直接写在这里
```

⚠️ **注意**：不要将API密钥提交到Git仓库！请确保 `.env` 文件已添加到 `.gitignore` 中。

## 步骤3：安装依赖包

运行以下命令安装所需的Python包：

```bash
pip install -r requirements.txt
```

这将安装新增的 `openai` 包（用于调用DeepSeek API）。

## 步骤4：测试功能

1. 启动Django开发服务器：
   ```bash
   python manage.py runserver
   ```

2. 登录你的账号

3. 尝试创建一个贡献，提交内容

4. 查看是否成功调用DeepSeek API进行审核

## 故障排除

### 问题1：API密钥配置错误
- 检查环境变量是否正确设置
- 在Django shell中测试：
  ```bash
  python manage.py shell
  ```
  ```python
  from django.conf import settings
  print(settings.DEEPSEEK_API_KEY)  # 应该显示你的API密钥
  ```

### 问题2：API调用失败
- 检查网络连接
- 确认API密钥有效且有足够的余额
- 查看DeepSeek API文档：https://api-docs.deepseek.com/

### 问题3：内容审核不工作
- 检查 `wall_app/utils.py` 文件是否存在
- 检查 `views.py` 中是否正确导入了审核函数
- 查看Django控制台输出的错误信息

## 额外说明

1. **内容审核逻辑**：当前配置使用 `deepseek-v4-flash` 模型进行快速审核。你可以根据需要修改 `utils.py` 中的模型配置。

2. **审核提示词**：在 `utils.py` 的 `check_content_with_deepseek` 函数中，可以修改系统提示词来调整审核标准。

3. **API费用**：DeepSeek API按Token计费，价格非常便宜。建议查看官方定价页面了解详情。

4. **生产环境部署**：在生产环境中，请确保：
   - API密钥通过环境变量配置
   - 不要将密钥提交到代码仓库
   - 考虑添加API调用失败时的降级策略

## 参考资料

- DeepSeek 平台：https://platform.deepseek.com/
- DeepSeek API 文档：https://api-docs.deepseek.com/
- OpenAI Python 客户端文档：https://platform.openai.com/docs/api-reference?lang=python
