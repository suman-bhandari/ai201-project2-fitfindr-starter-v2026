# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr takes a natural-language search request for a thrifted clothing item, optionally specifying a desired size, maximum price, or style keywords. It searches a catalog of thrift listings to find the best match and checks the item against the user's existing wardrobe. Finally, it generates a personalized outfit recommendation pairing the new find with owned clothes, accompanied by a social-media-ready caption card.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
     Search the listings data for items matching a description, and optionally a size and a price ceiling.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
     description (str), size (str | None), max_price (float | None)
- **Returns:**
     (list[dict]) A list of matching listing dicts (containing fields like id, title, description, size, price, etc.), best match first.
- **When it has nothing:**
     Returns an empty list when nothing matches — an empty list, not None, and not an exception.

### `suggest_outfit`

- **What it does:**
     Given a thrifted item and the user's wardrobe, suggest one or two outfits.
- **Inputs:**
     new_item (dict), wardrobe (dict)
- **Returns:**
     (str) A non-empty string containing outfit suggestions and styling advice.
- **When it has nothing:**
     With an empty wardrobe, return general styling advice string rather than raising an exception or returning "".

### `create_fit_card`

- **What it does:**
     Write a short caption that reads like a real post someone would post about the outfit find.
- **Inputs:**
     outfit (str), new_item (dict)
- **Returns:**
     (str) A two-to-four sentence string caption describing the fit post.
- **When it has nothing:**
     If outfit is empty or whitespace, return a descriptive error message string rather than raising an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
     If `search_listings` returns an empty list, store an error message in `session["error"]` and stop execution. Otherwise, take the first listing (`results[0]`) and proceed to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
     regex / string splitting
**What moves through the session:** <!-- which fields, in what order -->
     query (str) -> listings (list[dict]) -> selected_item (dict) -> outfit_suggestion (str) -> fit_card (str)

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'looking for a vintage graphic tee under $30'
[1] parse_query
      in:  looking for a vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Hey! As your stylist, I am so excited about this Y2K butterfly baby tee. It’s a super versatile piece because …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Channel your inner 2000s pop star with this adorable Y2K Baby Tee featuring a gorgeous butterfly print! It’s g…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Hey! As your stylist, I am so excited about this Y2K butterfly baby tee. It’s a super versatile piece because we can lean into its nostalgic 2000s roots or give it a cool-girl grunge contrast. 

Here are 2 distinct outfits using pieces straight from your current wardrobe:

### Outfit 1: Streetwear Y2K Contrast
* **Top:** Y2K Butterfly Baby Tee (New Item)
* **Bottoms:** Baggy straight-leg jeans, dark wash (#1)
* **Shoes:** Chunky white sneakers (#7)
* **Accessories:** Black crossbody bag (#10)
* **Layering Option (Optional):** Black cropped zip hoodie (#5) left open.

**Why this works:** 
This outfit plays on the classic Y2K proportion-play of "tight top, baggy bottom." The fitted, cropped nature of the baby tee balances out the relaxed volume of the dark wash straight-leg jeans. Finishing it with chunky white sneakers keeps the streetwear vibe grounded and effortless, while the black crossbody bag ties the whole casual look together. 

### Outfit 2: Vintage Grunge Twist
* **Top:** Y2K Butterfly Baby Tee (New Item)
* **Bottoms:** Wide-leg khaki trousers (#2)
* **Outerwear:** Vintage black denim jacket (#6)
* **Shoes:** Black combat boots (#8)
* **Accessories:** Brown leather belt (#9)

**Why this works:** 
While butterflies and baby tees lean sweet and cottagecore, pairing them with your black combat boots and vintage black denim jacket completely transforms the vibeinto a 90s/2000s grunge-meets-minimalist aesthetic. Tucking the tee into the wide-leg khaki trousers (cinched with your brown leather belt) adds a nice touch of earth tones that grounds the black outerwear and boots. 

Which direction are you feeling more today?

  Fit card: Channel your inner 2000s pop star with this adorable Y2K Baby Tee featuring a gorgeous butterfly print! It’s giving major nostalgia and is super easy to style for both sweet street looks and edgy grunge fits. Grab this ultimate wardrobe staple right now on depop for just $18.0 before someone else snags it!

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, ...]

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Hello! As your personal stylist, I am so excited about this new thrift find. Vintage Levi's 501s are the ultimate wardrobe holy grail—they go with literally everything. 

Here are two distinct, effortlessly cool outfits using pieces straight from your current wardrobe:

### Outfit 1: The Off-Duty Streetwear Look
* **The Vibe:** Casual, cool, and perfectly balanced between fitted and oversized.
* **The Recipe:**
  * **Top:** **White ribbed tank top** (fitted)
  * **Outerwear:** **Oversized grey crewneck sweatshirt** (layered casually over the shoulders or worn as your main top)
  * **Shoes:** **Chunky white sneakers**
  * **Accessories:** **Black crossbody bag**
* **Why it works:** The secret to styling straight-leg vintage denim is playing with proportions. The fitted **white ribbed tank top** contrasts the relaxed, straight-leg cut of the Levi's. Throwing on the **oversized grey crewneck sweatshirt** adds that cozy, streetwear-approved ease, while the **chunky white sneakers** and **black crossbody bag** tie the whole casual, everyday uniform together.

### Outfit 2: The Edgy Double-Denim Look
* **The Vibe:** Grunge-leaning, classic Americana with a modern edge.
* **The Recipe:**
  * **Top:** **White ribbed tank top** as your base layer
  * **Outerwear:** **Vintage black denim jacket**
  * **Shoes:** **Black combat boots**
  * **Accessories:** **Brown leather belt** & **Black crossbody bag**
* **Why it works:** Mixing medium wash blue jeans with a **vintage black denim jacket** is a foolproof way to do double-denim without looking costume-y—the contrast in washes keeps it intentional. Tucking the **white ribbed tank top** in and defining your waist with the **brown leather belt** adds a polished touch to the rugged base. Finally, grounding the outfit with **black combat boots** leans into thatclassic grunge aesthetic, making the whole look feel sharp and tough.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless fit of broken-in denim, and these Vintage Levi's 501Jeans in a timeless medium wash are absolute perfection. I love styling them withcrisp white sneakers for that classic off-duty look. Grab this dreamy pair now over on my depop for just $38.0 before someone else snaps them up!

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* 
I asked AI to review and write justifications for my target criteria, including a rule that `search_listings` must return items under `max_price` 5 out of 5 times.

- *What came back:* 
The AI helped formalize the justification, emphasizing that unlike LLM-generated output, price filtering in `search_listings` relies on deterministic Python logic (`price <= max_price`), meaning model variance does not apply and 100% reliability (5 out of 5) is the expected standard.

- *What I changed:* 
I incorporated this distinction into `criteria.md` to clearly differentiate between deterministic code filters (which require 5/5 pass rates) and LLM prompt generation steps (which allow a 4/5 pass rate due to text parsing variations).

**Moment 2**

- *What I asked for:* 
I asked AI to evaluate if a starter stub definition of `search_listings` satisfied the tool specification requirements.

- *What came back:* 
The AI identified that the starter stub returned a hardcoded `[]` without performing keyword parsing, price filtering, or size matching, and provided the full scoring and filtering logic.

- *What I changed:* 
Instead of using basic string substring matching for sizes (which incorrectly matched `"s"` in `"us 9"` or `"l"` in `"xl"`), I ensured size evaluation used `_size_matches()` token checking so non-matching clothes and shoes were correctly excluded from search results.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. The item passed to suggest_outfit matches the top search result | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 4. The fit card caption mentions the price of the item | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 5. search_listings strictly enforces the max_price filter | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1: Matching query completes all three tools
Produced by: agent.py::run_agent via run_eval.py::run_once (Scenario: matching query completes, Try 1)   
Output: 
Channel your inner early 2000s pop star with this adorable Y2K baby tee featuring a gorgeous butterfly print. It's listed on depop right now for just $18.0 and looks amazing styled with baggy denim or tailored trousers. Grab this nostalgic gem before someone else beats you to it!
   
Criterion 2: Impossible query stops before the second tool
Produced by: agent.py::run_agent (_nothing_found_message) (Scenario: impossible query stops early, Try 1)   
Output:
Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
   
Criterion 3: Selected item matches top search result
Produced by: agent.py::run_agent (Scenario: selected item matches top search result, Try 1)   
Output:
selected_item: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
top search result: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
trace: [3] select_item -> [4] suggest_outfit in: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
   
   
Criterion 4: Fit card caption mentions item price
Produced by: tools.py::create_fit_card (Scenario: fit card mentions item price, Try 1)   
Output:
Scored these chunky white platform sneakers on Poshmark for just $48, and I am officially obsessed. They give off major Y2K energy whether I'm styling them with baggy denim or dressing down wide-leg trousers. Honestly, they’re about to be my go-to shoe for every single outfit this season.
   
Criterion 5: Search respects max_price budget ceiling
Produced by: tools.py::search_listings via MCP (Scenario: search respects max_price budget ceiling, Try 1)   
Output:
Query max_price ceiling: $50.0
Returned 7 items, all under ceiling:
- Denim Jacket — Light Wash, Cropped: $42.0 (selected)
All 7 returned listings satisfy listing['price'] <= 50.0.
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | In all 5 tries, the agent successfully executed `parse_query`, `search_listings (via MCP)`, `select_item`, `suggest_outfit`, and `create_fit_card`, returning a populated `fit_card` string without errors or early terminations. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | In all 5 tries, `search_listings (via MCP)` returned `[]` (0 matches). The deterministic early-stop branch `if not results:` fired immediately at step [3], terminating the session, returning the explanatory guidance string, and making 0 model calls. |
| 3 | The item passed to suggest_outfit matches the top search result | 5 of 5 | MET (5/5) | For every run, `session["selected_item"]["id"]` matched the first element of `session["search_results"]` (`90s Silk Slip Dress — Floral, Midi Length`, id: 2). The step trace confirmed that the exact selected dictionary was passed into `suggest_outfit`. |
| 4 | The fit card caption mentions the price of the item | 4 of 5 | MET (5/5) | The selected item's price was $48.0. In all 5 tries, the generated fit card explicitly included the dollar price ("$48" or "$48.0") in its social caption body. |
| 5 | search_listings strictly enforces the max_price filter | 5 of 5 | MET (5/5) | The query specified "under $50". Across all 5 runs, all 7 returned items from the catalog had `price <= 50.0`, with the selected top item priced at $42.0. No listing exceeded the ceiling. |

**Diagnoses**
- Misses: 0 misses across 25 total trials (5/5 across all 5 criteria).
- Were the targets set too low?
  Yes, particularly for Criterion 1 and Criterion 4, which were both set at 4 of 5.
  - Criterion 1 (Matching query completes):A 4 of 5 target was originally selected as a buffer for potential keyword mismatch or JSON parsing hiccups. However, because `parse_query` uses structured fallback parsing and the catalog has broad keyword overlap across tags and categories, standard queries reliably retrieve items on every attempt.
  - Criterion 4 (Fit card mentions item price):A 4 of 5 target was chosen to account for non-deterministic model behavior. But the prompt template in `tools.py` strongly emphasizes including price and platform in the copy, which reliably steered Gemini to output the price across all 5 runs (even with temperature at 0.9 and caching off).

- Criterion to tighten:
  Criterion 4 (Fit card caption).
  Currently, it only checks that the price string appears in the card. To make this an informative evaluative test of output quality rather than just a keyword spot-check, it should be tightened to evaluate distinct creative angles or strict length constraints:
  
  Tightened Criterion 4: Across 5 independent runs for the same item, the generated fit cards share no opening sentence, mention the price ($48), and remain under 280 characters — 5 of 5 tries.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**
python app.py ask 'looking for a vintage graphic tee under $30' --trace
```
[1] parse_query
      in:  looking for a vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Hey! As your stylist, I am so excited about this Y2K butterfly baby tee. It’s a super versatile piece because …
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Channel your inner 2000s pop star with this adorable Y2K Baby Tee featuring a gorgeous butterfly print! It’s g…
```

**Empty search**
python app.py ask 'designer ballgown size XXS under $5' --trace

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
Refined the prompt in tools.py::create_fit_card to enforce a strict length limit (under 280 characters and 2 to 3 sentences), slice the incoming outfit string (outfit[:250]) to reduce token load, and mandate an engaging first-sentence hook alongside explicit ${price} and {platform} requirements.

**Which failure it was meant to fix:**
Targeted Criterion 4. In earlier evaluation, the generated fit cards were verbose (often exceeding 400 characters) and used repetitive opening clichés. The change was designed to make the fit cards concise, social-media-ready captions while ensuring the price formatting remained strictly present.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | FAIL | PASS | PASS | PASS | FAIL | MISSED (3/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 3. The item passed to suggest_outfit matches the top search result | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |
| 4. The fit card caption mentions the price of the item | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 5. search_listings strictly enforces the max_price filter | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET(5/5) |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
