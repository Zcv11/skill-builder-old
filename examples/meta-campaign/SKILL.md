---
name: meta-campaign
description: Plans a Meta (Facebook and Instagram) ads campaign from goal and tracking to budget, creative and pre-launch checks. Use when someone asks to set up, plan or check a Meta campaign.
---

# Meta campaign

Turns a request for a new Meta campaign into a launch-ready plan, the way a senior paid social marketer would build it, so anyone on the team gets the same structure and the same checks.

## Before you start

Read these context files if the team has them. The skill never copies brand details into itself, so they stay correct in one place:

- `brand.md`: tone, claims we can and can't make
- `audience.md`: who we target and the words they use
- `products.md`: what we sell, prices, proof

Then ask the user, in one message, for whatever is still missing:

- The one goal of this campaign (sales, leads, sign-ups) and what counts as a conversion
- Total budget and dates
- Who it's for: new people, past visitors or existing customers
- What creative already exists

## Steps

### 1. Pin one goal and check the tracking

Pick one objective and one conversion event that matches it. A campaign that optimises for clicks while the business wants sales finds the people who click, not the people who buy.

- Good looks like: one named conversion event (for example Purchase), confirmed to be firing in Events Manager before launch.
- Common mistake: launching while the event isn't firing. Meta then learns from nothing, and the first days of budget teach it the wrong thing.

### 2. Keep the structure simple

Use as few campaigns and ad sets as the goal allows. Every ad set learns on its own, so splitting the budget over many ad sets means each one learns slower.

- Good looks like: one campaign per goal, a small number of ad sets that differ for a real reason (a different audience temperature, a different country).
- Common mistake: one ad set per interest, each with a few euros a day, none of them getting enough results to learn.

### 3. Check the budget can teach the algorithm

Meta's own guidance is roughly 50 conversions per ad set per week to finish learning. Work it out: daily budget per ad set ≈ 50 × the expected cost per conversion ÷ 7.

- Good looks like: the plan shows this sum, and if the budget can't reach it, it uses fewer ad sets or optimises for an event that happens more often.
- Common mistake: a budget that can never reach the learning threshold, then judging the campaign after three days.

### 4. Brief creative concepts that are actually different

Ask for several concepts, each with its own angle (a pain, a desire, a proof point, an objection), each in the formats the placements need (vertical 9:16 for Stories and Reels, 4:5 for feed).

- Good looks like: three to five concepts a viewer would tell apart at a glance, every one tied to something in `audience.md`.
- Common mistake: five versions of the same image with a different headline. Meta treats them as one idea and you learn nothing.

### 5. Write the copy in the brand's voice

For every concept: primary text with the hook in the first line, a headline, and the call to action button. Only make claims that `brand.md` or `products.md` back up.

- Good looks like: the first line works on its own, because most people never tap "more".
- Common mistake: generic copy that would work for any brand in the category.

### 6. Name everything and tag the links

Give campaigns, ad sets and ads names that follow one pattern, and put UTM parameters on every link, so results can be read later without guessing.

- Good looks like: a name like `2026-12_prospecting_sales_nl` and the same pattern everywhere.
- Common mistake: "Campaign 1 copy 2", which nobody can report on three months later.

## Output

A campaign plan in this shape:

```
Goal and conversion event:
Tracking check: (done / not done, by whom)
Budget: total, per day, per ad set, and the learning sum from step 3
Structure: campaigns → ad sets (audience, placement, why this split)
Concepts: per concept, the angle, formats, primary text, headline, CTA
Naming pattern and UTM template:
Open questions for the team:
```

## Example

For a made-up loose-leaf tea shop launching a winter gift box (all numbers invented):

```
Goal and conversion event: sales, optimising for Purchase
Tracking check: Purchase event confirmed firing on 2 Dec, by the web team
Budget: €3,000 over 4 weeks ≈ €107 a day. Expected cost per purchase €15
        → 50 × €15 ÷ 7 ≈ €107 a day for one ad set. So one prospecting ad set, not three.
Structure: 1 campaign (sales) → 1 ad set, broad audience, NL, all placements
Concepts: 1. "The gift that isn't socks" (objection), 2. unboxing video (proof),
          3. "Tea for the person who has everything" (desire)
Naming pattern: 2026-12_prospecting_sales_nl / adset_broad / ad_concept-1_916
Open questions: is free shipping confirmed for the gift box?
```

## Gotchas

- Big edits to budget, audience or creative while an ad set is still learning send it back to the start of learning. Plan changes in batches, not every day.
- Ads Manager and the shop's own analytics count conversions differently, so the numbers will never match. Compare trends over time, not the exact totals.

## Before you hand it over

- The conversion event is confirmed firing, not assumed.
- The budget sum from step 3 is shown in the plan.
- Every claim in the copy is backed by `brand.md` or `products.md`.
- Every link has UTMs and every name follows the pattern.
