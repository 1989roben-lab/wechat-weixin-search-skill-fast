---
name: wechat-weixin-search-skill-fast
description: Search WeChat Official Account / 微信公众号 news quickly using the local weixin_search MCP fast workflow. Use when the user asks to search WeChat, 微信, 公众号, 搜狗微信, mp.weixin, 微信公众号新闻, latest WeChat articles, company news from public accounts, or wants clean results with dates and reference links.
---

# WeChat News Search

## Workflow

Use the local `weixin_search` MCP fast path for company news discovery. Prefer the MCP tool `weixin_company_news` when available. If the MCP tool is not visible in the current session, run `scripts/weixin_company_news.py`.

Default behavior:

- Return results within about **5 seconds** when possible.
- Use fast search only: do not resolve each result to a real `mp.weixin.qq.com` URL unless the user explicitly asks.
- Output the result table first, without long links inside the table.
- Put reference links at the end as a numbered list.
- Treat 搜狗微信 links as reference/search-result links, not confirmed original article links.

## Search Defaults

For company searches, call `weixin_company_news` with:

- `company`: the company name from the user.
- `topics`: pick 4-8 useful terms based on the company. Common defaults: `2026`, `AI`, `安全`, `算力`, `边缘云`, `CDN`, `出海`, `数据库`, `云计算`, `海外`.
- `exclude_terms`: remove obvious noise such as `招聘`, `校园招聘`, `实习`, `内推`, `培训班`, `课程报名`, and known unrelated brand terms.
- `max_results`: normally `10`.
- `max_workers`: normally `6` to `10`.

If the company name is ambiguous, add exclusion terms rather than asking first when the ambiguity is obvious from the results. Example: for `白山云`, exclude `白山一云`, `白山一雲`, `矿泉水`, `饮品`, `Foodaily`, `春糖`.

## Fallback Script

When the MCP tool is not available directly, run:

```bash
python3 scripts/weixin_company_news.py \
  --company "网宿科技" \
  --topics "2026,AI,CDN,边缘云,算力,安全,海外" \
  --exclude "招聘,校园招聘,实习,内推" \
  --limit 10
```

The script prints JSON with `elapsed` and `items`.

## Output Format

Use this shape by default:

```markdown
搜索耗时：**N.NNN 秒**。

| # | 日期 | 标题 | 命中关键词 |
|---|---|---|---|
| 1 | 2026-05-29 | ... | AI |

**参考链接**

1. [标题简写](搜狗微信链接)
2. [标题简写](搜狗微信链接)
```

Only add business value, sales value, database relevance, or other interpretation when the user explicitly asks for it. Otherwise keep the output neutral: date, title, matched query/topic, and reference links.

## Limitations

- This workflow searches 搜狗微信-indexed public account results; it is not an official WeChat API.
- Result order is 搜狗微信 ranking plus local sorting by parsed publish date.
- Long 搜狗跳转 links can make chat rendering slow. Keep them in the final reference list only.
- Real `mp.weixin.qq.com` links and full article bodies require slower follow-up fetching; do that only for selected high-value items.
