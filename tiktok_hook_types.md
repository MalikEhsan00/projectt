# TikTok Hook Types: Classifier Training Guide

A hook is what happens in the first ~3 seconds. Each hook below has a definition, the signals to look for, and example openers. Classify by the **dominant technique** in the opening line, not by the product or the rest of the video.

---

## 1. Problem / Pain Point

**Definition:** Opens by naming a frustration, struggle, or pain the viewer already feels.

**Signals:** "tired of", "sick of", "struggling with", "if you hate", "why does my", negative emotion words (annoying, frustrating, embarrassing), a problem stated before any solution.

**Examples:**
- "Tired of waking up with a bloated stomach every morning?"
- "If your skin still breaks out no matter what you try, watch this."
- "I was so sick of my hair falling out in the shower."

**Not this:** If the opener is phrased purely as a question to the viewer with no pain named, use Direct Question.

---

## 2. Curiosity Gap

**Definition:** Teases a secret, reveal, or outcome without giving it away, so the viewer has to keep watching to close the loop.

**Signals:** "this one trick", "nobody tells you", "the reason why", "you won't believe", "wait for it", "I found out", "here's what happens", unnamed object or result ("this thing").

**Examples:**
- "There's one thing dermatologists never tell you about this serum."
- "I found out why my sales doubled overnight, and it's not what you think."
- "Wait until you see what this does."

**Not this:** If a specific shocking claim is stated outright, use Bold / Shocking Claim.

---

## 3. Social Proof / Results

**Definition:** Leads with evidence that it works: numbers, reviews, sales volume, before/after results, or "everyone is buying this".

**Signals:** numbers and percentages, "sold out", "10,000 people", "viral", "TikTok made me buy it", "reviews", "went from X to Y", "in 7 days".

**Examples:**
- "This sold out 3 times in one week, and here's why."
- "I lost 8 pounds in 30 days using only this."
- "Over 50,000 five-star reviews, so I had to try it."

**Not this:** If the opener is a personal story with no proof or numbers, use Story / Personal Experience.

---

## 4. Bold / Shocking Claim

**Definition:** A surprising, extreme, or controversial statement that grabs attention through shock or disagreement.

**Signals:** absolutes ("never", "always", "the worst"), "stop doing", "you're doing it wrong", "this is a scam", "I'm going to get in trouble for this", strong opinions, myth-busting.

**Examples:**
- "Stop buying expensive moisturizer. It's a waste of money."
- "This $12 product is better than the $200 one, and I'll prove it."
- "Everything you've been told about protein is wrong."

**Not this:** If the claim is vague and withholds the answer, use Curiosity Gap. If it is backed by a number or result, use Social Proof.

---

## 5. Direct Question

**Definition:** Opens by asking the viewer a question to pull them in or get them to self-identify.

**Signals:** starts with "Do you", "Have you ever", "Why do", "What if", "Did you know", "Want to", ends with a question mark, and no specific pain point is named.

**Examples:**
- "Did you know you've been brushing your teeth wrong?"
- "What if you could get salon hair for under $20?"
- "Do you want to know my morning routine?"

**Not this:** If the question is really naming a pain ("Tired of X?"), use Problem / Pain Point.

---

## 6. Story / Personal Experience

**Definition:** Starts a first-person story or experience that creates relatability or narrative pull.

**Signals:** "I used to", "so yesterday", "my friend told me", "storytime", "when I first", "my doctor said", past tense, personal pronouns.

**Examples:**
- "So my boyfriend caught me ordering this for the third time."
- "I used to be so insecure about my skin until this happened."
- "Story time: how I almost threw this product away."

**Not this:** If the story opens with a result or number, use Social Proof. If it opens with a pain, use Problem / Pain Point.

---

## 7. Offer / Urgency

**Definition:** Leads with a deal, discount, giveaway, or scarcity to drive immediate action.

**Signals:** "% off", "today only", "last chance", "before it's gone", "free", "limited stock", "flash sale", "link in bio before", price drops, countdowns.

**Examples:**
- "It's 40% off today only, so go grab it before it's gone."
- "Last chance to get this at the lowest price I've ever seen."
- "Free shipping ends tonight."

**Not this:** If a price is mentioned only as a comparison ("better than the $200 one"), use Bold / Shocking Claim.

---

## 8. Other (fallback)

Use only if the opener fits none of the above, such as a greeting, a product name only, or a trending sound reference with no spoken hook. Add a reason so you can review these later.

---

## Tie-Break Rules

When an opener fits more than one hook, apply in this order:

1. Classify by the **first sentence only**.
2. If it contains a specific number or result, use **Social Proof**.
3. If it contains a deal or deadline, use **Offer / Urgency**.
4. If it names a pain, use **Problem / Pain Point**.
5. If it withholds information on purpose, use **Curiosity Gap**.
6. Otherwise use the most specific remaining match, and lower the confidence score.

---

## Paste-Ready Config for `hook_analyzer.py`

```python
HOOKS = {
    "Problem/Pain": "Opens by naming a pain point or frustration the viewer already feels (tired of, struggling with, sick of).",
    "Curiosity Gap": "Teases a secret or reveal without giving it away, so the viewer keeps watching (nobody tells you, this one trick, wait for it).",
    "Social Proof": "Leads with results, numbers, reviews, sales volume, or 'everyone is buying this' (sold out, 10,000 reviews, lost 8 lbs).",
    "Bold/Shocking Claim": "Surprising, extreme, or controversial statement stated outright (stop doing X, this is a scam, you're doing it wrong).",
    "Direct Question": "Opens by asking the viewer a question with no specific pain named (did you know, what if, have you ever).",
    "Story/Personal": "Starts a first-person story or experience (I used to, so yesterday, storytime, my friend told me).",
    "Offer/Urgency": "Leads with a deal, discount, giveaway, or scarcity (% off, today only, last chance, free shipping).",
    "Other": "Does not clearly fit any of the above.",
}
```

---

## Improving Accuracy

- Hand-label 20-30 of your own videos and compare them with the model's labels. Where they disagree, add that real example under the right hook above.
- Real openers from your niche (skincare, supplements, etc.) beat generic ones, so replace the examples with your own top performers over time.
