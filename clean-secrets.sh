#!/bin/bash

# 备份原始分支
git branch backup-branch

# 清理所有包含 API 凭证的提交
git filter-branch --force --index-filter '
  git rm --cached --ignore-unmatch \
    TOKEN_TEST_RESULTS.md \
    TOKEN_SUMMARY.md \
    NEW_TOKEN_TEST_RESULTS.md \
    test-new-token.py \
    test-gemini-token.py \
    test-all-env-variables.py \
    configure-ai-gateway.py \
    test-ai-gateway.py \
    test-ai-gateway-detailed.py \
    test-ai-gateway-formats.py
' --prune-empty --tag-name-filter cat -- --all

# 清理引用
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive