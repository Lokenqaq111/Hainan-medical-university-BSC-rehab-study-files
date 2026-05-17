# 英方作业辅助工具库

这个目录用来放置在英方课程作业(论文写作、引用、文献检索等)中能直接复用的小工具。
目标是把零散的提示词、引用规则、文档处理流程沉淀为可调用的"技能(Skill)"，
方便后续同学在不同 AI 客户端里直接加载使用，少重复造轮子。

## 当前收录的工具

| 工具 | 用途 | 适用场景 |
| --- | --- | --- |
| [`uwe-bristol-harvard-reference-generator`](./uwe-bristol-harvard-reference-generator) | 按 UWE Bristol Harvard 规范生成参考文献条目与正文引用，支持期刊文章、article-number 期刊、网页/机构报告，以及对 DOCX 参考文献清单的批量修订 | 写 UWE 英方课程论文、references 整理与校对 |
| [`pubmed-search-casp`](./pubmed-search-casp) | 跑完整的循证文献检索流程：从作业 brief 与课件出发构建 PubMed 检索式、保存检索结果、做 PRISMA 筛选、用 CASP 做质量评价，最后产出可纳入的中/高质量文献清单 | 英方 EPSP(Exercise Prescription for Special Populations)等需要 PubMed 检索 + PRISMA + CASP 的循证作业 |

后续如有新增工具，请保持"一个工具一个子目录 + 一个 `SKILL.md`"的结构。

## 这些工具是什么

每个工具的本体就是一个 `SKILL.md` 文件——它是一段写给 AI 的结构化提示词，
用 YAML frontmatter 描述工具用途，用正文写规则、流程和示例。
AI 客户端把它加载进上下文之后，你只要说"帮我生成 UWE Harvard 参考文献"，
模型就会按照里面定义的规则输出，而不是自由发挥。

## 怎么用

下面分客户端列出加载方式。**所有方式都需要先把工具内容(`SKILL.md`)交给 AI**，
区别只在交付方式不同。

### 1. Claude Code (官方 CLI，推荐)

Claude Code 原生支持 skill 协议，把工具目录放到 `~/.claude/skills/` 即可被识别。

```bash
# 克隆/更新本仓库到本地任意位置后:
mkdir -p ~/.claude/skills
cp -r 英方作业辅助工具库/uwe-bristol-harvard-reference-generator ~/.claude/skills/
cp -r 英方作业辅助工具库/pubmed-search-casp ~/.claude/skills/
```

之后在 Claude Code 会话里直接输入:

```
/uwe-bristol-harvard-reference-generator
```

也可以自然语言触发，比如"帮我用 UWE Harvard 格式整理这段引用"。

### 2. Hermes Agent (第三方长驻 harness)

Hermes 的技能目录在 `~/.hermes/skills/`，按类别组织。建议放到 `research/` 下:

```bash
mkdir -p ~/.hermes/skills/research
cp -r 英方作业辅助工具库/uwe-bristol-harvard-reference-generator ~/.hermes/skills/research/
cp -r 英方作业辅助工具库/pubmed-search-casp ~/.hermes/skills/research/
```

Hermes 启动后会自动加载技能库，使用方式与 Claude Code 类似。

### 3. Codex CLI / openclaw 等其他 harness

这类 harness 目前没有统一的 skill 协议，但都支持系统提示词或自定义指令。
做法是把 `SKILL.md` 的全文作为**首轮系统提示词**或**项目级 `CLAUDE.md` / `AGENTS.md`** 喂给模型:

```bash
# 例: 直接把内容拼到项目根目录的 AGENTS.md 里
cat 英方作业辅助工具库/uwe-bristol-harvard-reference-generator/SKILL.md >> AGENTS.md
```

之后正常发起对话即可。

### 4. Claude.ai / Codex 网页客户端

网页端没有文件系统访问权限，最简单的做法是:

1. 打开对应工具的 `SKILL.md`(例如
   [`uwe-bristol-harvard-reference-generator/SKILL.md`](./uwe-bristol-harvard-reference-generator/SKILL.md) 或
   [`pubmed-search-casp/SKILL.md`](./pubmed-search-casp/SKILL.md))复制全文
2. 新建一个会话，把全文作为第一条消息发送，并在末尾追加你的具体需求
   (例如"现在帮我生成下面这条 DOI 的 UWE Harvard 引用: 10.1136/bmj-2023-077934")

如果是 Claude.ai 的 **Projects** 功能，可以把 `SKILL.md` 内容粘到 Project 的
"Custom instructions"里，之后这个 Project 下的所有会话都会自动加载。

## 工具更新与贡献

- 工具改动直接修改对应子目录里的 `SKILL.md`，并在本 README 的工具表里同步说明
- 新增工具时，建议在子目录里只放一个 `SKILL.md`，避免引入二进制或大文件
- 命名用全小写英文 + 连字符(例: `apa7-reference-generator`)，方便跨客户端识别
- 涉及隐私/学校内部资料的处理流程，提交前请先参考根目录的[隐私脱敏指南](../隐私脱敏指南.md)

## 备注

- 这些工具不替代你自己的判断。AI 给出的引用、改写、翻译结果仍需逐条核对，
  尤其是涉及作者姓名、期刊卷期、DOI 这种容易出错的字段
- 工具本身不联网。需要联网查 Crossref / PubMed 的流程，依赖你所在 harness 的网络能力
