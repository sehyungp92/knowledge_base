---
name: challenge
description: Challenge a landscape entity or self-challenge a tracked belief
---

# /challenge Skill

You are executing the /challenge skill. This supports two modes:
1. **Landscape challenge** — challenge the system's assessment of a landscape entity
2. **Belief self-challenge** — construct the strongest counter-case against one of your own beliefs

## Safety
- Always present both sides of the argument
- Record all challenge resolutions in the challenge_log
- Never silently modify beliefs — surface all changes for user confirmation
- Preserve the distinction between "user disagrees" and "evidence contradicts"

## Execution Contract

### Step 1: Parse Command

- `/challenge <entity_type> <entity_id>` — challenge a landscape entity
  - entity_type: capability, limitation, bottleneck, breakthrough, anticipation
- `/challenge belief <belief_id>` — self-challenge a tracked belief
- `/challenge belief <belief_id> steelman` — steelman mode: construct strongest counter-case

### Step 2: Execute Mode

#### Mode: Landscape Challenge (`/challenge <entity_type> <entity_id>`)

1. Load the entity from DB:
   - capabilities, limitations, bottlenecks, breakthroughs, anticipations
2. Present the system's current position:
   - Description, confidence, evidence sources, history of changes
3. Ask the user for their argument:
   - "What's your challenge to this assessment?"
4. Evaluate the challenge:
   a. Search library for evidence supporting and contradicting the user's position
   b. Check landscape_history for how the entity has evolved
   c. Check if related entities would be affected by the change
5. Present resolution options:
   - **system_updated**: System changes its assessment based on user's argument
   - **user_position_recorded**: System maintains position but records user's view
   - **ambiguous_flagged**: Evidence is genuinely mixed, flag for future review
   - **system_maintained**: User withdraws challenge after seeing evidence
6. Execute resolution:
   - Log to challenge_log via `reading_app.db.insert_challenge_log()`
   - If system_updated: modify the entity + log to landscape_history
   - If entity is linked to beliefs: flag linked beliefs for review

#### Mode: Belief Self-Challenge (`/challenge belief <belief_id>`)

1. Load belief via `reading_app.db.get_belief()`
2. Load evidence_for and evidence_against
3. Load landscape context for the belief's theme
4. Present the belief with all evidence:
   - Claim, confidence, evidence for/against, landscape links
5. Construct the counter-case:
   a. Search library for contradicting evidence
   b. Identify logical weaknesses in the belief's foundations
   c. Check if any evidence_for has been weakened by newer sources
   d. Look for implicit assumptions that may not hold
6. Present counter-case to user
7. Ask for resolution:
   - **confidence_adjusted**: User updates confidence
   - **belief_refined**: User reformulates the belief
   - **belief_decomposed**: User splits into sub-beliefs (uses parent_belief_id)
   - **challenge_dismissed**: User maintains original position
   - **belief_archived**: User abandons the belief
8. Execute resolution:
   - Log to challenge_log with entity_type='belief'
   - Update belief via appropriate DB call
   - If confidence changed: append to history via `update_belief_confidence()`

#### Mode: Steelman (`/challenge belief <belief_id> steelman`)

Same as self-challenge, but with steelman framing:
1. Instead of looking for weaknesses, construct the STRONGEST possible counter-argument
2. Include:
   - Best evidence against the belief from the library
   - Most compelling theoretical argument against it
   - What would need to be true for the belief to be wrong
   - Who in the field would disagree and their strongest argument
3. Present as a devil's advocate case, not a verdict
4. Same resolution options as self-challenge

### Step 3: Return Response

```
{For landscape challenge:}
**Challenge: {entity_type} — "{description}"**

**System position:** {current assessment with evidence}

**Your argument:** {user's challenge}

**Evidence review:**
Supporting your challenge: {evidence found}
Against your challenge: {counter-evidence}

**Resolution:** {outcome}
{If system_updated: "Assessment updated: {description of change}"}
{If linked beliefs affected: "Note: This change may affect your belief: '{belief_claim}'"}

{For belief self-challenge:}
**Self-Challenge: "{belief_claim}"**
Current confidence: {confidence}

**Counter-case:**
{structured argument against the belief}

**Strongest counter-evidence:**
{from library}

**Weakest foundations:**
{logical weaknesses identified}

**Resolution:** {outcome}
{If confidence_adjusted: "Confidence: {old} → {new} (trigger: self-challenge)"}
{If belief_refined: "Belief updated: '{new_claim}'"}

{For steelman:}
**Steelman Counter-Case: "{belief_claim}"**

{strongest possible argument against}

**Devil's advocate verdict:** {assessment of counter-case strength}

**Your response?**
- Update confidence
- Refine belief
- Dismiss challenge
- Archive belief
```
