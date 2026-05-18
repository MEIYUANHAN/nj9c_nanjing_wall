# Cloudinary 媒体文件配置指南

## 为什么需要 Cloudinary？

Railway 服务器的文件系统是**临时的**：每次重新部署后，之前上传的文件都会消失。
同时，`.gitignore` 中包含了 `media/`，所以图片不会随 git push 上传到服务器。

解决方案：把所有媒体文件（用户上传的图片等）存储到 **Cloudinary 云端**，
Django 通过 `django-cloudinary-storage` 自动对接。

---

## 第一步：注册 Cloudinary 账号

1. 打开 [https://cloudinary.com](https://cloudinary.com)
2. 点击右上角 **Sign Up for Free**
3. 填写邮箱、密码，完成注册
4. 登录后进入 **Dashboard（仪表盘）**

---

## 第二步：获取 CLOUDINARY_URL

登录后，在 Dashboard 首页可以看到：

```
Account Details
Cloud Name: xxxxxxx
API Key:    000000000000000
API Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

将这三个值组合成以下格式的 URL：

```
cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

例如：
```
cloudinary://123456789012345:abc123XYZ@my-cloud-name
```

---

## 第三步：在 Railway 添加环境变量

1. 打开 [https://railway.app](https://railway.app)，进入你的项目
2. 点击你的服务（Django 应用），选择 **Variables** 选项卡
3. 点击 **New Variable**，添加：
   - 变量名：`CLOUDINARY_URL`
   - 变量值：`cloudinary://API_KEY:API_SECRET@CLOUD_NAME`（替换为真实值）
4. 点击 **Add** 保存
5. Railway 会自动重新部署

---

## 第四步：重新上传现有图片

Railway 部署成功后，旧的图片记录（`media/static/cq1.jpeg` 等）虽然路径还在数据库里，
但对应文件已经在 Cloudinary 账号下不存在。你需要：

1. 登录网站后台 `/admin/`
2. 进入 **Wall sections**（城墙段落）和 **User contributions**（用户贡献）
3. 逐条编辑，重新上传图片文件
4. 保存后，图片会自动上传到 Cloudinary，数据库中的路径会自动更新

或者，可以使用 Cloudinary 控制台的 **Media Library** 手动上传图片，
然后在 Django admin 中填入对应的 Cloudinary 图片 URL。

---

## 验证是否正常工作

部署后，在后台上传一张新图片，如果上传成功且能在前台正常显示，说明配置正确。
图片的 URL 应该类似：`https://res.cloudinary.com/你的cloud-name/image/upload/xxx.jpg`

---

## 本地开发说明

本地开发时，只要不设置 `CLOUDINARY_URL` 环境变量，
Django 就会自动使用本地文件系统（`media/` 目录），和之前完全一样。
