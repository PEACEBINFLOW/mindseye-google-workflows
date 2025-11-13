# MindsEye + Google – System Flow

This doc tells the story version of what the YAML files are saying.

Think of it as the **lore** for how data moves through your Google + MindsEye stack.

---

## 1. Entry: Google Workspace as the outer shell

Everything starts with **events**:

- A Gmail thread gets a `MindsEye-*` label.
- A user clicks “MindsEye → Review with MindsEye” in a Google Doc.
- A Drive folder hits its daily summary trigger.
- A Forms response comes in for a new prompt node.

These are captured by **Apps Script** in:

- `mindseye-workspace-automation`

and normalized into a consistent shape:

```text
surface     = gmail / docs / drive / forms
source_id   = threadId / docId / folderId / formId
source_url  = link to the thing
title       = best-guess title
summary     = short text summary
event_type  = logical event name
