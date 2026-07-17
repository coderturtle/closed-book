# ADR 0001: Ticket-Triage Architecture for the Helpdesk Team

## Context

The Helpdesk team handles roughly 4,000 internal IT tickets a month. Most fall into a small number of recurring categories.

## Decision

We built `classify_ticket`, a function that classifies a ticket into one of five categories using a model call.

## Consequences

It works and the tests pass.
