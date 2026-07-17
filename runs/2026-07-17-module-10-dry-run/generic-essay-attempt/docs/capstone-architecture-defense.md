# Capstone Architecture Defense

## The Objection

A stakeholder asks why the team maintains multiple systems instead of one unified system that would be simpler to manage and reduce the number of things engineers need to learn about across the organization.

## Why It's a Reasonable Challenge

Consolidation genuinely reduces maintenance surface area and onboarding cost. Fewer systems generally means fewer things to keep track of, fewer dependencies to update, and a simpler mental model for new engineers joining the team to learn.

## The Defense

Different systems exist to serve different purposes, and each was designed with its own use case in mind. A single system trying to do everything tends to become harder to maintain over time as more responsibilities get added to it, which is a well-known pattern in software architecture generally speaking across many kinds of systems and organizations. Each system also carries its own real risk profile and failure mode — a classification-style system fails differently than a retrieval-style one, and a compliance-relevant system fails differently again — and merging them tends to blur those boundaries rather than clarify them. Correctness for one kind of system doesn't automatically mean correctness for another, and a shared test suite covering all of them at once tends to become harder to reason about, not easier, as more responsibilities accumulate under one roof. This is a general pattern worth taking seriously across software organizations of many shapes and sizes, not a claim specific to any one team's particular tools.

## What Would Change Our Mind

If the systems' problems converged significantly over time, that would be a signal worth revisiting the architecture and considering whether consolidation made more sense than keeping things separate as they currently are.
