---
name: unslop
description: Cut AI tells from any writing. Applies to every prose surface: replies, docs, handoffs, convergence packets, SKILL.md bodies, PR descriptions, commit messages, and CIL records.
---

# Unslop

Edit text to remove AI patterns and add human voice.

Source: `cursor/plugins` `pstack/skills/unslop/SKILL.md` @ `60c641e4fad674784b30abcf9f8915dea39df38d`, MIT (Lauren Tan), scouted 2026-08-19. Tweaked for this system: rule 26 is scoped to the glossary lock, and a Diátaxis / Global English section is folded in from the same repo's `technical-writing` skill.

## Process

1. Scan for the patterns below.
2. Rewrite. Preserve meaning, match intended tone.
3. Add soul (see next section).
4. Self-audit: "What makes this obviously AI generated?" Fix remaining tells.

## Adding soul

Removing patterns is half the job. Sterile, voiceless writing is just as obvious.

- **Have opinions.** React to facts instead of neutrally listing pros and cons.
- **Vary rhythm.** Short sentences. Then longer ones that take their time. Mix it up.
- **Acknowledge complexity.** "Impressive but also kind of unsettling" beats "impressive."
- **Use "I" when it fits.** First person isn't unprofessional.
- **Let some mess in.** Perfect structure looks machine-made.
- **Be specific.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am."

## Patterns to detect and fix

### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Listing sources without context. Pick one, say what was said.
3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
4. **Promotional language.** "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has".
9. **"Not just X, but Y."** State the point directly instead.
10. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash substitutes). If a thought needs separation, end the sentence or use a comma.
14. **Colon overuse.** Colons are fine before a list or example. Not as mid-sentence connectors.
15. **Boldface overuse.** Don't bold every proper noun or acronym.
16. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove from headings and bullets.
19. **Curly quotes.** Replace with straight quotes.

### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
21. **Cutoff disclaimers.** "While specific details are limited..." Find sources or remove.
22. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.

### Filler

23. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
25. **Generic conclusions.** "The future looks bright." State specific plans or facts.

### Jargon

26. **Abstract metaphor nouns.** Wedge, vector, locus, vantage, nexus, harness (as metaphor), bedrock, modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. These read as technical but usually have a plainer concrete word. "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Gold-plating" becomes "more than the job needs". "Evacuate" becomes "move out". "Endgame" becomes "the last phase". Pick the concrete word.

    **SCOPE EXCEPTION, this system only.** This rule does NOT apply to terms held by
    `docs/handoffs/CANONICAL-TERMINOLOGY-GLOSSARY-LOCK-v1.md`, `operator-web/CONTEXT.md`,
    or CIL `doctrine/DOC-003-surface-clarity.md`. **`substrate`, `surface`, `primitive`,
    and `scaffolding` are canonical domain terms here, not metaphors.** Census
    2026-08-19: `surface` 7,375 uses, `substrate` 1,691 in `docs/` + `skills/`.
    Substrate-8 is the product name and Surface Clarity is locked doctrine. Renaming
    them is a canon change, not a style edit. Before adding any word to this rule,
    check the glossary lock first. If a canonical term is genuinely being used as a
    metaphor in a specific sentence, fix that sentence; do not touch the term.

### Plain speech

27. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: **if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.**
28. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.
29. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries". Passive is fine only when the actor is unknown or genuinely doesn't matter.
30. **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta.
31. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".

## Structure and disambiguation

Folded in from `technical-writing` @ the same pin. The STE layer of that skill is
omitted deliberately, because ASD-STE100 for operator-facing replies is already carried
elsewhere: by `~/.claude/output-styles/ELI5.md` on surfaces that can read it, and by the
operator preference block on surfaces that cannot. Cowork cannot read `~/.claude` at all, so
there the preference block is the only carrier. On a surface with neither, apply ASD-STE100
from here. These are the parts that setting does not cover, and
they apply to artifacts, not just chat.

**One document, one mode.** Two questions pick it: does the content inform action or
understanding, and does it serve learning or work?

- Action + learning: **tutorial**. Action + work: **how-to**.
- Understanding + work: **reference**. Understanding + learning: **explanation**.

Don't mix modes. No reference tables inside a tutorial, no arguing inside a how-to.
Split and link instead. Opinion is allowed in explanation and nowhere else. This is
the rule governed artifacts break most: a convergence packet that is part reference,
part argument, part instruction is three documents wearing one filename.

**Leave no sentence open to two readings.**

- Keep "only" and "not" next to the word they change. "only fails on growth" and "fails only on growth" say different things.
- Break up long noun strings. "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Make every "it", "they", and "this" point at one obvious thing. Never use "this" or "which" to point at a whole clause.
- Don't drop verbs across a parallel construction.
- Keep the small words that show structure. "Ensure that the switch is off" keeps "that".
- Say which parts "and" or "or" joins when a sentence can group two ways.
- Use periods, not semicolons.
- Make parenthetical text a full grammatical unit or its own sentence. Never form plurals with "(s)".
- No slashes. Write "a, b, or both".
- **Call each thing by one name, everywhere.** A doc that says "the gate", "the ratchet", and "the budget check" for one thing teaches three things.
- Skip idioms, Latin abbreviations, and metaphors.

**Review checklist.** Item 1 applies to document sets only.

1. Is each file one mode, with links where modes meet?
2. Is every instruction a command, with its condition in front?
3. Does any sentence carry two instructions or two thoughts? Split it.
4. Can any word be cut without losing meaning? Cut it.
5. Is "only" next to the word it changes? Does every "it" point at one thing?
6. Does each thing have exactly one name across the docs?
7. Would a developer say these words out loud?
8. Are all symbols, paths, and counts real at this commit, with the commands that regenerate the counts?

## When a rule makes it worse

The rules serve the reader. A sentence that follows every rule and sounds like a
machine wrote it has failed. Fix it another way or leave it alone.
