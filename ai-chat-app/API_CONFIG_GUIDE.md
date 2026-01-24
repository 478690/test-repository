# Cloudflare Pages AI 绑定配置指南

## 方法3：使用 Cloudflare API 令牌配置

### 步骤1：获取必要信息

#### 1.1 获取 Cloudflare API 令牌

1. 访问 https://dash.cloudflare.com/profile/api-tokens
2. 点击 "Create Token"
3. 选择 "Edit Cloudflare Workers" 模板或自定义权限
4. 设置权限：
   - Account → Workers Scripts → Edit
   - Account → Workers KV Storage → Edit
5. 设置 Account Resources 为你的账户
6. 设置 TTL（过期时间）
7. 点击 "Continue to summary" → "Create Token"
8. **复制并保存令牌**（只显示一次！）

#### 1.2 获取账户 ID

1. 登录 https://dash.cloudflare.com/
2. 在右侧边栏找到 "Account ID"
3. 复制账户 ID

#### 1.3 获取项目名称

1. 进入 Workers & Pages
2. 找到你的项目名称（通常是 "cloudflare-ai-chat"）

### 步骤2：使用 PowerShell 配置

#### 2.1 创建配置脚本

创建文件 `configure-ai-binding.ps1`：

```powershell
# 配置参数
$apiToken = "你的API令牌"
$accountId = "你的账户ID"
$projectName = "cloudflare-ai-chat"

# API 端点
$url = "https://api.cloudflare.com/client/v4/accounts/$accountId/pages/projects/$projectName"

# 请求头
$headers = @{
    "Authorization" = "Bearer $apiToken"
    "Content-Type" = "application/json"
}

# 请求体
$body = @{
    "deployment_configs" = @{
        "production" = @{
            "bindings" = @(
                @{
                    "type" = "ai"
                    "name" = "AI"
                    "model" = "@cf/meta/llama-2-7b-chat-int8"
                }
            )
        }
    }
}

# 发送请求
try {
    $response = Invoke-RestMethod -Uri $url -Method PATCH -Headers $headers -Body ($body | ConvertTo-Json -Depth 10)
    Write-Host "配置成功！"
    Write-Host $response
} catch {
    Write-Host "配置失败：$($_.Exception.Message)"
}
```

#### 2.2 运行脚本

1. 将上面的脚本保存为 `configure-ai-binding.ps1`
2. 替换 `你的API令牌` 和 `你的账户ID`
3. 在 PowerShell 中运行：
   ```powershell
   .\configure-ai-binding.ps1
   ```

### 步骤3：验证配置

#### 3.1 检查项目配置

```powershell
# 获取项目配置
$url = "https://api.cloudflare.com/client/v4/accounts/$accountId/pages/projects/$projectName"
$response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers
$response.deployment_configs.production.bindings
```

#### 3.2 重新部署项目

1. 进入 Cloudflare Dashboard
2. 选择你的 Pages 项目
3. 点击 "Deployments"
4. 点击 "Retry deployment"

### 常见问题

#### Q1: 403 Forbidden 错误
- 检查 API 令牌权限
- 确保令牌有 "Edit Cloudflare Workers" 权限

#### Q2: 404 Not Found 错误
- 检查账户 ID 是否正确
- 检查项目名称是否正确

#### Q3: 400 Bad Request 错误
- 检查请求体格式
- 确保模型名称正确

### 替代方案

如果 API 配置遇到问题，可以使用 Dashboard 手动配置：

1. 进入项目设置
2. 找到 "Functions" 部分
3. 点击 "Create binding"
4. 选择 "AI Binding" 类型
5. 设置 Variable name 为 "AI"
6. 选择模型 "@cf/meta/llama-2-7b-chat-int8"
7. 点击 "Save"

### 注意事项

- API 令牌只显示一次，请妥善保存
- 账户 ID 和项目名称区分大小写
- 配置完成后需要重新部署项目
- 确保你的 Cloudflare 账号有 Workers AI 的使用权限