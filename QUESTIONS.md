# Questions Before Implementation

## Critical Setup Questions

### 1. Email Address for Galah Configuration (REQUIRED)
The galah Python package requires an email address to be configured for accessing the Atlas of Living Australia (ALA) API.

**Question:** What email address should I use for the galah configuration?

```python
galah.galah_config(
    atlas="Australia",
    email="???"  # Required for ALA access
)
```

w.mcalister@gmx.com

---

## Implementation Strategy Questions

### 2. Testing Approach
Processing all 297 species will take significant time (minimum ~60 seconds with rate limiting, plus processing overhead).

**Question:** Should I:
- A) Test on a small subset first (e.g., 10-20 species) to verify the approach works, then run the full batch?
- B) Run the full 297 species immediately?

A! ---

### 3. Multi-Source Strategy
The backlog focuses on using galah to access ALA exclusively. However, the original instructions (`bird_photo_agent_instructions.md`) specify a priority order:
1. Wikimedia Commons (preferred)
2. Atlas of Living Australia (secondary)
3. iNaturalist (tertiary)

The existing script tried all three sources but failed completely (0 photos found).

**Question:** Should I:
- A) Use galah for ALA ONLY (as per backlog)?
- B) Combine galah (ALA) with Wikimedia Commons and iNaturalist (as per original instructions)?
- C) Use galah as primary, and only try other sources if galah finds fewer than N photos?

C!

---

### 4. Code Organization
There's an existing `search_photos.py` script that didn't work.

**Question:** Should I:
- A) Replace the existing `search_photos.py` with the new galah-based implementation?
- B) Create a new script (e.g., `search_photos_galah.py`) and keep the old one for reference?

Actually, the old script might have failed because of the environment in which it was run. Could you please test it and see if it is working from this computer? 

---

### 5. Audio Implementation Priority
The backlog includes both photo search (Phase 2) and audio search (Phase 4).

**Question:** Should I:
- A) Implement both photos and audio in the same run?
- B) Implement photos first, verify they work, then implement audio separately?

B!

---

### 6. Photos Per Species
The backlog specifies `max_photos=5` per species.

**Question:** Is 5 photos per species the desired target, or would you prefer a different number?
Aim for 5 photos per species but less is ok if you can't find enough.

---

## Technical Questions

### 7. Python Environment
**Question:** Should I:
- A) Install packages globally in the current Python environment?
- B) Create a virtual environment first?

B!

---

### 8. License Preferences
The backlog lists acceptable licenses with varying permissions. Within the acceptable licenses, should I prefer:
- A) Most permissive first (CC0 > CC BY > CC BY-SA > CC BY-NC > CC BY-NC-SA)?
- B) No preference, just take the first acceptable license found?

**Recommendation:** Option A (prefer most permissive).

---

### 9. Error Retry Strategy
The backlog mentions "retry up to 3 times with exponential backoff" for network errors.

**Question:** What backoff parameters should I use?
- Initial delay: 1 second? 2 seconds?
- Backoff multiplier: 2x?

**Example:** Attempt 1 → wait 1s → Attempt 2 → wait 2s → Attempt 3 → wait 4s → fail

**Recommendation:** Start with 1 second initial delay, 2x multiplier, 3 max attempts.

---
