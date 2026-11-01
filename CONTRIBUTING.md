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

## 元数据静态校验

在仓库根目录执行（Python 3.10+）：

```bash
python -m pip install -r scripts/requirements-metadata.txt
python scripts/validate_skill_metadata.py
python -m unittest discover -s tests -p 'test_skill_metadata.py' -v
```

GitHub Actions 会在 push、PR 和手动触发时执行同样的检查。校验范围为
`skills/**/SKILL.md`：检查 frontmatter 分隔符、YAML 语法、各层显式重复键、
非空字符串 `name` / `description`、跨文件名称唯一性，以及正文开头遗留的重复字段。
名称按去除首尾空白后的字符串比较，区分大小写。

为兼容现有技能，允许显示式名称、名称与目录名不同、多行描述、字符串或列表标签、
包含 `|` 的兼容平台字符串、内联 JSON / 嵌套 YAML `metadata` 和扩展字段。
不强制补齐可选字段，也不扫描标题、代码块或说明段落之后的 YAML 示例。
正文需要展示元数据时应使用代码块。

名称变更的兼容性说明及本次全量检查结果见 [元数据检查记录](docs/skill-metadata-audit.md)。
