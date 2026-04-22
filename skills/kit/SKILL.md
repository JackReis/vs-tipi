---
name: kit
description: Surface the right epigenetic input — fetches a prompt kit from Nate's PromptKit matching the query, returns the full kit inline + a suggestion of which prompt inside to run first.
---

# /kit

Epigenetic-input skill. Promptkit = external modulating library; `/kit` is how Jack reaches into it without leaving the Today pane.

## Sequence

1. Take `<query>` arg (e.g. `/kit agent-stack`, `/kit plumbing`, `/kit codex-playbook`).
2. Call `tipi-epigenetics/upstream_for("search_prompt_kits")` → get the canonical upstream tool name.
3. Call that upstream tool (`mcp__nate-promptkit__search_prompt_kits`) with `query=<user-query>`, `limit=3`.
4. Take the top-ranked result, call `mcp__nate-promptkit__get_prompt_kit(id=<top-result.id>)` for full content.
5. Return:
   - Kit name + published date
   - Kit summary (first 5 lines of content)
   - **Which prompt inside to run first** — read the kit, pick the prompt that matches Jack's current arc, explain why in one sentence.
   - Link to the Substack URL for reading alternative prompts.

## If no query

Fall back to `tipi-epigenetics/list_epigenetic_sources()` and show the available upstream search tools. Ask Jack what he's trying to express/refresh/refine.

## Integration with Today chat mode

The Today mode auto-surfaces 3 relevant kits based on today's Top 3 Priorities. `/kit` is the targeted-search escape hatch when auto-surfacing misses.

## Don't

- Don't execute the kit's prompts — return them; Jack decides whether to run.
- Don't cache kits locally — upstream is the source. Fresh fetch each time.
