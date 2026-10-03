# Stakeholder Validation Module

## Objective
To gather empirical usability feedback from actual target users (warehouse dispatchers and operations managers) as requested in the Phase 1 Qbee review.

## Validation Protocol
This document outlines the formal test scenarios to be performed by stakeholders. Due to current prototype constraints, **actual human validation is PENDING**. The protocol below is established to execute when participants are available.

### Scenario Matrix

| Task | Actor | Scenario | Expected Behavior | Observed / Feedback | Status |
|---|---|---|---|---|---|
| 1 | Dispatcher | Login and navigate to the Verify Packing screen. | Dashboard routes correctly, clear UI. | [Pending] | PENDING |
| 2 | Dispatcher | Upload a valid packaging image (`dataset/images/correct/correct_001.jpg`). | System evaluates quickly and displays "READY TO DISPATCH". | [Pending] | PENDING |
| 3 | Dispatcher | Upload a blurry/occluded image to trigger a Manual Review. | System safely catches the ambiguity and halts dispatch, displaying "HUMAN REVIEW REQUIRED". | [Pending] | PENDING |
| 4 | Manager | Login and open the Manual Review queue. | The queue clearly lists pending inspection IDs with time and confidence. | [Pending] | PENDING |
| 5 | Manager | Open a pending review and analyze the evidence. | The UI clearly highlights the captured image, triggered rules, and automated decision logic. | [Pending] | PENDING |
| 6 | Manager | Attempt to submit a decision *without* entering a comment. | System blocks submission and mandates an audit explanation. | [Pending] | PENDING |
| 7 | Manager | Enter a justification and override to "READY TO DISPATCH". | The decision processes successfully and the queue updates. | [Pending] | PENDING |
| 8 | QA / Admin | Open the Inspection History tab. | Both the initial inspection and the manager override are visible and accurate. | [Pending] | PENDING |
| 9 | Dispatcher | Simulate Network Failure (Offline), perform an inspection. | System accepts the payload into a local offline queue and alerts the user. | [Pending] | PENDING |
| 10| Dispatcher | Reconnect Network. | The pending offline inspection automatically synchronizes to the server. | [Pending] | PENDING |

## Synthesis & Implementation
Once stakeholders execute the tasks above, their qualitative feedback (e.g. "The button is too small", "I don't understand the confidence score") will be recorded in the `Feedback` column, prioritized by severity, and implemented into the frontend React application.
