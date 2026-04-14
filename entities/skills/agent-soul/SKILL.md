---
name: agent-soul
category: skills
description: "Canonical SOUL.md templates and analysis — personality, boundaries, security guidance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Soul, Security, Skill]
---

# SOUL Skill Canonical

This SKILL.md archives extracted guidance and templates for SOUL.md usage. It matches the `entities/skills/` format required by the wiki schema and can be used as a canonical reference for creating or reviewing SOUL.md files.

## Trigger Conditions
- When a raw article about SOUL.md is ingested
- When a user asks to create or audit a SOUL.md for an agent

## Templates
- Efficiency assistant
- Learning partner
- Data analyst

## Pitfalls
- Prompt-injection and persistence backdoors
- Allowing autonomous edits without approval

## Verification
- Confirm frontmatter present and `sources` reference the raw articles (moved to _archive/raw/)
- Run file integrity monitoring recommendations
