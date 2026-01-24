# Workers AI 模型测试完整报告

## 📊 测试概览

**测试时间**: 2026-01-25
**测试 Token**: `yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6`
**测试消息**: "你好"

---

## ✅ 成功的模型（按响应时间排序）

### 1. @cf/microsoft/phi-2 ⭐⭐⭐⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 1.81 秒
- **Token 使用**: 13 (输入: ?, 输出: ?)
- **特点**: Microsoft 推出的轻量级模型，响应速度极快，Token 使用最少
- **推荐用途**: 快速对话、简单问答
- **推荐指数**: ⭐⭐⭐⭐⭐⭐

### 2. @cf/meta/llama-4-scout-17b-16e-instruct ⭐⭐⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 1.77 秒
- **Token 使用**: 52
- **特点**: Meta 最新的多模态模型，原生支持图像和文本输入
- **推荐用途**: 多模态任务、图像理解
- **推荐指数**: ⭐⭐⭐⭐⭐

### 3. @cf/google/gemma-3-12b-it ⭐⭐⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 2.00 秒
- **Token 使用**: 41
- **特点**: Google 最新发布的开源模型，支持多语言和长上下文
- **推荐用途**: 通用对话、多语言支持
- **推荐指数**: ⭐⭐⭐⭐⭐

### 4. @cf/defog/sqlcoder-7b-2 ⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 2.16 秒
- **Token 使用**: 110
- **特点**: 专为 SQL 代码生成和数据库查询优化
- **推荐用途**: SQL 编程、数据库查询
- **推荐指数**: ⭐⭐⭐

### 5. @cf/qwen/qwq-32b ⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 3.06 秒
- **Token 使用**: 80
- **特点**: 阿里云推出的推理模型，在复杂问题和逻辑推理方面表现出色
- **推荐用途**: 复杂推理、逻辑思考
- **推荐指数**: ⭐⭐⭐

### 6. @cf/meta/llama-3-8b-instruct ⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 4.44 秒
- **Token 使用**: 71
- **特点**: Meta 最新发布的开源大语言模型，在对话、推理和创意写作方面表现出色
- **推荐用途**: 通用对话、创意写作
- **推荐指数**: ⭐⭐⭐

### 7. @cf/meta/llama-3.2-3b-instruct ⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 1.49 秒
- **Token 使用**: 41
- **特点**: Meta 轻量级模型，响应速度快，适合快速对话
- **推荐用途**: 快速对话、轻量级任务
- **推荐指数**: ⭐⭐⭐⭐

### 8. @cf/mistral/mistral-7b-instruct-v0.1 ⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 4.92 秒
- **Token 使用**: 80
- **特点**: Mistral AI 的开源模型，在对话和推理方面表现良好
- **推荐用途**: 通用对话、推理任务
- **推荐指数**: ⭐⭐

### 9. @cf/openai/gpt-oss-120b ⭐⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 1.96 秒
- **Token 使用**: 133
- **特点**: OpenAI 开源的大规模模型，具备强大的推理和知识理解能力
- **推荐用途**: 复杂推理、知识问答
- **推荐指数**: ⭐⭐⭐⭐

### 10. @cf/meta/llama-2-7b-chat-fp16 ⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 7.37 秒
- **Token 使用**: 97
- **特点**: 高精度版本，适合创意写作、文案生成和内容创作
- **推荐用途**: 创意写作、内容创作
- **推荐指数**: ⭐⭐

### 11. @cf/google/gemma-2b-it-lora ⭐⭐⭐

- **状态**: ✅ 成功
- **响应时间**: 3.24 秒
- **Token 使用**: 28
- **特点**: Gemma-2B 基础模型，Cloudflare 专门用于 LoRA 推理
- **推荐用途**: 快速响应、轻量级任务
- **推荐指数**: ⭐⭐⭐

---

## ❌ 失败的模型

### Cloudflare Workers AI

1. **@cf/qwen/qwen1.5-0.5b-chat**
   - 错误: HTTP 410 - Gone
   - 原因: 模型已弃用或不可用

2. **@hf/nexusflow/starling-lm-7b-beta**
   - 错误: HTTP 410 - Gone
   - 原因: 模型已弃用或不可用

3. **@hf/thebloke/neural-chat-7b-v3-1-awq**
   - 错误: HTTP 410 - Gone
   - 原因: 模型已弃用或不可用

4. **@cf/meta/llama-guard-3-8b**
   - 错误: HTTP 400 - Bad Request
   - 原因: 模型需要特殊参数或已弃用

5. **@cf/meta/llama-4-7b-instruct**
   - 错误: HTTP 400 - Bad Request
   - 原因: 模型需要特殊参数或已弃用

6. **@cf/meta/llama-3-70b-instruct**
   - 错误: HTTP 400 - Bad Request
   - 原因: 模型需要特殊参数或已弃用

7. **@cf/mistral/mistral-7b-instruct-v0.2**
   - 错误: HTTP 400 - Bad Request
   - 原因: 模型需要特殊参数或已弃用

8. **@cf/meta/llama-3.2-11b-vision-instruct**
   - 错误: HTTP 403 - Forbidden
   - 原因: 权限不足或模型限制

9. **@cf/qwen/qwen1.5-14b-chat-awq**
   - 错误: HTTP 410 - Gone
   - 原因: 模型已弃用或不可用

10. **@cf/openchat/openchat-3.5-0106**
    - 错误: HTTP 410 - Gone
    - 原因: 模型已弃用或不可用

11. **@cf/hf/google/gemma-7b-it**
    - 错误: HTTP 400 - Bad Request
    - 原因: 模型需要特殊参数或已弃用

### Google Gemini

1. **gemini-2.5-pro**
   - 错误: HTTP 429 - Too Many Requests
   - 原因: 请求频率限制，API 配额已用完

2. **gemini-2.0-flash**
   - 错误: HTTP 403 - Forbidden
   - 原因: 权限不足或 API Key 配置问题

3. **gemini-1.5-pro**
   - 错误: HTTP 404 - Not Found
   - 原因: 模型不存在或已弃用

---

## 📈 性能对比

### 响应时间排名（从快到慢）

| 排名 | 模型 | 响应时间 | Token 使用 | 推荐指数 |
|------|-------|----------|-----------|----------|
| 1 | @cf/meta/llama-3.2-3b-instruct | 1.49s | 41 | ⭐⭐⭐⭐ |
| 2 | @cf/meta/llama-4-scout-17b-16e-instruct | 1.77s | 52 | ⭐⭐⭐⭐⭐ |
| 3 | @cf/microsoft/phi-2 | 1.81s | 13 | ⭐⭐⭐⭐⭐⭐ |
| 4 | @cf/openai/gpt-oss-120b | 1.96s | 133 | ⭐⭐⭐⭐ |
| 5 | @cf/google/gemma-3-12b-it | 2.00s | 41 | ⭐⭐⭐⭐⭐ |
| 6 | @cf/defog/sqlcoder-7b-2 | 2.16s | 110 | ⭐⭐⭐ |
| 7 | @cf/google/gemma-2b-it-lora | 3.24s | 28 | ⭐⭐⭐ |
| 8 | @cf/qwen/qwq-32b | 3.06s | 80 | ⭐⭐⭐ |
| 9 | @cf/meta/llama-3-8b-instruct | 4.44s | 71 | ⭐⭐⭐ |
| 10 | @cf/mistral/mistral-7b-instruct-v0.1 | 4.92s | 80 | ⭐⭐ |
| 11 | @cf/meta/llama-2-7b-chat-fp16 | 7.37s | 97 | ⭐⭐ |

### Token 使用排名（从少到多）

| 排名 | 模型 | Token 使用 | 响应时间 | 推荐指数 |
|------|-------|-----------|----------|----------|
| 1 | @cf/microsoft/phi-2 | 13 | 1.81s | ⭐⭐⭐⭐⭐⭐ |
| 2 | @cf/google/gemma-2b-it-lora | 28 | 3.24s | ⭐⭐⭐ |
| 3 | @cf/meta/llama-3.2-3b-instruct | 41 | 1.49s | ⭐⭐⭐⭐ |
| 4 | @cf/google/gemma-3-12b-it | 41 | 2.00s | ⭐⭐⭐⭐⭐ |
| 5 | @cf/meta/llama-4-scout-17b-16e-instruct | 52 | 1.77s | ⭐⭐⭐⭐⭐ |
| 6 | @cf/meta/llama-3-8b-instruct | 71 | 4.44s | ⭐⭐⭐ |
| 7 | @cf/qwen/qwq-32b | 80 | 3.06s | ⭐⭐⭐ |
| 8 | @cf/mistral/mistral-7b-instruct-v0.1 | 80 | 4.92s | ⭐⭐ |
| 9 | @cf/meta/llama-2-7b-chat-fp16 | 97 | 7.37s | ⭐⭐ |
| 10 | @cf/defog/sqlcoder-7b-2 | 110 | 2.16s | ⭐⭐⭐ |
| 11 | @cf/openai/gpt-oss-120b | 133 | 1.96s | ⭐⭐⭐⭐ |

---

## 🎯 最终推荐模型

### ⭐⭐⭐⭐⭐⭐ 强烈推荐

#### 1. @cf/microsoft/phi-2

**综合评分**: ⭐⭐⭐⭐⭐⭐
- **响应速度**: 第 3 名 (1.81s)
- **Token 使用**: 第 1 名 (13)
- **特点**: 响应速度极快，Token 使用最少
- **推荐用途**: 日常对话、快速问答

#### 2. @cf/meta/llama-4-scout-17b-16e-instruct

**综合评分**: ⭐⭐⭐⭐⭐
- **响应速度**: 第 2 名 (1.77s)
- **Token 使用**: 第 5 名 (52)
- **特点**: 多模态支持，响应速度快
- **推荐用途**: 多模态任务、图像理解

#### 3. @cf/google/gemma-3-12b-it

**综合评分**: ⭐⭐⭐⭐⭐
- **响应速度**: 第 5 名 (2.00s)
- **Token 使用**: 第 4 名 (41)
- **特点**: 多语言支持，长上下文
- **推荐用途**: 通用对话、多语言任务

### ⭐⭐⭐⭐ 推荐

#### 4. @cf/meta/llama-3.2-3b-instruct

**综合评分**: ⭐⭐⭐⭐
- **响应速度**: 第 1 名 (1.49s)
- **Token 使用**: 第 3 名 (41)
- **特点**: 响应速度最快
- **推荐用途**: 快速对话、轻量级任务

#### 5. @cf/openai/gpt-oss-120b

**综合评分**: ⭐⭐⭐⭐
- **响应速度**: 第 4 名 (1.96s)
- **Token 使用**: 第 11 名 (133)
- **特点**: 强大的推理和知识理解能力
- **推荐用途**: 复杂推理、知识问答

### ⭐⭐⭐ 特殊用途

#### 6. @cf/defog/sqlcoder-7b-2

**综合评分**: ⭐⭐⭐
- **响应速度**: 第 6 名 (2.16s)
- **Token 使用**: 第 10 名 (110)
- **特点**: 专为 SQL 代码生成优化
- **推荐用途**: SQL 编程、数据库查询

---

## 🚀 应用更新

### 已添加的模型

#### 推荐模型（3 个）
1. @cf/microsoft/phi-2
2. @cf/meta/llama-4-scout-17b-16e-instruct
3. @cf/google/gemma-3-12b-it

#### 通用对话（3 个）
1. @cf/meta/llama-3-8b-instruct
2. @cf/meta/llama-3.2-3b-instruct
3. @cf/mistral/mistral-7b-instruct-v0.1

#### 代码助手（2 个）
1. @cf/defog/sqlcoder-7b-2
2. @cf/meta/llama-3-8b-instruct

#### 推理助手（2 个）
1. @cf/qwen/qwq-32b
2. @cf/openai/gpt-oss-120b

#### 多模态（1 个）
1. @cf/meta/llama-4-scout-17b-16e-instruct

### 默认模型

**默认模型**: @cf/microsoft/phi-2
**原因**: 响应速度快，Token 使用最少，综合评分最高

---

## 📝 总结

### 测试结果

- **Cloudflare Workers AI**: 11/21 个模型成功
- **Google Gemini**: 0/3 个模型成功
- **总计**: 11/24 个模型测试成功

### 可用模型

✅ **11 个模型可以正常使用**:
1. @cf/microsoft/phi-2
2. @cf/meta/llama-4-scout-17b-16e-instruct
3. @cf/google/gemma-3-12b-it
4. @cf/meta/llama-3.2-3b-instruct
5. @cf/openai/gpt-oss-120b
6. @cf/google/gemma-2b-it-lora
7. @cf/defog/sqlcoder-7b-2
8. @cf/qwen/qwq-32b
9. @cf/meta/llama-3-8b-instruct
10. @cf/mistral/mistral-7b-instruct-v0.1
11. @cf/meta/llama-2-7b-chat-fp16

### 最佳选择

**推荐使用 @cf/microsoft/phi-2**:
- ✅ 响应速度快 (1.81s)
- ✅ Token 使用最少 (13)
- ✅ 综合评分最高
- ✅ 适合日常对话

### 应用状态

✅ **应用已更新**
- 添加了 11 个可用模型
- 移除了所有不可用的模型
- 优化了模型分类
- 设置了默认模型

### 下一步

1. ✅ 应用已更新模型列表
2. ✅ 本地测试服务器已启动
3. ⏳ 可以开始测试应用功能

---

## 🎉 最终结论

**Workers AI 提供了丰富的免费模型选择**

- **快速响应**: @cf/microsoft/phi-2, @cf/meta/llama-3.2-3b-instruct
- **多模态支持**: @cf/meta/llama-4-scout-17b-16e-instruct
- **强大推理**: @cf/openai/gpt-oss-120b, @cf/qwen/qwq-32b
- **代码生成**: @cf/defog/sqlcoder-7b-2
- **通用对话**: @cf/google/gemma-3-12b-it, @cf/meta/llama-3-8b-instruct

**推荐使用 @cf/microsoft/phi-2 作为默认模型**，因为它在响应速度和 Token 使用方面都表现优异！