# GitHub Ticket Format Standards

> Standard format for creating clear, actionable, and traceable GitHub tickets in the ERPat project.

---

## 📌 Purpose of This Document

This document defines the **standard GitHub Ticket Format** used across the ERPat project.  
Its goal is to ensure that **all tickets are clear, complete, traceable, and actionable**, regardless of whether they describe a bug, feature, enhancement, refactor, or compliance task.

This format is designed to:
- Reduce back-and-forth clarification
- Improve development speed and accuracy
- Support auditing, compliance, and historical tracking
- Align issues, pull requests, and changelogs

---

## 🧭 Guiding Principles

When creating a ticket:
1. **Clarity over length** – be specific, not verbose  
2. **Context matters** – include why the ticket exists  
3. **Future-proofing** – tickets should still make sense months later  
4. **General-purpose** – one format for all ticket types  
5. **Optional ≠ Ignored** – optional sections are encouraged when relevant  

---

## 🧩 Ticket Sections Overview

Each ticket is composed of **required** and **optional** sections.  
Not all sections need to be filled every time, but **required sections must always be completed**.

### 🔴 Required Sections
- Title  
- Reported By  
- Date Reported  
- ERPat Version  
- Description  
- Expected Result  

### 🟡 Conditionally Required
- Steps to Reproduce (for bugs)  
- Actual Behaviour (for bugs)  

### 🟢 Optional but Recommended
- Priority  
- Ticket Type  
- Impact / Risk  
- Proposed Solution  
- Acceptance Criteria  
- Additional Tasks  
- Technical Notes  
- Related Issues / PRs  
- Environment  

---

## 🧱 Standard GitHub Ticket Template

```md
# TITLE HERE

###### **REPORTED BY:** @username  
###### **DATE REPORTED:** MM/DD/YY  
###### **ERPAT VERSION:** ERPAT vX.X.X  
###### **TICKET TYPE:** Bug / Feature / Enhancement / Refactor / Compliance / Tech Debt  
###### **PRIORITY:** Low / Medium / High / Critical _(optional)_  

---

## **DESCRIPTION** _(Required)_
Explain the issue, feature, or improvement.
- What is happening or requested?
- Why is this important?
- Who is affected?

---

## **STEPS TO REPRODUCE** _(Required for Bugs | Optional for Others)_
1. Go to  
2. Navigate to  
3. Click  

**Image / Video / Log Reference:**  
PASTE (optional but encouraged)

---

## **ACTUAL BEHAVIOUR** _(Required for Bugs)_
Describe what currently happens.
- Errors
- Unexpected behavior
- Logs or warnings

---

## **EXPECTED RESULT** _(Required)_
Describe the correct or desired outcome.

---

## **IMPACT / RISK** _(Optional but Recommended)_
- Affected users or modules
- Business / payroll / compliance impact
- Risk if left unresolved

---

## **PROPOSED SOLUTION** _(Optional)_
High-level approach only (no deep implementation):
- Logic changes
- UI changes
- Configuration
- Refactor / migration

---

## **ACCEPTANCE CRITERIA** _(Recommended for Features & Refactors)_
- [ ] Criteria 1  
- [ ] Criteria 2  
- [ ] No regression introduced  
- [ ] Works under expected environment  

---

## **ADDITIONAL TASKS** _(Optional)_
- [ ] Documentation updates  
- [ ] Migration scripts  
- [ ] Unit / regression tests  
- [ ] QA validation  
- [ ] Permission updates  

---

## **TECHNICAL NOTES** _(Optional)_
- Files affected  
- Database tables  
- APIs or helpers involved  
- Known constraints  

---

## **RELATED ISSUES / PRs** _(Optional)_
- Related Issue: #XXXX  
- Related PR: #XXXX  
- Log reference or link  

---

## **ENVIRONMENT** _(Optional – Useful for Bugs)_
- PHP Version:  
- Database:  
- Browser / OS:  
- Server / Hosting:  
```

---

## 🏷 Ticket Type Guidelines

| Ticket Type   | Usage                                   |
|---------------|-----------------------------------------|
| **Bug**       | Something is broken or incorrect        |
| **Feature**   | New functionality                       |
| **Enhancement** | Improvement to existing feature      |
| **Refactor**  | Code restructuring, same behavior       |
| **Compliance**| Government, legal, security requirements|
| **Tech Debt** | Cleanup, modernization, performance     |

---

## 🚦 Priority Guidelines

| Priority   | When to Use                              |
|-----------|-------------------------------------------|
| **Low**   | Cosmetic, non-blocking                    |
| **Medium**| Usability or minor logic issues           |
| **High**  | Affects core workflows or major modules   |
| **Critical** | Payroll, compliance, security, outages |

---

## 🧪 Acceptance Criteria Best Practices

Acceptance Criteria should:
- Be **testable**  
- Be **binary** (pass/fail)  
- Avoid vague words like "should be okay"

**Example:**
```md
- [ ] created_by must never be NULL  
- [ ] No PHP warnings under PHP 8.2  
- [ ] Works for Admin and Staff roles  
```

---

## 🔗 Relationship Between Tickets, PRs & Changelog

- **GitHub Issue** → defines *what & why*  
- **Pull Request** → defines *how*  
- **Changelog** → defines *what shipped*  

Guideline:
- Every **PR** should reference at least one **Issue**  
- Every **Changelog entry** should reference at least one **PR**  

---

## ✅ Best Practices Checklist

Before submitting a ticket:
- [ ] Title is clear and specific  
- [ ] Description explains the business impact  
- [ ] Expected Result is unambiguous  
- [ ] Steps to Reproduce are included (if bug)  
- [ ] Screenshots/logs attached if helpful  

---

## 📌 Final Notes

This format is:
- **Flexible, not rigid**  
- Designed to grow with ERPat  
- Optimized for collaboration, audits, and long-term maintenance  

All contributors are expected to follow this format unless explicitly instructed otherwise.
