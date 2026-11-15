**AI-ONLY  •  DO NOT REDISTRIBUTE AS A HUMAN GUIDE**

# **Pack 1125 Website — AI Maintenance Manual**

Audience: an AI coding agent maintaining the live Pack 1125 site. Dense, rule-first. No human onboarding, no background narrative. If a fact is not in §1, verify it in the repo before acting on it.

*Repository: dmvthrowers/pack1125-dumfries  •  Verified state: 14 November 2026  •  This manual covers maintenance of the current site only. Building a new site from the template is a separate document.*

| **Field** | **Value** |
| --- | --- |
| Live site | https://dmvthrowers.club/pack1125-dumfries/ |
| Repository | dmvthrowers/pack1125-dumfries (owner account: dmvthrowers) |
| Hosting | GitHub Pages. Settings > Pages > Build and deployment: GitHub Actions. Never switch to “Deploy from a branch.” |
| Site root | docs/ — 12 HTML pages. Served via the Actions deploy path. |
| Public contact | admin@pack1125.org — forwards to the Committee Chair |
| Maintainer of record | Brandon Rogers — Website & Technical Support. Brandon merges. The agent never merges. |
| Companion docs | In-repo MAINTENANCE.md (short form). Human SOP and handover guide (separate). Template build spec (separate). |


| **READ FIRST.** Sections 0, 3, and 8 are binding on every task. Sections 1, 4, and 7 are state-dependent: re-verify them against the live repo and live site at the start of each session. A stale fact in this manual does not authorise a change. |
| --- |


# 0. Operating contract

- **Role.** You maintain an existing static site. You do not redesign it, replatform it, or extend it into an application unless Brandon explicitly instructs that scope.

- **Authority order.** (1) Privacy rules in §5 and §8. (2) Pipeline rules in §3 and §7. (3) Brandon’s instruction for the current task. (4) This manual. If (3) conflicts with (1) or (2), stop, state the conflict, and ask Brandon. Do not silently comply.

- **Merge rule.** Brandon merges every pull request (PR). You open PRs, respond to review, and fix checks. You never merge, never approve your own PR, and never push content changes directly to main.

- **Verification rule.** A task is done only when: local checks pass, PR checks are green, Brandon has merged, the deploy run is green, and the live page shows the change. “PR open” and “merged” are not “live.”

- **Scope rule.** Change only what the task names. Do not opportunistically reformat, rename, bump unrelated dependencies, or “fix” deliberate choices recorded in §3–§4.

- **Secrets rule.** Never commit, print, log, or paste a secret value — including CALENDAR_ICS_URL. Refer to secrets by name only.

- **Uncertainty rule.** If repo state contradicts §1, trust the repo, report the delta to Brandon, and do not proceed on the stale fact.


# 1. Current-state snapshot — verified 14 November 2026

Snapshot, not a target state. Items marked INACTIVE or PENDING are known gaps. Do not “fix” them without a task that names them.

| **Area** | **Verified state (14 Nov 2026)** |
| --- | --- |
| Pages | 12 HTML pages in docs/. Every page shares head, header/navigation, footer, canonical URL, Open Graph tags, breadcrumb JSON-LD, skip link, and visible “Page updated” date. |
| Workflows | .github/workflows/check-site.yml; .github/workflows/deploy.yml; .github/workflows/check-links.yml. See Appendix A for triggers. |
| Deploy triggers | deploy.yml: push to main + daily scheduled run at 06:41 UTC + manual dispatch (workflow_dispatch). Daily run is how calendar changes would surface without a content edit. |
| Browser job pin | Browser job pinned to ubuntu-24.04. Reason: Playwright 1.56.1 cannot install Chromium on the Ubuntu 26.04 runner image. Pin is load-bearing. See §7. |
| Deploy history | Deploy freeze 24 Oct – 14 Nov 2026. Fixed by PR #20 (pin). First green deploy after the freeze: 14 Nov 2026, 20:10 EST. |
| Photo permission form | LIVE. https://docs.google.com/forms/d/e/1FAIpQLSfLMYSqmwUZk10rP2-4-G3mQDKNnuH5hnJSFoZZWpIjUpX64g/viewform — linked from New Families and Privacy pages. Collects parent/guardian name + email, Scout first name + den, one choice: opt in / opt out / remove a photo. One form per Scout. |
| Custom domain | PENDING. pack1125.org still serves a registrar Coming Soon page (A 198.18.117.188 / 198.18.117.189). It is NOT pointed at GitHub Pages. Live canonical base remains https://dmvthrowers.club/pack1125-dumfries/. Do not rewrite canonicals, sitemap URLs, or JSON-LD URLs to pack1125.org until the domain move is executed as its own task. |
| Calendar sync | INACTIVE. CALENDAR_ICS_URL secret is not set. Live calendar events list is empty. Calendar page falls back to static content / regular meeting schedule. Build does not fail when the secret is absent — this failure is silent. See §4. |
| Config | docs config in config.js. BeAScout pin link is still generic in config.js — not yet replaced with the pack-specific pin. Do not invent a pin URL. |
| Gallery | Published gallery photos are web copies only: faces blurred, EXIF stripped, JPG + WebP, each file < 500 KB. Originals never live in the repo. |


## People and money facts — copy exactly, never paraphrase into different figures

| **Item** | **Value** |
| --- | --- |
| Cubmaster | Clive Vella |
| Committee Chair | Andy Tainter — receives admin@pack1125.org; approves policy-level changes (privacy wording, photos, dues figures) |
| Website & Technical Support | Brandon Rogers — site builder and maintainer of record; sole merger |
| Pack dues | $100 / year (pack dues) |
| National dues | $85 (national) |
| Council fee | $80 NCAC — first-year. First-year total as presented: $100 + $85 + $80. Do not collapse these into a single figure without showing the breakdown. |
| Charter / council | Chartered by Future Kings, Inc. National Capital Area Council (NCAC), Prince William District. |
| Meeting pattern (as published) | Covington-Harper Elementary School auditorium. Pack meetings 1st Thursday, den meetings 3rd Thursday, 18:30–19:30. Confirm against the live page before restating — do not treat this line as a source for a calendar edit. |


| **KNOWN-GAP LIST.** Three gaps are expected state, not bugs to auto-fix: (a) CALENDAR_ICS_URL not set; (b) pack1125.org not pointed at Pages; (c) BeAScout link generic in config.js. Each needs its own authorised task. Log them if you encounter them; do not remediate them inside an unrelated PR. |
| --- |


# 2. Change workflow

Applies to every content, code, workflow, and config change. The only exception is a one-line typo fix Brandon explicitly authorises as a direct edit — default is still PR.

1. **Step 1 — Get an exact brief.** Page/file, exact old text, exact new text (or exact asset + destination). Reject vague briefs (“update the camping bit”) back to Brandon for specifics before editing.

1. **Step 2 — Branch.** Create a feature branch from current main. Never work on main. Branch names: short, descriptive, hyphenated (e.g. fix/calendar-copy, content/dec-17-potluck). One concern per branch.

1. **Step 3 — Edit minimally.** Edit the HTML file(s) in docs/. Match existing structure: head, navigation, content, footer. Do not paste formatting from Word, email, or a rich-text editor. Do not reformat untouched lines.

1. **Step 4 — Bump dates together.** For every page you change: update its visible “Page updated” date AND its <lastmod> in sitemap.xml to the same new date, in the same commit set. Mismatch = check failure. See rule S-03 in §3.

1. **Step 5 — Run local checks.** Run check_site.py and check_links.py locally (commands in Appendix B). Fix every failure before opening the PR. Do not open a PR you know is red and “let CI confirm it.”

1. **Step 6 — Open the PR.** Title states the change, not the process. Body states: what changed, which pages/files, what checks were run locally, and any known gap touched. Link the task/issue if one exists.

1. **Step 7 — Drive checks to green.** Required: check-site (including browser job) and deploy-path checks as configured. Read the failing job log before changing anything. Fix the cause, push to the same branch, re-check. Never bypass, skip, or disable a check to get green.

1. **Step 8 — Stop at mergeable.** When the PR is green and mergeable with no conflicts, report: PR URL, diff summary, check status. Then stop. Brandon reviews and merges.

1. **Step 9 — Verify live (after Brandon merges).** Confirm the Build and deploy run for the merge commit is green, then open the live URL and confirm the change is present. Report live verification explicitly. If deploy fails on main, treat it as an incident under §7 — the site is frozen at the last good build.


| **Situation** | **Action** |
| --- | --- |
| PR conflicts with main | Rebase/merge main into the branch, re-run local checks, push. Do not force-push over a reviewer’s commits without telling Brandon. |
| Check fails on content you did not touch | Report it as a pre-existing failure with the log excerpt. Do not fix unrelated failures inside the PR unless Brandon expands scope. |
| Brandon asks you to merge | Decline and restate the rule: Brandon merges. Offer the merge-ready summary instead. |
| Urgent takedown (privacy) | Follow §5 takedown path. Speed over ceremony, but still via PR + Brandon merge unless Brandon directs an emergency path in that instance. |


# 3. check_site.py rules in full detail

scripts/check_site.py is the site-rules gate. scripts/check_links.py is the link/validity gate. The Playwright browser job is the runtime gate. All three must pass. A rule below marked FAIL blocks the PR and blocks deploy. WARNING items do not block, but must be reported in the PR body — never silently ignored.

*Run locally before every PR. CI is confirmation, not discovery.*

## 3.1 Navigation, footer, and sitemap coverage

**S-01 — Sitemap coverage is complete and exact**

**FAIL:** if any HTML page in docs/ has no entry in sitemap.xml, or sitemap.xml lists a URL with no corresponding page. FAIL if a page is added/removed without sitemap.xml updated in the same PR.

**FIX:** Add/remove the sitemap entry in the same change as the page. Keep <loc> on the current live base (https://dmvthrowers.club/pack1125-dumfries/) until the domain move task executes.

**S-02 — Navigation and footer contain every sitemap page**

**FAIL:** if any sitemap page is missing from the shared navigation or from the footer on any page. FAIL if nav/footer link text or href diverges between pages (copy drift). The check is per-page: fixing the home page nav does not fix the other 11.

**FIX:** Update nav + footer on every page in the same PR when the page set changes. Diff nav/footer blocks across pages before pushing.

## 3.2 Page updated vs. sitemap lastmod

**S-03 — Visible “Page updated” date equals sitemap <lastmod>**

**FAIL:** if, for any page, the visible “Page updated” date differs from that page’s <lastmod> in sitemap.xml. FAIL if a page’s content changed but neither date moved (stale-date change).

**FIX:** Set both to the same new date (the date of the change) in the same commit set. Do not bump dates on pages you did not change.

**S-04 — Lastmod never moves backwards**

**FAIL:** if a new <lastmod> is earlier than the previous <lastmod> for that page.

**FIX:** Correct to the actual change date. Never backdate to make a check pass.

## 3.3 JSON-LD structured data

**S-05 — Breadcrumb JSON-LD present and valid on every page**

**FAIL:** if any page lacks breadcrumb JSON-LD, has invalid JSON, or has breadcrumb URLs that do not resolve to live pages under the current base. FAIL if canonical URL, Open Graph URL, and JSON-LD URL for a page disagree.

**FIX:** Restore the shared head pattern from an untouched page. Keep all three URL fields identical per page.

**S-06 — Event JSON-LD matches visible event content**

**FAIL:** if Event JSON-LD names, dates, or locations disagree with the visible events list / calendar content on the same page. FAIL if structured data is added for an event that is not visibly listed.

**FIX:** Edit visible content and JSON-LD together. If you cannot keep them in sync, remove the Event block rather than leaving it stale.

**S-07 — Past-event warning**

WARNING (report in PR body) when Event JSON-LD or a visible “upcoming events” entry has an end date in the past. The event is stale content, not upcoming. Repeated pattern on this site: expired home-page event cards left in the “upcoming” data after the date passed (e.g. the 1 Nov Fall Camp and 5 Nov meeting entries cleaned up in Nov 2026).

**FIX:** Remove the past event from upcoming lists, or move it to an explicit past/recap presentation if Brandon asks for a recap. Never leave a past date labelled as upcoming. Never auto-delete without confirming whether a recap is wanted when the task is ambiguous.

## 3.4 Content Security Policy (CSP)

**S-08 — Strict CSP on every page, no widening**

**FAIL:** if any page lacks the Content-Security-Policy, weakens it, or triggers a CSP error in the browser job. Policy intent: default-src 'self'; scripts, styles, fonts, and images only from the site itself; no framing, no objects, no form actions. FAIL if an external script, stylesheet, font, or image is introduced.

**FIX:** Self-host the asset or remove it. Fonts are self-hosted for this reason. Do not add CDN links, embeds, analytics, or tracking to satisfy a content request.

**S-09 — Single exception: Google Calendar frame, Calendar page only**

**FAIL:** if the calendar frame allowance appears on any page other than the Calendar page, or if the policy is widened site-wide to fix a one-page embed. On the Calendar page, the embed loads only after the visitor clicks “Show the Calendar” — preserve that click-to-load behaviour.

**FIX:** Scope any frame allowance to the Calendar page head only. If the embed breaks, fix the Calendar page; never edit the shared policy.

## 3.5 Images

**S-10 — Image file size, format, and metadata**

**FAIL:** if any published image exceeds 500 KB. FAIL if a gallery image lacks its pair (JPG + WebP). FAIL if EXIF/metadata — especially GPS/location — is present on a published photo.

**FIX:** Export JPG + WebP, each < 500 KB, EXIF stripped, into docs/images/gallery/ (gallery) or the page’s existing image location. Re-export; do not commit the original.

**S-11 — Alt text and external loading**

**FAIL:** (browser/accessibility gate) on missing alt text for content images, or on any image loaded from outside the site. Pure decoration uses alt="" only.

**FIX:** Write meaningful alt text describing the activity, not a child’s identity. Never put a Scout’s name in alt text, captions, or filenames.

## 3.6 Browser and link gates (enforced alongside check_site.py)

**S-12 — Browser job: layout, accessibility, isolation**

**FAIL:** if Playwright finds, at 360 px (phone) or 1,280 px (desktop): horizontal scrolling, a serious accessibility violation, a resource loaded from outside the site, or a CSP error. Applies to every page.

**FIX:** Reproduce at the failing width first. Fix the page/CSS causing it. Do not suppress the axe/accessibility rule or the width to get green.

**S-13 — Link gate: check_links.py + check-links.yml**

**FAIL:** if markup is invalid (W3C validation) or any external link does not return 200. check-links.yml also runs monthly on a schedule, so link rot can fail main without any code change.

**FIX:** Replace the dead link with its current live target (verified by opening it) or remove the link. Do not leave a known-dead link and note it as “later.” Monthly failures on main are real defects: open a fix PR.

| **INTERPRETATION RULE.** If check output and this section disagree, the script’s current output wins for that run. Quote the exact failing rule and page in the PR body. Do not paraphrase a failure into a pass. |
| --- |


# 4. Calendar sync

Scripts: scripts/sync_calendar.py + scripts/publish_events.py. Execution: build time only, inside the deploy workflow. There is no runtime fetch by the visitor’s browser for the events list, and nothing is committed back to the repo by the sync.

| **Property** | **Rule** |
| --- | --- |
| Source | Pack Google Calendar, via its secret iCal feed address held as repo secret CALENDAR_ICS_URL (“Secret address in iCal format”). Read-only feed. |
| Current state | INACTIVE. Secret not set (14 Nov 2026). Sync step does nothing; build succeeds; live events list is empty. Do not claim the calendar is “working” because the build is green. |
| When it runs | As part of deploy.yml builds: push to main, daily 06:41 UTC, manual dispatch. A calendar-only change surfaces on the next build; there is no separate publish step. |
| Horizon | 180 days. Events beyond 180 days from build date are not published to the site list. Do not extend the horizon to “show the whole year” without Brandon’s instruction. |
| Visibility filter | Only events marked Public are published. Publish title, date/time, location, and Public: description content only. Never publish private-event details, attendee lists, or internal notes. If an event’s visibility is ambiguous, exclude it. |
| Write-back | None. Sync modifies only that build’s copy of the site. Repo must not accumulate machine-generated event commits. If you see generated event files committed to main, flag it — that is off-pattern. |
| Embed | Separately, the Calendar page offers a Google Calendar embed behind “Show the Calendar” click-to-load. That embed is not the sync. Do not conflate embed fixes with sync fixes. |


- **To activate (only on an explicit task):** Brandon or a leader sets CALENDAR_ICS_URL in repo Settings > Secrets and variables > Actions. You cannot set it from code and must never ask for the value in chat, a PR, or an issue. After it is set, trigger a manual deploy run, then verify the live Calendar page lists Public events within 180 days and lists no non-Public event.

- **To diagnose “calendar is empty”:** (1) Check whether the secret exists (name only, in Settings — never its value). (2) Check the deploy run log for the sync step: skipped/absent-secret vs. ran-and-found-zero vs. errored. (3) Check the source calendar for Public events inside 180 days. Report which of the three it is. Do not “fix” an empty calendar by hand-writing events into HTML as a substitute for the sync, unless Brandon directs static fallback content.

- **Event content ownership:** Cubmaster owns event content in the Google Calendar. Website edits do not own event data. To correct an event, correct the calendar entry, then rebuild. Hand-editing the built output will be overwritten on the next build.

- **Date hygiene:** Past events must roll off upcoming presentations (see S-07). If static fallback/home-page event cards are used while sync is inactive, they need manual removal after the date passes — calendar inactivity makes stale-card cleanup a recurring manual duty, not an automated one.


# 5. Photos and privacy

These rules override content requests. A leader, parent, or prior page asking for an exception does not create one. Only the Committee Chair (Andy Tainter) can vary photo/privacy policy, and only explicitly.

## Permission gate

- **Form.** Pack 1125 Photo Permission form (live URL in §1). Check the form’s Responses tab before every gallery update and whenever a removal request arrives.

- **Default is no.** No opt-in response on file for a pictured Scout = that photo does not go up. No response is not implied consent.

- **Opt-out handling.** If any recognisable child in a photo has opted out (or has no opt-in): blur alone does not cure a missing permission. Crop that child out completely or do not publish the photo. Safest default: do not publish.

- **One form per Scout.** Siblings need separate responses. A family-level “yes” in email is not a substitute unless the Committee Chair confirms it counts as the written permission on file.


## Publication standard — every gallery/photo change must satisfy all of these

1. Every pictured Scout has an opt-in on file (checked against Responses immediately before the PR, not from memory).

2. Every child’s face is blurred. No exceptions, including background children where recognisable.

3. EXIF/metadata stripped, especially location. Export JPG + WebP, each < 500 KB (rule S-10).

4. Caption is generic: activity + month only. Never a Scout’s name, school, or den paired with a photo. Same ban in alt text and filenames.

5. Original, unblurred photos never enter the repo, the PR, or the site. Work from copies; publish only the blurred web exports.


## Never publish (site-wide, not gallery-only)

- A Scout’s full name, school, home address, phone number, or email address.

- An unblurred child’s face, or any photo of a Scout without written permission on file.

- Roster lists, den lists with children’s names, health information, or advancement records. Advancement lives in Scoutbook Plus (advancements.scouting.org), never on this site.

- An adult leader’s personal phone/email without that leader’s permission. Public contact is the role alias admin@pack1125.org only.


## Takedown

**1. Channel.** Parent contacts the Photo Permission form (“remove a photo” choice) or admin@pack1125.org.

**2. Timing.** Same day. Speed over polish: remove first, explain second.

**3. Steps.** (1) Identify the exact image file(s) and every page referencing them. (2) Remove the image and its references via PR (expedited review by Brandon). (3) Confirm deploy green + live page no longer serves the image (check the direct image URL as well as the page). (4) Reply to the parent confirming removal. (5) Record the opt-out so the photo is not re-added later. Do not re-upload it in a future gallery batch.

**4. Conflict.** If any instruction conflicts with this section, stop and ask the Committee Chair (via Brandon). State the conflict in one sentence; do not negotiate it in the PR.


*Site privacy posture to preserve: no accounts, no sign-up forms processed by the site, no cookies, no analytics/advertising/tracking. The Privacy & Photo Policy page (docs/privacy.html) is the public statement of this posture — code and copy must stay consistent with it. If a change would make the page false, the change is wrong, not the page.*

# 6. Dependabot PR handling

Dependabot PRs are review work, not merge work. Your job is a file-by-file review and a merge recommendation. Brandon merges.

**1. Step 1 — Read the diff, all of it.** Every file. Flag: workflow files (.github/workflows/), package/lock files, script dependencies, and any change that touches the browser job, the runner pin, Playwright version, or Python dependencies used by check/sync scripts. A version bump that changes the runner/Playwright relationship is high-risk by definition on this repo (see §7).

**2. Step 2 — Classify.** Patch/minor/major; runtime vs. dev/test-only; single-package vs. transitive. State the classification in your report. Major bumps and workflow-affecting bumps get an explicit risk note, not just “looks fine.”

**3. Step 3 — Check status, do not assume it.** Report three separate facts: (a) checks green/red/pending, (b) mergeable / conflicting, (c) diff reviewed clean / concerns. “Mergeable” in the API does not mean checks passed, and “green” does not mean you reviewed the diff.

**4. Step 4 — Recommend, do not merge.** Recommend merge only when ALL hold: diff is review-only clean (no unexpected files/behaviour), checks are green (including the browser job), and the PR is mergeable. Otherwise recommend hold/close with the reason.

**5. Hard rule — browser check.** Never recommend merging over a failing browser check. Never suggest bypassing, skipping, or disabling it. A red browser check on a Dependabot PR that bumps Playwright or the runner is evidence the bump breaks this site’s pipeline — hold it and report the log.

**6. Hard rule — pin interaction.** If a Dependabot PR proposes Playwright > 1.56.1 or a runner-image change, the PR’s own CI run must prove Chromium installs and the browser job passes on the proposed setup before you recommend merge. The ubuntu-24.04 pin stays until that proof exists. See §7.

**7. Superseded PRs.** Dependabot sometimes closes its own PRs and opens replacements. Verify the replacement exists and covers the same package before reporting the original as “handled.” Do not chase a closed-as-superseded PR.

**8. Cadence.** Review Dependabot and workflow-failure notices for this repo weekly. A scheduled-workflow failure on main is a defect (site frozen), not background noise.


| **Finding** | **Recommendation** |
| --- | --- |
| Diff clean + checks green (incl. browser) + mergeable | Recommend merge. Brandon merges. |
| Diff clean + checks pending | Wait. Re-check. Do not recommend yet. |
| Diff clean + browser check red | Hold. Report failing step + log excerpt. Do not override. |
| Unexpected files / workflow change not described in PR body | Hold. List the unexpected files. Ask Brandon. |
| Conflicting / not mergeable | Hold. Note the conflict. Do not rebase a Dependabot PR yourself unless Brandon asks. |


# 7. Deploy troubleshooting

Failure mode by design: a failed check blocks deploy and Pages keeps serving the last good build. The site goes stale, never half-broken. Treat “stale” as an incident when it persists: two consecutive daily deploy failures = incident.

**1. Step 1 — Identify the failing job.** Open Actions > newest Build and deploy run. Name the failed job: check-site (content/rules), browser job (Playwright), or deploy step. Record the commit SHA the run was for. Do not change anything before reading the log.

**2. Step 2 — Read the failed step’s log.** Quote the exact error line in your report. Classify: content failure (fix the page), link failure (fix the link), environment failure (runner/browser install), or platform failure (GitHub incident). Local-pass + CI-fail points to environment, not content.

**3. Step 3 — Apply the matching fix only.** Content: fix per §3. Links: fix per S-13. Environment: check the runner pin first (below). Platform: wait; do not restructure the site during a GitHub outage. Tell Brandon the site is stale-but-up; urgent comms go by email/Scoutbook.

**4. Step 4 — Re-run and verify live.** Re-run via push or manual dispatch. Confirm green, then open the live site and confirm current content. A green run you did not verify live is not a closed incident.

**5. Step 5 — Write it down.** Record cause + fix in MAINTENANCE.md or a repo issue before closing. The freeze below lasted weeks in part because the pattern had to be re-diagnosed from email notices.


## Known failure: browser job dies in seconds during setup

| **PIN RULE.** The browser job must run on ubuntu-24.04 (.github/workflows/check-site.yml). Never remove the pin unproven. “Unproven” means: no PR CI run on the newer image showing Playwright installing Chromium and the full browser job passing. A successful local run does not prove the runner image. |
| --- |


Signature: browser job fails within seconds, before testing any page; deploy skipped; check-site content checks may still pass; same failure repeats on the same commit and on scheduled runs. First check: runs-on value for the browser job. If it reads ubuntu-latest or ubuntu-26.04 (or any image newer than 24.04 without proof), restore the pin via PR.

## Case study: the October–November 2026 deploy freeze (worked example)

| **Phase** | **What happened** |
| --- | --- |
| Onset — 24 Oct 2026 | Build and deploy workflow began failing repeatedly on the same commit (fbb88f5). Browser/check job failed in seconds; deploy skipped each time. Live site stopped redeploying. |
| Misleading signal | Local runs of the same checks passed on all pages. Content was not the fault. Failure notices arrived as GitHub “Run failed” emails and recurred 24 Oct, 26 Oct, 29 Oct, 2 Nov, and beyond — easy to file as noise. It was not noise: every failure meant zero deploys. |
| Root cause | GitHub’s ubuntu-latest image had moved to Ubuntu 26.04. Playwright 1.56.1 cannot install Chromium on 26.04. The browser job died in setup, before any page test ran. |
| Fix — PR #20 | Pin only the browser job to ubuntu-24.04 in .github/workflows/check-site.yml. No content changes. No check weakened. |
| Resolution — 14 Nov 2026 | PR #20 merged by Brandon. First green deploy since 24 Oct: 14 Nov 2026, 20:10 EST. Live site verified serving again. Blocked Dependabot work (e.g. pack PR #19, held by the same red browser check) unblocked only after the pipeline went green. |
| Lessons (binding) | (1) Fast browser-setup failure = suspect the runner environment first. (2) Never merge on red to “just get it live.” (3) Never remove the pin without in-PR proof. (4) Two consecutive daily failures = incident, not backlog. (5) Write the diagnosis down the day it is found. |


## Other deploy faults — quick map

| **Symptom** | **Likely layer** | **Action** |
| --- | --- | --- |
| check-site fails, log names a page + rule | Content / §3 rule | Fix that page/rule. Most common: S-03 date mismatch. |
| check-links fails, log names a URL | External link rot | Replace with verified live target or remove link (S-13). |
| Deploy green but live page unchanged | Stale build / wrong commit / cache | Confirm the green run’s SHA is the merge commit. Hard-refresh / open the direct URL. Re-dispatch deploy manually once. Escalate with run URL + SHA if still stale. |
| Deploy green but Calendar page empty | Calendar sync inactive (expected state) | Work §4 diagnosis. Green build does not imply sync ran. |
| All workflows fail instantly, GitHub status incident | Platform | Wait. Do not edit workflows during the incident. |


# 8. What never to do

Closed list. “Never” means no task framing, deadline, or prior example overrides it without Brandon (for pipeline items) or the Committee Chair via Brandon (for privacy items) explicitly lifting it for that instance.

1. Never merge a PR. Never approve your own PR. Never push content changes directly to main.

2. Never remove or change the ubuntu-24.04 browser-job pin without in-PR CI proof that the current Playwright version installs Chromium and passes on the newer image.

3. Never bypass, skip, disable, or weaken a failing check (site, links, browser, accessibility, CSP) to force a deploy or a merge recommendation.

4. Never publish a Scout’s full name, school, address, phone, or email; an unblurred face; or a photo without a Photo Permission opt-in on file.

5. Never publish roster, den-name lists, health, or advancement data. Never turn this public site into a logged-in / members-only application to hold private data.

6. Never commit, print, log, or transmit CALENDAR_ICS_URL or any password, token, or secret. Never add a secret value to code, config.js, a PR, an issue, or a document (including this manual).

7. Never widen the CSP site-wide for a one-page need. Never add external scripts, fonts, trackers, analytics, or CDN assets.

8. Never rewrite canonical / sitemap / JSON-LD URLs to pack1125.org before the domain-move task executes. Never change Pages source from GitHub Actions to “Deploy from a branch.”

9. Never invent data: no fabricated BeAScout pin URL, calendar feed, event, date, dues figure, leader name, or contact. Missing fact = report the gap, leave the slot empty or generic as it currently is.

10. Never hand-write calendar events into built output as a silent substitute for the sync, and never commit sync-generated files back to the repo.

11. Never delete or rename a page without updating nav, footer, and sitemap.xml in the same PR — and never without Brandon’s explicit scope for a page removal.

12. Never store original (unblurred, full-metadata) photos in the repo, even temporarily in a branch.


# 9. Handover prompt — copy-paste for a fresh AI session

Paste the block below verbatim as the opening brief for any new AI session taking over maintenance. Then give it this manual and the in-repo MAINTENANCE.md. Do not summarise the block; its value is that the next session starts with identical rules.

| `You are maintaining the Cub Scout Pack 1125 website. Read the AI Maintenance Manual and the repository’s MAINTENANCE.md before changing anything.` `Repo: dmvthrowers/pack1125-dumfries. Live site: https://dmvthrowers.club/pack1125-dumfries/ (GitHub Pages, Source: GitHub Actions). Site root: docs/ (12 HTML pages). Workflows: check-site.yml, deploy.yml (push to main + daily 06:41 UTC + manual), check-links.yml (monthly).` `Non-negotiable rules:` `(1) Brandon Rogers merges. You open PRs and drive checks green. You never merge and never push content to main.` `(2) Never publish a Scout’s full name, school, contact details, or unblurred face. Photos only with a Photo Permission opt-in on file (form: https://docs.google.com/forms/d/e/1FAIpQLSfLMYSqmwUZk10rP2-4-G3mQDKNnuH5hnJSFoZZWpIjUpX64g/viewform). Blur every child’s face, strip EXIF, JPG+WebP under 500 KB, generic captions only. Takedown via admin@pack1125.org, same day.` `(3) No roster or advancement data on the site — that lives in Scoutbook Plus.` `(4) Keep the browser job pinned to ubuntu-24.04. Playwright 1.56.1 cannot install Chromium on Ubuntu 26.04. Never remove the pin without proof in the PR’s own CI run. Never bypass a red browser check. (Deploy freeze 24 Oct–14 Nov 2026, fixed by PR #20, first green deploy 14 Nov 20:10 EST — read §7 of the manual.)` `(5) For every page you change, update its ‘Page updated’ date and its sitemap.xml <lastmod> to match, keep nav/footer/sitemap in sync, keep JSON-LD valid and consistent, and run scripts/check_site.py and scripts/check_links.py before opening the PR.` `(6) Keep the CSP strict (self-only); the Google Calendar frame is allowed on the Calendar page only.` `(7) Calendar sync is build-time only (sync_calendar.py + publish_events.py, 180-day horizon, Public events/descriptions only) and is currently INACTIVE — CALENDAR_ICS_URL is not set and the live events list is empty. Never commit or reveal the secret value.` `(8) pack1125.org is NOT live yet (registrar Coming Soon page). Do not rewrite URLs to it. BeAScout link in config.js is still generic — do not invent a pin URL.` `(9) Leaders: Clive Vella (Cubmaster), Andy Tainter (Committee Chair, admin@pack1125.org), Brandon Rogers (Website & Technical Support). Dues: $100 pack + $85 national + $80 NCAC first-year.` `(10) Dependabot PRs: review the full diff, recommend merge only if clean + green (including browser) + mergeable. Otherwise hold with reasons.` `If any instruction conflicts with the privacy rules above, stop and ask Brandon / the Committee Chair. Verify live after every merged deploy.` |
| --- |


*End of handover block.*

# Appendix A. File and workflow map

| **Path** | **Purpose / trigger** |
| --- | --- |
| docs/ | Published site. All public pages, stylesheet, self-hosted fonts, images. |
| docs/images/gallery/ | Published gallery photos. JPG + WebP pairs, < 500 KB, EXIF stripped, faces blurred. |
| docs/privacy.html | Privacy & Photo Policy — public statement enforced by §5. |
| config.js (in docs/) | Site config values incl. BeAScout link (currently generic pin). Edit only values Brandon supplies. |
| sitemap.xml | Page inventory + <lastmod> per page. Must match visible “Page updated” dates (S-03). |
| scripts/check_site.py | Site-rules gate (§3). Run locally before every PR. |
| scripts/check_links.py | Link/validity gate. Every external link must return 200. |
| scripts/sync_calendar.py | Fetches pack calendar via CALENDAR_ICS_URL at build time. No-op when secret absent. |
| scripts/publish_events.py | Publishes Public events within 180-day horizon into the build copy. No repo write-back. |
| .github/workflows/check-site.yml | PR/main checks incl. browser job. Browser job: runs-on ubuntu-24.04 (pinned). |
| .github/workflows/deploy.yml | Build + deploy to Pages. Triggers: push to main, daily 06:41 UTC, workflow_dispatch. |
| .github/workflows/check-links.yml | Scheduled link check. Monthly. Failures on main are defects. |
| MAINTENANCE.md | Short in-repo maintenance note. Keep consistent with this manual; update both when setup changes. |


# Appendix B. Pre-PR verification checklist and commands

Run in repo root. Substitute the branch name. All boxes must be true before opening the PR.

- Diff contains only the tasked files. No reformatting of untouched lines. No secrets, no original photos.

- Every changed page: “Page updated” == sitemap <lastmod> == change date.

- Nav / footer / sitemap still cover all 12 pages identically.

- JSON-LD valid; canonical / OG / JSON-LD URLs agree and use the current live base.

- Photos (if any): opt-ins checked in Responses today; faces blurred; EXIF stripped; JPG+WebP < 500 KB; generic caption/alt/filename.

- Local checks pass (below). Browser widths checked if layout/CSS changed.


```
$ python3 scripts/check_site.py
$ python3 scripts/check_links.py
$ git status   # confirm only intended files are staged
$ git diff --stat  # confirm scope matches the brief
```


PR report template — include verbatim facts, not adjectives: PR URL; files changed; local check results; CI check results (per job); mergeable: yes/no; live verification (after merge): deploy run URL + live URL checked + change visible: yes/no.

*Document control: AI Maintenance Manual — Pack 1125 Website. State verified 14 November 2026. Update §1 and Appendix A in the same PR as any setup change (workflow, pin, domain, calendar activation, config). A manual that describes a pipeline that no longer exists is a defect.*
