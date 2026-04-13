---
name: file
description: File a recent chat answer or topic as a wiki page
---

# /file Skill

## Purpose
Create a wiki page from a topic, concept, or recent conversation context.

## Execution Contract

1. Parse the user input after `/file` to determine:
   - **Page type**: theme, entity, synthesis, or question
   - **Topic/title**: the subject matter
   - If ambiguous, default to synthesis type

2. Determine relevant theme_ids by querying the themes table:
   ```python
   from reading_app.db import ensure_pool, get_conn
   ensure_pool()
   with get_conn() as conn:
       themes = conn.execute("SELECT id, name FROM themes").fetchall()
   ```
   Match the topic against theme names/ids.

3. Route by page type and write:

   **synthesis** (default):
   ```python
   from retrieval.wiki_writer import create_synthesis_page, slugify
   slug = slugify(topic)
   create_synthesis_page(slug, content, theme_ids, executor=None)
   # → wiki/syntheses/{slug}.md
   ```

   **question** (when filing a Q&A pair):
   ```python
   from retrieval.wiki_writer import create_question_page
   create_question_page(question_text, answer_text, theme_ids)
   # → wiki/questions/{slug}.md
   ```

   **entity** (regenerate an entity page — triggers LLM call):
   ```python
   from retrieval.wiki_writer import create_entity_page
   # Requires concept_data dict from DB (id, name, description, type, claims)
   create_entity_page(concept_id, concept_data, executor, model="sonnet")
   # → wiki/entities/{slug}.md
   ```

   **theme** (regenerate a theme page — triggers LLM call):
   ```python
   from retrieval.wiki_writer import create_theme_page
   # Requires theme_data dict from DB (name, state_summary, capabilities, etc.)
   create_theme_page(theme_id, theme_data, executor, model="sonnet")
   # → wiki/themes/{theme_id}.md
   ```

4. Confirm to the user: "Filed as wiki page: `wiki/{type}/{slug}.md`"

## Safety
- Only write to wiki/ directory
- Never modify existing pages without explicit instruction
- Always add proper frontmatter
