# ADR 0001: Ticket-Triage Architecture for the Helpdesk Team

## Context

The Helpdesk team handles roughly 4,000 internal IT tickets a month. The large majority fall into a small number of recurring categories (password reset, VPN/network access, software requests, hardware requests), stated up front by the employee in a single message. The team's first request was "we want something like `resolve`" — Part 1's multi-tool agentic coordinator, capable of looking up account status, resetting credentials, and escalating autonomously across multiple turns.

## Decision

We are building a single-turn classification workflow (`classify_ticket`), not an agentic loop. Each ticket is classified in one model call (plus schema-validated retries on malformed output) against a fixed set of five categories, with the result routed to the correct downstream queue by existing (non-Claude) Helpdesk tooling. The system prompt carrying the IT policy and category definitions is static and reused verbatim across every ticket, structured so it can be cached rather than resent in full for each of the ~4,000 monthly tickets.

## Alternatives Considered

**A full agentic loop, matching `resolve`'s own architecture (the team's original request).** Rejected. `resolve` is a multi-tool coordinator because its job genuinely requires multi-step tool use across turns — verifying a customer, looking up an order, and conditionally issuing a refund are causally dependent steps that can fail or need escalation partway through. Ticket triage has no such structure: the input is a single message, the output is one of five labels, and there is no multi-step tool sequence to orchestrate. An agentic loop here would add a `stop_reason` handling layer, tool-call latency, and a materially larger failure surface (tool selection errors, loop termination bugs, the class of defect Module 06's own capstone exists to teach diagnosing) for zero functional benefit over a single well-designed classification call. Cost also scales the wrong way: an agentic loop's per-ticket cost is at minimum one model call and typically several (tool-use turns), against classify_ticket's one call in the common case.

**A larger, more capable model tier for every ticket.** Rejected as the default. Ticket categorization from a single short message is a well-bounded, low-ambiguity task; the marginal accuracy of a larger model on this task does not justify its added latency and per-call cost at ~4,000 calls/month. The "other" category with a required, mandatory `detail` field is the deliberate escape hatch for the genuinely ambiguous minority — those get routed to a human triager with real context, rather than the whole pipeline paying a larger model's cost to marginally improve accuracy on the easy majority.

## Consequences

**What this buys us:** low, predictable per-ticket latency and cost; a static system prompt that's byte-identical across every call, making prompt caching straightforward rather than something bolted on later; a failure mode (`TriageFailed`) that's simple to reason about and alert on, unlike a multi-turn agentic loop's larger space of partial-failure states.

**What this gives up, stated honestly:** if the Helpdesk team's real need grows to include multi-step actions (e.g., actually resetting a password rather than just routing the ticket to a human who does), this architecture doesn't extend to that in place — it would need a genuinely different design at that point, not an incremental change to `classify_ticket`. That's a real, named trade-off, not a gap discovered later: we're building for the problem as stated today, not for a hypothetical future scope the team hasn't actually asked for.
