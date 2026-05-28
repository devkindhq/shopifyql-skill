# Open Source Growth Playbook

Learnings from building `devkindhq/shopifyql-skill` into a well-structured, SEO-optimized open source project.

---

## 1. README Structure (Order Matters)

**What converts visitors to stars:**

```
1. Badges row (first line, before any heading)
2. H1 + one-liner value prop ("X for Y" format)
3. Hero GIF/screenshot (visitors decide in 10-15 seconds)
4. Quick Install (FIRST code block — highest conversion placement)
5. "Why this over X" comparison table
6. Who It's For (3 personas, one sentence each)
7. What It Does (5-6 bullets max)
8. Quick Start (numbered steps, <15 lines)
9. ... technical docs come AFTER the pitch
```

**Key insight:** Most READMEs lead with "What is X?" — that educates but doesn't sell. Lead with value proposition, install command, and social proof.

---

## 2. SEO for GitHub Repos

### Keywords (plugin.json / package.json)
- Expand from 8 to **20 keywords**
- Include variations: `shopify`, `shopifyql`, `shopify-analytics`, `shopify-plus`
- Include ecosystem terms: `claude-code-plugin`, `ai-analytics`

### GitHub Topics (set in repo settings)
- Use **12 topics** max
- Put primary keyword first: `shopifyql` → `shopify` → `analytics`
- **Claim empty topics** — if no repo uses `shopifyql` as a topic, you become the #1 result instantly

### Backlinks in README
Place service/company links **near the top** (within first 1/3 of README):
```markdown
Built by **[Devkind](https://devkind.com.au)** — specialising in 
**[Shopify Plus development](https://example.com/shopify-plus)** and 
**[AI platform services](https://example.com/ai-services)**.
```
Scrapers and indexers weight content by position.

---

## 3. Community Infrastructure

### Required Files (.github/)

| File | Purpose |
|------|---------|
| `CONTRIBUTING.md` | Invites PRs, reduces friction |
| `SECURITY.md` | Shows maturity, triggers GitHub badge |
| `ISSUE_TEMPLATE/bug_report.md` | Structured bug reports |
| `ISSUE_TEMPLATE/feature_request.md` | Captures ideas |
| `ISSUE_TEMPLATE/[custom].md` | Unique to your project (we did "Share a Query") |
| `PULL_REQUEST_TEMPLATE.md` | Consistent PRs |

### Seed Content
- Create **5 "good-first-issue" labeled issues** immediately — appears in GitHub's discovery feed
- Enable **GitHub Discussions** with 3 seed posts (Show & Tell, Q&A, Ideas)
- Create a **Release** (even if v1.0.0) — shows the repo is maintained

---

## 4. Examples Directory

```
examples/
  README.md          ← index with links
  category-a/
    example-1.md
    example-2.md
  category-b/
    example-3.md
```

Each example file template:
```markdown
# [Title]

**Use case:** [One sentence]
**Tables/API:** `[resource]`

## Code
\`\`\`language
[copy-paste ready code]
\`\`\`

## What this returns
[Explanation]

## Variations
[2-3 alternatives]
```

**Why it works:**
- Each example is a **landing page** for long-tail searches
- Copy-paste ready = immediate value = stars
- Variations show depth without separate files

---

## 5. Plugin/Package Simplicity

**Before:** 
```bash
/plugin marketplace add devkindhq/shopifyql-skill
/plugin install shopifyql@shopifyql-skill
```

**After:**
```bash
/plugin install devkindhq/shopifyql-skill
```

**Lesson:** Remove intermediate concepts (marketplace.json) when a single file (plugin.json) suffices. Every extra step loses users.

---

## 6. Credentials & Security

**Never:**
- Accept tokens as CLI arguments (visible in shell history)
- Auto-load `.env` files (risk of committing)
- Pass credentials through AI context

**Do:**
- Read from OS environment variables: `os.environ.get('TOKEN')`
- Document the `export` command for `~/.zshrc` or `~/.bashrc`
- Provide a setup wizard that guides but doesn't store

---

## 7. Distribution Strategy (Star Acquisition)

### Awesome Lists (Immediate Exposure)
Submit PRs to:
1. **Ecosystem lists** — `awesome-claude-skills`, `awesome-claude-code`
2. **Domain lists** — `awesome-shopify`
3. **Language lists** — `awesome-python` (if applicable)

### Coordinated 48-Hour Launch
```
T+0h   Hacker News (Show HN) — 9-11am US Eastern, Tue/Wed
T+2h   Reddit r/[primary-community]
T+4h   Reddit r/[secondary-community]
T+8h   Reddit r/[tertiary-community]
T+12h  Product Hunt (submit 12:01am PST)
T+24h  Dev.to article
T+36h  Twitter/X thread
```

**Why concentrated:** GitHub Trending triggers on **50+ stars in 24h**. Spreading launches dilutes impact.

---

## 8. What Drives Stars (Research Summary)

| Factor | Impact |
|--------|--------|
| Hero GIF (auto-playing demo) | **Highest** — visitors decide in 10-15 sec |
| One-command install | High — reduces friction |
| Comparison table vs alternatives | High — answers "why this?" |
| Star history chart embed | Medium — social proof loop |
| Active issues/PRs | Medium — signals life |
| Badges row | Medium — quick trust signals |
| Comprehensive README | 3x more stars, 5x more contributions |

---

## 9. Technical SEO Signals

```markdown
[![Star History](https://api.star-history.com/svg?repos=owner/repo&type=Date)](https://star-history.com/#owner/repo)
```

This creates a **reinforcing loop**: spike in stars → chart shows momentum → more stars attracted by social proof.

---

## 10. Cross-Platform = Larger Audience

```markdown
Also works with **Cursor**, **Codex CLI**, and **Gemini CLI** — 
drop `skills/[name]/SKILL.md` into any AI coding tool.
```

One skill file, 4x the potential users. Include copy commands:
```bash
cp skills/name/SKILL.md .cursor/rules/name.md  # Cursor
```

---

## Summary Checklist

```
□ README: value prop before technical docs
□ README: hero GIF in first 10 lines
□ README: install as FIRST code block
□ README: comparison table
□ README: service backlinks near top
□ Keywords: 20 in package/plugin.json
□ Topics: 12 in GitHub settings
□ .github/: CONTRIBUTING, SECURITY, issue templates
□ examples/: copy-paste ready, categorized
□ Release: at least v1.0.0 published
□ Discussions: enabled with seed posts
□ Issues: 5 good-first-issue labeled
□ Launch: coordinated 48-hour window
□ Awesome lists: PRs submitted
```

---

## Sources

Research compiled from:
- [How to Promote Open Source Projects](https://business.daily.dev/resources/promote-open-source-project-proven-channels/)
- [GitHub Open Source in 2026](https://github.blog/open-source/maintainers/what-to-expect-for-open-source-in-2026/)
- [10 GitHub README Examples That Get Stars](https://blog.beautifulmarkdown.com/10-github-readme-examples-that-get-stars)
- [AFFiNE GitHub Stars: 60K+ Playbook](https://dev.to/iris1031/how-to-get-more-github-stars-the-definitive-guide-33k-stars-case-study-2kjo)
- Analysis of top Claude Code skill repos (ComposioHQ, travisvn, hesreallyhim)
