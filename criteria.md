# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

This target is set to 4 of 5 rather than 5 of 5 because user input parsing relies on text processing (extracting terms like style keywords or size constraints). Occasionally, variations in phrasing or edge-case keyword extraction might prevent a listing match or cause downstream formatting issues in the multi-step pipeline. Allowing 1 out of 5 runs to fail accounts for subtle phrasing edge cases while ensuring the happy path remains overwhelmingly reliable.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

Unlike the multi-step generation path, the early-stop branch rule (`if not listings: return session`) is controlled by deterministic Python code in `agent.py`. If `search_listings` returns an empty list, the control flow must immediately halt execution without invoking unnecessary LLM API calls. Because this is pure programmatic conditional branching, there is no model variance involved, making 100% (5 of 5) the required standard for correctness.

---

## 3. The item passed to suggest_outfit matches the top search result

When a query matches listings, the exact `id` of the top item returned by `search_listings` matches the `new_item["id"]` passed into `suggest_outfit` — 5 of 5 tries.

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

This tests that session state transfers accurately between pipeline steps without being dropped, overwritten, or misindexed. Because state passing is fully deterministic Python code in `agent.py`, any failure is a code bug rather than model variance, making 5 of 5 a necessary and achievable baseline.


**Why this target:**



---

## 4. The fit card caption mentions the price of the item

When given a valid outfit and item dict, the generated fit card caption contains the price of the item (formatted as a dollar amount, e.g., "$25") — in at least 4 of 5 tries.

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

`create_fit_card` uses an LLM, which introduces non-deterministic text generation. While prompt engineering instructs the model to include the price, LLM outputs occasionally miss structured details, so 4 of 5 allows for slight model variance while ensuring the required pricing information is consistently present.


**Why this target:**



---

## 5. search_listings strictly enforces the max_price filter

When a query includes a price ceiling (e.g., "under $30"), every listing dict returned by `search_listings` has a `price` less than or equal to `max_price` — 5 of 5 tries.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->



**Why this target:**
Filtering logic in `search_listings` is programmatic Python filtering (`item['price'] <= max_price`). Since search filtering relies on standard numeric comparison rather than LLM generation, it must never return an item above the user's budget, making 5 of 5 the expected standard for correctness.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
