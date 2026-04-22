---
name: kit
description: Surface the right epigenetic input — fetches a prompt kit from Nate's PromptKit matching the query, returns kit details + which prompt to run first. Requires nate-promptkit MCP (configured via NATE_PROMPTKIT_URL env var).
---

# /kit

Epigenetic-input skill. Promptkit = external modulating library; `/kit` is how Jack reaches into it without leaving the Today pane.

## HARD RULES

- You **MUST** call `nate-promptkit/search_prompt_kits` before writing any response. No exceptions.
- If the tool is not available (MCP not registered / env var not set / server failing), **SAY SO EXPLICITLY**: *"nate-promptkit MCP isn't reachable — set NATE_PROMPTKIT_URL and reload the plugin."* Do not improvise.
- If search returns no results, **SAY SO EXPLICITLY**: *"no kits matched query X."* Do not invent a kit name.
- **Never fabricate kit names, dates, IDs, or content.** If you don't have a UUID from a real tool call, you don't have the kit.

## Sequence

1. Take `<query>` arg (e.g. `/tipi:kit agent-stack`, `/tipi:kit plumbing`).
2. Call `nate-promptkit/search_prompt_kits` with `query=<user-query>`, `limit=3`.
3. Verify the returned list is non-empty and each entry has `id`, `name`, `published_at`. If not, follow HARD RULES.
4. For the top-ranked result, call `nate-promptkit/get_prompt_kit(id=<top-result.id>)` to fetch full content.
5. Return:
   - Kit name + published date **exactly as the tool returned**
   - First 5 lines of fetched content, verbatim
   - **Which prompt inside to run first** — pick the one matching Jack's current arc, explain why in one sentence. Say so if the kit has only one prompt.
   - The kit's UUID for reference

## No-query fallback

If Jack types `/tipi:kit` with no args, call `nate-promptkit/list_prompt_kits(limit=10)`, show the list, ask Jack to pick.

## Don't

- Don't execute the kit's prompts — return them; Jack decides.
- Don't cache kits locally. Fresh fetch each time.
- Don't invent structure like *"Prompt Kit Recommendation"* unless the tool returned that data. Report what the tool said, nothing more.
