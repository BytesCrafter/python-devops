## 📌 Purpose of This Document
This document defines the **standard GitHub Pull Request (PR) format** used across the ERPat project.  
Its goal is to ensure that every PR is:

- Clear and easy to review  
- Properly linked to its corresponding issue(s)  
- Testable and safe to deploy  
- Useful for future audits, debugging, and changelog generation  

This format is designed to work for **any type of change**:
- Bugfixes  
- New features  
- Enhancements  
- Refactors / tech debt  
- Compliance / security updates  

---

## 🧭 Guiding Principles

When creating a PR:

1. **Explain the “why” and “what” first** – reviewers should understand intent quickly.  
2. **Keep sections practical** – no filler, only useful info.  
3. **Call out risk and impact** – especially for payroll, security, infra, and migrations.  
4. **Make it testable** – Acceptance Criteria + Testing Results should tell QA exactly what to verify.  
5. **Keep it reusable** – same structure works for small and big PRs.

---

## 🧩 Section Types (Required vs Optional)

### 🔴 Required Sections
These must be present in every PR:
- Title  
- Summary  
- Features / Changes Implemented  
- Files Modified  
- Testing Results & Acceptance Criteria  

### 🟡 Conditionally Required
Required **if applicable**:
- Linked Issues (if tied to a ticket)  
- Files Added (if new files exist)  
- Documentation & Deployment Notes (if behavior/config changed)  

### 🟢 Optional but Recommended
- PR Type & Scope  
- Impact / Risk (can be inside Summary or as separate field)  
- Breaking Changes  
- Rollback Plan  
- Known Limitations / Pending Items  
- Screenshots / Recordings  
- Technical Notes  
- Environment (for environment-sensitive changes)

---

## 🧱 Standard GitHub PR Template

```md
# TITLE HERE

## **SUMMARY** _(Required)_
Short, clear explanation of what this PR does and why.
- What problem does it solve or what feature does it add?
- Which parts of the system are affected? (e.g., Attendance, Payroll, POS)

---

## **LINKED ISSUES** _(Required if applicable)_
- Closes #ISSUE_ID  
- Relates to #ISSUE_ID  

---

## **PR TYPE & SCOPE** _(Optional but Recommended)_
- Type: Bugfix / Feature / Enhancement / Refactor / Tech Debt / Compliance  
- Scope: Small / Medium / Large  

---

## **FEATURES / CHANGES IMPLEMENTED** _(Required)_
List the main changes in bullet form.
- Added ...  
- Updated ...  
- Fixed ...  
- Removed / Deprecated ...  

---

## **FILES ADDED** _(Optional – Required if new files exist)_
- `path/to/new_file_1.php` – short description  
- `path/to/new_file_2.php` – short description  

## **FILES MODIFIED** _(Required)_
- `path/to/modified_file_1.php` – what changed  
- `path/to/modified_file_2.js` – what changed  

---

## **TECH STACK DETAILS** _(Optional)_
Note any relevant technical context:
- Framework / version  
- New libraries / dependencies  
- Database changes (new tables, columns, indexes)  

---

## **TESTING RESULTS & ACCEPTANCE CRITERIA** _(Required)_

### Testing Performed
- [ ] Local manual testing  
- [ ] Staging testing  
- [ ] Unit tests  
- [ ] Integration tests  

### Test Notes
- Scenario 1: TYPEHERE  
- Scenario 2: TYPEHERE  

### Acceptance Criteria
- [ ] Criteria 1 met  
- [ ] Criteria 2 met  
- [ ] No regression in related module(s)  
- [ ] Works under expected environment (PHP version, browser, role, etc.)  

---

## **BREAKING CHANGES** _(Optional but strongly recommended)_
- Does this introduce breaking changes? **Yes / No**  
- If **Yes**:
  - What breaks? (API, UI, DB structure, permissions, etc.)
  - Required actions: migrations, config updates, data changes, etc.

---

## **ROLLBACK PLAN** _(Optional but Recommended)_
How to safely revert if needed:
- [ ] Revert commit / PR  
- [ ] Run rollback migration `YYYYMMDD_rollback_xyz`  
- [ ] Restore config / ENV variables  
- Notes: TYPEHERE  

---

## **KNOWN LIMITATIONS / PENDING ITEMS** _(Optional)_
- Limitation 1  
- Limitation 2  
- TODO / Future ticket: TYPEHERE  

---

## **SCREENSHOTS / SCREEN RECORDINGS** _(Optional but encouraged)_
_Add before/after screenshots, GIFs, or links to recordings._  
- Screenshot 1: TYPEHERE  
- Screenshot 2: TYPEHERE  

---

## **DOCUMENTATION & DEPLOYMENT NOTES** _(Required if behavior or config changed)_

### Documentation
- [ ] Updated internal docs (Wiki / Notion / README)  
- [ ] No documentation impact  

Details: TYPEHERE  

### Deployment Notes
- Migrations: TYPEHERE (e.g., `php index.php migrations latest`)  
- Crons / Workers: TYPEHERE  
- Config: TYPEHERE (e.g., new ENV vars)  
- Other: TYPEHERE  
```

---

## ✅ Best Practices Checklist for Authors

Before submitting a PR:
- [ ] Linked at least one Issue (if applicable)  
- [ ] Clearly explained Summary and Changes  
- [ ] Listed all important modified files  
- [ ] Documented any migrations or config changes  
- [ ] Ran tests and documented results  
- [ ] Called out any breaking changes and rollback plan  
- [ ] Attached screenshots for UI changes  

This template keeps PRs consistent, reviewable, and safe to merge across all ERPat modules.
