# 免费方案快速配置指南

## 🆓 方案 1：Vercel 免费部署（最推荐）⭐⭐⭐⭐⭐

### 步骤：

1. **注册 Vercel**
   - 访问：https://vercel.com
   - 点击 "Sign Up"
   - 使用 GitHub 账号注册

2. **导入项目**
   - 登录后，点击 "New Project"
   - 点击 "Import" 导入 GitHub 仓库
   - 选择 `test-repository` 仓库

3. **配置项目**
   - Project Name: `ai-chat-app`（或任意名称）
   - Framework Preset: "Other"
   - Root Directory: `.`（根目录）
   - Build Command: 留空
   - Output Directory: `.`

4. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成（约 1-2 分钟）
   - 获得 Vercel URL（如 `https://ai-chat-app.vercel.app`）

5. **配置环境变量**（如果需要）
   - 进入项目设置 → Environment Variables
   - 添加以下变量：
     - `CLOUDFLARE_ACCOUNT_ID`: `30fdf13d5bb71a81bc6f7c732f244a72`
     - `CLOUDFLARE_API_TOKEN`: `yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6`
     - `GOOGLE_GEMINI_API_KEY`: `AIzaSyCHXQsENnN8ilwrdWqDartcHOvptRsqetA`

6. **测试访问**
   - 访问 Vercel URL
   - 测试所有功能

---

## 🆓 方案 2：Cloudflare Workers 免费代理

### 步骤：

1. **创建 Worker**
   - 访问：https://dash.cloudflare.com
   - 点击 "Workers & Pages"
   - 点击 "Create application"
   - 选择 "Create Worker"
   - 输入名称：`ai-chat-proxy`
   - 点击 "Deploy"

2. **编辑代码**
   - 点击 "Edit code"
   - 替换为以下代码：

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    url.hostname = 'test-repository-9xi.pages.dev';
    
    const response = await fetch(url.toString(), {
      headers: {
        ...request.headers,
        'Host': 'test-repository-9xi.pages.dev'
      }
    });
    
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Access-Control-Allow-Origin', '*');
    newResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    newResponse.headers.set('Access-Control-Allow-Headers', '*');
    
    return newResponse;
  }
};
```

3. **部署**
   - 点击 "Save and Deploy"
   - 记录 Worker URL（如 `https://ai-chat-proxy.your-subdomain.workers.dev`）

4. **使用**
   - 直接访问 Worker URL
   - 或配置自定义域名

---

## 🆓 方案 3：EU.org 免费域名

### 步骤：

1. **申请域名**
   - 访问：https://nic.eu.org
   - 点击 "Register"
   - 填写注册信息
   - 申请域名（如 `yourname.eu.org`）
   - 等待审核（1-2 天）

2. **配置 DNS**
   - 登录 EU.org 控制面板
   - 添加 CNAME 记录：
     ```
     名称: www
     类型: CNAME
     值: test-repository-9xi.pages.dev
     ```

3. **在 Cloudflare Pages 配置**
   - 登录 Cloudflare Dashboard
   - 进入 Pages 项目
   - 点击 "Custom domains"
   - 添加域名：`www.yourname.eu.org`

4. **等待生效**
   - 等待 5-10 分钟
   - 访问新域名

---

## 🆓 方案 4：DuckDNS 免费域名

### 步骤：

1. **注册 DuckDNS**
   - 访问：https://www.duckdns.org
   - 使用 GitHub 或 Google 账号登录

2. **创建子域名**
   - 输入子域名名称（如 `yourname`）
   - 点击 "add domain"
   - 获得域名：`yourname.duckdns.org`

3. **配置 DNS**
   - 在 DuckDNS 控制面板配置 CNAME
   - 指向：`test-repository-9xi.pages.dev`

4. **在 Cloudflare Pages 配置**
   - 添加自定义域名：`yourname.duckdns.org`

---

## 🆓 方案 5：Netlify 免费部署

### 步骤：

1. **注册 Netlify**
   - 访问：https://www.netlify.com
   - 使用 GitHub 账号注册

2. **导入项目**
   - 点击 "Add new site" → "Import an existing project"
   - 选择 GitHub 仓库
   - 选择 `test-repository` 仓库

3. **配置构建**
   - Build command: 留空
   - Publish directory: `.`

4. **部署**
   - 点击 "Deploy site"
   - 等待部署完成
   - 获得 Netlify URL

---

## 🎯 推荐方案

### 最简单：Vercel ⭐⭐⭐⭐⭐
- 完全免费
- 国内访问快
- 配置简单
- 自动部署

### 最稳定：EU.org + Cloudflare ⭐⭐⭐⭐⭐
- 完全免费
- 稳定性好
- 自定义域名

### 最快速：Cloudflare Workers ⭐⭐⭐⭐
- 完全免费
- 配置简单
- 无需域名

---

## 📝 测试工具

- 国内访问测试：https://www.ce.baidu.com
- 网站速度测试：https://www.webpagetest.org
- DNS 查询：https://www.nslookup.io

---

**更新时间**: 2026-01-25
**版本**: v1.0