# Copilot Execution Instructions (python-devops)

## Purpose
Standardize AI-assisted issue-to-PR execution for `BytesCrafter/python-devops`.

## Core Flow (per ticket)
1. Create issue using `.github/ISSUE_TEMPLATE.md`
2. Add labels (`type:*`, `priority:*`, `area:*`)
3. Assign milestone + assignee
4. Create branch: `feat|fix|chore/issue-<N>-<slug>`
5. Implement scoped change
6. Commit in logical chunks (2-4 commits)
7. Push and open PR using `.github/PULL_REQUEST_TEMPLATE.md`
8. Link issue in PR body (`Closes #<N>`)

## Quality Gates
- Run local tests when available
- Keep changes scoped to ticket acceptance criteria
- Include rollback notes in PR
- Avoid unrelated refactors

## Commit Convention
- `feat: ...`
- `fix: ...`
- `chore: ...`
- `refactor: ...`
- `test: ...`
- `docs: ...`

## Suggested Labels
- Type: `type:feature|type:bug|type:chore|type:refactor|type:test|type:docs`
- Priority: `priority:p1|priority:p2|priority:p3`
- Area: `area:deps|area:changelog|area:tests|area:ci|area:security|area:architecture|area:reporting|area:docs`

## Milestone Routing
- Weeks 1-2 -> `M1 - Foundations (Weeks 1-2)`
- Weeks 3-4 -> `M2 - Quality & CI (Weeks 3-4)`
- Weeks 5-6 -> `M3 - Security & Extensibility (Weeks 5-6)`
- Weeks 7-8 -> `M4 - Reporting & Hardening (Weeks 7-8)`

## Safety Rules
- Never commit directly to `master`.
- Abort run if repo has unresolved conflicts.
- If CI is red after retry budget, comment findings and stop.
