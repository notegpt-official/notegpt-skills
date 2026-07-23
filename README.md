# notegpt-skills

AI Agent Skills 集合 — 覆盖浏览器自动化、音视频转录和完整的 SEO 工作流。

## 目录结构

```
skills/
├── browser-automation/       # 浏览器自动化（反检测）
├── transcript/               # 音视频转文字
└── seo/                      # SEO 自动化管线
    ├── seo-keyword-difficulty/   # 步骤 0：关键词难度分析
    ├── page-seo-generator/       # 步骤 1：英文 SEO 页面生成
    ├── page-seo-generator-i18n/  # 步骤 1：多语言 SEO 页面生成
    ├── seo-image-generator/      # 步骤 2：SEO 配图生成
    └── page-seo-checker/         # 最终步骤：SEO 合规检查
```

---

## 技能概览

### 1. Browser Automation — 浏览器自动化

基于 **CloakBrowser**（预打补丁的 Chromium）实现的反检测浏览器自动化。

| 特性 | 说明 |
|------|------|
| **反检测** | C++ 源码级指纹修补，绕过 reCAPTCHA v3、Cloudflare Turnstile、FingerprintJS |
| **双语言** | JavaScript（Playwright/Puppeteer）和 Python 双 API |
| **拟人化** | Bézier 曲线鼠标路径、逐字符打字延迟、自然滚动物理 |
| **GeoIP** | 根据代理 IP 自动匹配时区和语言环境 |
| **持久化** | 支持持久化用户配置，保持登录态和 Cookie |

**触发词**：scrape XX page、automate filling XX、bypass captcha for XX

---

### 2. Transcript — 音视频转文字

通用的音视频到文本转换工具。

| 来源 | 方法 | 输出格式 |
|------|------|----------|
| **YouTube URL** | yt-dlp 提取字幕（手动字幕 → 自动字幕 → Whisper 兜底） | 纯文本、SRT/VTT、JSON、时间戳片段 |
| **音视频文件** | faster-whisper（CTranslate2 加速，4x 推理速度） | 同上 |

**触发词**：transcribe、transcript、download subtitles、extract text from video、convert audio to text

---

### 3. SEO 自动化管线

#### 步骤 0：[seo-keyword-difficulty](skills/seo/seo-keyword-difficulty/SKILL.md) — 关键词难度分析

**在任何内容生产之前**，评估关键词是否值得做。

- 通过 `seo-web-cafe` MCP 获取真实 KD 分数、搜索量、Top-10 竞品数据
- 支持 **Mode A**（单关键词深度分析）和 **Mode B**（多关键词对比）
- 输出决策报告：🟢 可做 / 🟡 谨慎做 / 🔴 换关键词
- 包含可行性评分公式：`(Volume/1000) × (1-KD/100) × TrendMultiplier × IntentMultiplier`

#### 步骤 1：[page-seo-generator](skills/seo/page-seo-generator/SKILL.md) — 英文 SEO 页面生成

从单个关键词输入生成完整的 **11 列 SEO 落地页**。

**4 阶段工作流**：
1. **关键词研究** — 语义分析、竞品情报、用户画像、KD 分析
2. **竞品 TDK 分析** — 通过 Playwright 抓取竞品真实 Title + Description
3. **TDK 骨架** — 生成 3 个 Title 选项，Python `len()` 验证字符数
4. **11 列完整内容** — 从 Hero 区到 Schema 标记的全页面内容

#### 步骤 1（多语言）：[page-seo-generator-i18n](skills/seo/page-seo-generator-i18n/SKILL.md) — 多语言 SEO 页面生成

面向日语（ja）和中文（zh）市场的原生语言 SEO 内容生成。

- **非机器翻译**：基于英文源页面的信息一致性，独立优化目标语言表达
- 日语：です・ます調，结论先行，子弹点排版
- 中文：简洁直接，短句为主，痛点直击

#### 步骤 2：[seo-image-generator](skills/seo/seo-image-generator/SKILL.md) — SEO 配图生成

为 SEO 页面生成 **4 类视觉素材**：

| 类型 | 比例 | 方式 | 品牌元素 |
|------|------|------|----------|
| Banner | 16:9 | 图生图（需要 Logo） | ✅ Logo + URL |
| 产品介绍 | 1:1 | 文生图 | ❌ 无品牌元素 |
| 为什么选择 | 1:1 | 文生图 | ❌ 无品牌元素 |
| 痛点场景 | 1:1 | 文生图 | ❌ 无品牌元素 |

#### 最终步骤：[page-seo-checker](skills/seo/page-seo-checker/SKILL.md) — 12 点 SEO 合规检查

发布前的**质量闸门**，对已发布页面执行 12 点自动化检查：

| # | 检查项 | 满分 |
|---|--------|------|
| 1 | Title Tag | 10 |
| 2 | Meta Description | 8 |
| 3 | Canonical Tag | 5 |
| 4 | H-Tag 结构 | 8 |
| 5 | Body 内容字数 | 10 |
| 6 | 用户评价真实性 | 5 |
| 7 | FAQ 结构与模式 | 8 |
| 8 | 图片 ALT 标签 | 5 |
| 9 | 内链 | 5 |
| 10 | Schema 结构化数据 | 10 |
| 11 | Hreflang 标签 | 5 |
| 12 | 品牌名计数 & 零冠词 | 5 |

**评分标准**：≥80% 🟢 可发布 / 60-79% 🟡 修复后发布 / <60% 🔴 不可发布

---

## SEO 工作流总览

```
关键词输入
    │
    ▼
┌─────────────────────────┐
│  seo-keyword-difficulty │  ← 步骤 0：这个关键词能做吗？
└───────────┬─────────────┘
            │ 🟢/🟡 通过
            ▼
┌─────────────────────────┐
│  page-seo-generator     │  ← 步骤 1：生成英文 SEO 页面
│  page-seo-generator-i18n│  ← 步骤 1（可选）：生成多语言页面
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  seo-image-generator    │  ← 步骤 2：生成配图素材
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  page-seo-checker       │  ← 最终步骤：发布前质量检查
└─────────────────────────┘
```

---

## 使用方式

这些 Skill 需要在支持 Skill 机制的 AI Agent 环境中使用。每个 Skill 的 `SKILL.md` 文件中定义了完整的触发规则和工作流说明。

将本仓库作为项目目录，Agent 会自动发现并加载 `skills/` 目录下的所有 Skill。
