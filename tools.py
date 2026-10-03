"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
import re


# ── Tool 1: search_listings ───────────────────────────────────────────────────
_STOPWORDS = {
    "a", "an", "and", "the", "for", "or", "but", "if", "then", 
    "else" "with", "in", "of"
}

def _keywords(text: str) -> set[str]:
    """
    Return a set of lowercase keywords worth matching on from a string, 
    with stopwords removed.

    Args:
        text: any string

    Returns:
        a set of lowercase words, with punctuation stripped and stopwords
        removed. If the input is empty or whitespace, returns an empty set.
    """
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}

def _size_tokens(size: str) -> set[str]:
    """
    Return a set of lowercase tokens from a size string, with punctuation
    stripped.

    Args:
        size: any string

    Returns:
        a set of lowercase words. If the input is empty or whitespace, returns
        an empty set.
    """
    cleaned = re.sub(r"\([^)]*\)", " ", size or "")
    parts = [p.strip().upper for p in cleaned.split("/")]
    return {p for p in parts if p}

def _size_matches(wanted: str, listing_size: str) -> bool:
    """
    Return True if the listing size matches the query size, False otherwise.    
    """
    if not wanted:
        return True
    listing_tokens = _size_tokens(listing_size)
    if any(token.startswith("ONE SIZE") for token in listing_tokens):
        return True
    return bool(_size_tokens(wanted) & listing_tokens)

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()
    query_keywords = _keywords(description)
    
    matching_listings = []

    for item in listings:
        # 1. Filter by max_price (inclusive)
        if max_price is not None and item.get("price", 0.0) > max_price:
            continue

        # 2. Filter by size
        if size and not _size_matches(size, item.get("size", "")):
            continue

        # 3. Calculate keyword match score across title, description, and style_tags
        item_text = f"{item.get('title', '')} {item.get('description', '')} {' '.join(item.get('style_tags', []))}"
        item_keywords = _keywords(item_text)

        overlap = query_keywords & item_keywords
        score = len(overlap)

        # 4. Drop anything scoring zero
        if query_keywords and score == 0:
            continue

        matching_listings.append((score, item))

    # 5. Sort by score descending and return top matches up to config.SEARCH_RESULT_LIMIT
    matching_listings.sort(key=lambda x: x[0], reverse=True)

    results = [item for score, item in matching_listings]
    return results[:config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = wardrobe.get("items", []) if wardrobe else []

    title = new_item.get("title", "thrifted item")
    desc = new_item.get("description", "")
    category = new_item.get("category", "")
    tags = ", ".join(new_item.get("style_tags", []))

    if not items:
        prompt = (
            f"Provide 2 short, versatile styling ideas and general advice for "
            f"incorporating this thrifted item into an everyday wardrobe:\n\n"
            f"Item: {title}\n"
            f"Category: {category}\n"
            f"Description: {desc}\n"
            f"Style Tags: {tags}\n\n"
            f"Keep the suggestions concise and practical."
        )
        outfit_text = generate(prompt)
        return outfit_text or "Pair this thrifted find with simple daily basics."

    wardrobe_summary = []
    for idx, w_item in enumerate(items, 1):
        w_title = w_item.get("title", w_item.get("name", "Item"))
        w_cat = w_item.get("category", "")
        w_tags = ", ".join(w_item.get("style_tags", []))
        wardrobe_summary.append(f"{idx}. {w_title} ({w_cat}) - Tags: {w_tags}")

    wardrobe_str = "\n".join(wardrobe_summary)

    prompt = (
        f"You are a personal stylist. Suggest 1 or 2 distinct outfits that pair the "
        f"following new thrift find with specific items from the user's current wardrobe.\n\n"
        f"NEW ITEM:\n"
        f"Title: {title}\n"
        f"Category: {category}\n"
        f"Description: {desc}\n"
        f"Style Tags: {tags}\n\n"
        f"USER'S WARDROBE:\n"
        f"{wardrobe_str}\n\n"
        f"Instructions: Name specific wardrobe items from the list above in your suggestions "
        f"and explain briefly why the pieces work well together."
    )

    outfit_text = generate(prompt)
    return outfit_text or "Pair this find with items in your wardrobe that share a similar style aesthetic."


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # 1. Guard against empty or whitespace-only outfit
    if not outfit or not outfit.strip():
        return "Could not generate fit card: no outfit suggestions provided."

    title = new_item.get("title", "thrift find")
    price = new_item.get("price", "bargain price")
    platform = new_item.get("platform", "thrift app")
    brand = new_item.get("brand") or "unbranded"

    # 2. Build prompt for social post caption
    prompt = (
        f"Write a short, engaging social media caption (2 to 4 sentences) about a thrift find.\n\n"
        f"Item: {title}\n"
        f"Price: ${price}\n"
        f"Platform: {platform}\n"
        f"Brand: {brand}\n"
        f"Outfit Details: {outfit}\n\n"
        f"Requirements:\n"
        f"- Keep it strictly between 2 and 4 sentences.\n"
        f"- Must sound like a real person posting on Instagram/Depop/TikTok.\n"
        f"- Mention the item name, price (${price}), and platform ({platform}) exactly once.\n"
        f"- Do NOT use hashtags."
    )

    # 3. Call generate and return response
    card_text = generate(prompt)
    return card_text or f"Scored this {title} for ${price} on {platform}! Perfect addition to the wardrobe."
