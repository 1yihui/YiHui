# 如何贡献 Skill

## 格式规范

每个 Skill 目录下必须有 `SKILL.md`，包含以下 frontmatter：

```yaml
---
name: skill-name          # 唯一标识，英文
description: 简短描述      # 一句话说明功能
triggers:                 # 触发词列表，中英文均可
  - 触发词1
  - trigger-word
tags:                    # 标签，用于分类
  - tag1
  - tag2
compatibility: openclaw | claude-code | cursor | ...  # 兼容平台
license: MIT             # 许可证
source: https://...     # 原始项目地址（若有）
---
```

## SKILL.md 结构

```
# Skill: <名称>

## 简介
一句话描述解决的问题。

## 核心功能
- 功能点1
- 功能点2

## 使用时机
什么时候应该激活这个 skill。

## 使用示例
代码示例。

## 注意事项
坑、限制、注意事项。
```

## 提交流程

1. Fork 本仓库
2. 创建 `skills/<your-skill>/SKILL.md`
3. 提交 PR，标题格式：`feat: add <skill-name>`
4. 等待 review

## 审核标准

- frontmatter 完整
- 描述清晰，触发词准确
- 无安全风险（敏感操作有警告）
- 代码示例可运行
