# Cloudflare AI 对话助手项目

## 项目说明
这是一个基于 Cloudflare Workers AI 的智能对话网页应用，使用 Cloudflare Pages 部署。

## 功能特性
- 美观的对话界面
- 实时 AI 回复
- 基于 Cloudflare Workers AI 的边缘计算
- 全球低延迟响应

## 技术栈
- 前端：HTML5 + CSS3 + JavaScript
- 后端：Cloudflare Workers
- AI 模型：@cf/meta/llama-2-7b-chat-int8

## 部署方法
1. 登录 Cloudflare 账号
2. 选择 "Pages" → "Create a project"
3. 连接 GitHub 仓库
4. 选择仓库：`478690/test-repository`
5. 构建配置：
   - Framework preset: None
   - Build command: `npm run build` (留空)
   - Build output directory: `ai-chat-app/public`
6. 点击 "Save and Deploy"
7. 部署完成后，访问分配的 Pages 域名

## 环境变量
无需额外配置环境变量，Cloudflare Pages 会自动配置 Workers AI 访问权限。

## 本地开发
```bash
# 安装依赖
npm install

# 启动本地开发服务器
npx wrangler dev
```

## 注意事项
- 使用免费计划的 Cloudflare AI 服务，可能有请求次数限制
- 首次部署可能需要几分钟时间初始化
- 确保 Cloudflare 账号已启用 Workers AI 服务