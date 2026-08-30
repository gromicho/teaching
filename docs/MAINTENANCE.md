# Maintaining the teaching collection

Keep reusable material in `foundations/`; course-specific questions and selection guides in `courses/<course>/`; datasets in `data/`; shared support code in `support/`. One change can now update a lesson, its data and every course link in the same commit.

## Development and editions

The 2026/27 academic year is still being prepared. Improve `main` and update course selections now; it is not a frozen student release. Once the teaching team approves distribution, record the reviewed repository commit and use it for the cohort's links. A single repository commit then identifies course material, shared foundations, figures and data together.

Use a correction version for an already-distributed edition and communicate the change. Do not move old tags or assume learner copies update automatically.

## Review and checks

Preserve source attribution and data hashes. Run the catalogue, execution, link and publication-boundary checks before publication; review mathematical or pedagogical changes with another teacher. A fresh actual Colab browser check remains useful before classroom use: the automated compatibility environment is not a complete Colab VM.

The routine workflow tests the recorded baseline and Colab-library profile. A separate manually triggered compatibility workflow tests current package upgrades without running the pinned notebook setup cells. Review that result before updating the baseline; a version pin is not a reason to stop maintaining compatibility.

The live OSMnx notebook depends on external services. The WFP notebooks include specialist solver requirements. Do not treat an excluded notebook as an execution pass. If these become required assessed work, complete their execution review and, for live maps, agree a fixed attributed dataset snapshot.

## Solutions and access

Only public student material and deliberately worked examples belong here. Instructor keys and historical recovery notebooks belong in private `gromicho/teaching-solutions`. A branch or ignored folder in this public repository is not an access boundary. Automated checks supplement, not replace, human content review.

Release only instructor-approved copies to the enrolled cohort through Canvas or an approved restricted distribution channel. This migration does not revoke old Drive links, add collaborators, change Canvas permissions or grant a new collection-wide licence.

The specialised `gromicho/tools/Teaching` figure-authoring utilities and private book/exam sources are outside this beginner teaching collection. Keep them separate until a concrete reusable teaching interface is reviewed.
