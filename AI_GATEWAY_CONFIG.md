# Cloudflare AI Gateway 配置指南

## 前提条件
- 账户 ID: `30fdf13d5bb71a81bc6f7c732f244a72`
- AI Gateway Token: `jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI`
- Cloudflare API Token: `fbRWRPmxK-zJyg9QfhCP-JZBar8ZjSjKuMBkvYFP`

## 步骤 1：访问 Cloudflare 控制台

1. 打开浏览器，访问：
   ```
   https://dash.cloudflare.com/30fdf13d5bb71a81bc6f7c732f244a72/ai-gateway
   ```

2. 如果没有 AI Gateway 页面，可能需要先启用：
   - 访问 `https://dash.cloudflare.com/30fdf13d5bb71a81bc6f7c732f244a72/ai-gateway/providers`
   - 或在左侧菜单找到 "AI" 或 "AI Gateway"

## 步骤 2：创建 AI Gateway

1. 点击 **"Create Gateway"** 或 **"创建网关"** 按钮
2. 填写表单：
   - **名称/Name**: `ai-chat-gateway`
   - **描述/Description**: `AI Chat Application Gateway`
3. 点击 **"Create"** 或 **"创建"**

## 步骤 3：配置提供商（Providers）

1. 在创建的网关中，找到 **"Providers"** 或 **"提供商"** 部分
2. 点击 **"Add Provider"** 或 **"添加提供商"**
3. 选择 **"Workers AI"**
4. 配置：
   - **Account ID**: `30fdf13d5bb71a81bc6f7c732f244a72`
   - **API Token**: 使用你的 Cloudflare API Token
5. 点击 **"Save"** 或 **"保存"**

## 步骤 4：配置路由（Routes）

1. 找到 **"Routes"** 或 **"路由"** 部分
2. 点击 **"Add Route"** 或 **"添加路由"**
3. 配置路由：
   - **路径/Path**: `*` 或 `/ai/run/*`
   - **方法/Method**: `POST`
   - **上游/Upstream**: 选择 `Workers AI`
   - **模型/Models**: 
     - `@cf/meta/llama-3-8b-instruct`
     - `@cf/meta/llama-2-7b-chat-int8`
     - `@cf/meta/llama-2-7b-chat-fp16`
     - `@cf/mistral/mistral-7b-instruct-v0.2`
     - `@hf/thebloke/neural-chat-7b-v3-1-awq`
4. 点击 **"Save"** 或 **"保存"**

## 步骤 5：配置缓存（可选但推荐）

1. 找到 **"Cache"** 或 **"缓存"** 部分
2. 启用缓存：
   - **启用/Enabled**: 是
   - **TTL**: 300 秒（5分钟）
3. 点击 **"Save"** 或 **"保存"**

## 步骤 6：配置速率限制（可选但推荐）

1. 找到 **"Rate Limiting"** 或 **"速率限制"** 部分
2. 配置限制：
   - **请求数/Requests**: 100
   - **时间窗口/Time Window**: 60 秒
3. 点击 **"Save"** 或 **"保存"**

## 步骤 7：获取网关信息

配置完成后，记录以下信息：
- **Gateway URL**: `https://gateway.ai.cloudflare.com/v1/30fdf13d5bb71a81bc6f7c732f244a72`
- **Token**: `jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI`

## 步骤 8：测试配置

1. 运行测试脚本：
   ```bash
   python test-ai-gateway.py
   ```

2. 如果看到 "✅ Success!"，说明配置成功
3. 如果看到 "❌ HTTP Error: 403"，需要检查：
   - 路由是否正确配置
   - Token 权限是否正确
   - 模型是否在允许列表中

## 常见问题

### Q1: 找不到 AI Gateway 页面
**A**: AI Gateway 可能需要在 Cloudflare 控制台中启用。访问：
- `https://dash.cloudflare.com/30fdf13d5bb71a81bc6f7c732f244a72/ai-gateway/providers`

### Q2: 403 Forbidden 错误
**A**: 检查以下几点：
1. 路由是否正确配置
2. Token 是否有正确的权限
3. 模型是否在允许列表中
4. AI Gateway 是否已启用

### Q3: 如何查看 AI Gateway 日志
**A**: 在 Cloudflare 控制台中：
1. 进入 AI Gateway 页面
2. 找到 **"Analytics"** 或 **"分析"** 部分
3. 查看请求日志、错误和性能指标

### Q4: 如何添加 Google Gemini
**A**: 在 AI Gateway 中：
1. 找到 **"Providers"** 部分
2. 点击 **"Add Provider"**
3. 选择 **"Google AI Studio"** 或 **"Google Gemini"**
4. 输入你的 Gemini API Key
5. 保存配置

## 配置验证清单

- [ ] AI Gateway 已创建
- [ ] Workers AI 提供商已添加
- [ ] 路由已配置（路径：`*` 或 `/ai/run/*`）
- [ ] 模型已添加到允许列表
- [ ] 缓存已启用（可选）
- [ ] 速率限制已配置（可选）
- [ ] 测试脚本运行成功

## 联系支持

如果遇到问题：
1. 查看 Cloudflare 文档：https://developers.cloudflare.com/ai-gateway/
2. 访问 Cloudflare 社区：https://community.cloudflare.com/
3. 联系 Cloudflare 支持

## 当前状态

- ✅ 应用已部署到 Cloudflare Pages
- ✅ 直接 API 调用正常工作
- ❌ AI Gateway 需要在控制台中配置
- 🔄 等待用户完成控制台配置

## 下一步

完成上述配置后：
1. 运行 `python test-ai-gateway.py` 验证配置
2. 如果成功，应用会自动使用 AI Gateway
3. 如果失败，应用会回退到直接 API 调用（仍然正常工作）