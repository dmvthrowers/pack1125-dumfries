**A FREE WEBSITE FOR YOUR GROUP**

**Scout Site Template**

**Setup Guide**

Copy a working scout website. Make it yours. Put it live.

This guide walks you through the whole job. You start with a site that already works. You change the names, the colors, and the photos. You turn it on. That is most of it.

You do not need to hire anyone. You do not need a server. If you can edit a document and click through settings pages, you can do this.

| **The worked example in this guide** | **What it is** |
| --- | --- |
| Pack 1125, Dumfries, Virginia | A real Cub Scout pack site built with this template. It runs live at dmvthrowers.club/pack1125-dumfries and the code sits on GitHub at dmvthrowers/pack1125-dumfries. Where this guide says Pack 1125, read it as an example. Your group will differ in the details. The steps stay the same. |


**Who this is for**

- a Cub Scout pack that needs a first website

- a Scout troop that wants to leave a paid site builder

- any youth group with one willing volunteer and no budget for hosting

How long it takes. Most groups copy the template on a Saturday morning, swap in their own facts that afternoon, and share the link at the next meeting. The domain step can add a day. Web addresses take time to spread across the internet.

| **Read this first.** Work top to bottom the first time. Later you can jump to the one section you need. Keep this guide with your group records. When you hand the site to someone new, hand them this guide too. |
| --- |


# Start here: what you are building

You are building a public website. Think of it as a notice board in a library window. Anyone can read it. So you only pin up things you are happy for anyone to see.

That one idea drives every rule in this guide. Meeting times go on the site. A roster does not. A photo with permission goes on the site. A child's full name next to a photo does not.

Private stuff has a home already. For scout groups that home is Scoutbook Plus. Your website links to it. Your website never copies records out of it.

# 1. What you get

The template is a set of plain web pages. There is no database. There is no login. There is nothing to patch each month. That is the point. A small group site gets read a lot and changed a little. Plain pages fit that job well.

You get 11 pages, ready to rename and rewrite:

| **Page** | **What it does** |
| --- | --- |
| Home | First look. Meeting time, place, and the next few events. |
| About | What your group is and who leads it. |
| Join | Who can join, the steps, and what it costs. |
| Families | Help for new families. First meeting, first month, forms. |
| Dens or groups | One card for each den, patrol, or age group. Packs call this page Dens. |
| Calendar | Your Google Calendar, plus an event list the site can fill in on its own. |
| Gallery | Photos from your events. |
| Resources | Links to your council, Scoutbook Plus, forms, and shops. |
| FAQ | The questions new families ask each fall. |
| Contact | One contact card. One email address. |
| Privacy | Your photo and privacy rules, in plain words, for parents to read. |


You also get safety checks that run on their own. Each time someone suggests a change, a computer reads every page. It looks for broken links, missing picture text, bad dates, and pages that scroll sideways on a phone. A bad change does not go live. The old site stays up.

And you get a paper trail. Each change is saved with a name and a date. If a page breaks, you can step back to the last good copy. Nothing is lost for good.

# 2. What you need before you start

Get these things first. Setup goes twice as fast if you are not hunting for passwords mid job.

**Accounts**

- **GitHub.** A GitHub account for your group. Use a group email address if you can, not one person's home email. GitHub holds the site files and puts them on the web. The free plan is enough.

- **Google Calendar.** A Google account that owns your group calendar. Most packs already have one. If not, make the calendar now and add two or three real events.

- **A contact email.** An email address you can print on the site. A role address works best, like admin@yourgroup.org. It can forward to whoever holds the job that year.

- **A domain name.** Only if you want your own web address. Buy it from any registrar. Buy it in an account your group controls. Write down where you bought it.

**Facts to have on one sheet of paper**

- your group name, number, town, and council or district

- your charter group, if you have one

- meeting day, time, place, and the street address if you show it

- leader names and roles. Ask each leader before you list them.

- dues and fees, in the exact numbers your treasurer uses

- your Scoutbook Plus link and your council link

- two or three good photos, with permission sorted out (see section 9)

| **One person or two?** One person can set this up. Two is better. The second person becomes the backup. Groups lose websites when one volunteer moves away with the only password. Do not be that group. |
| --- |


# 3. Copy the template

The template lives on GitHub as dmvthrowers/pack1125-dumfries. You make your own copy of it. From that moment on, your copy is yours. Changes to the Pack 1125 site do not touch yours, and your changes do not touch theirs.

1.  Sign in to GitHub with your group account.

2.  Open the template page: github.com/dmvthrowers/pack1125-dumfries

3.  Click Use this template, then Create a new repository. If you do not see that button, click Fork instead. Both work. The template button gives you a clean start with no old history. A fork keeps the history, which some groups like.

4.  Name your copy in plain words. Pack 1125 kept its pack number in the name. Your name might be pack-123-springfield or troop-45. Lower case, with hyphens, is the GitHub habit.

5.  Set the copy to Public. This matters. GitHub Pages is free on a public copy. Public means people can read the site files. It does not mean strangers can change them. Only people you add can change them.

6.  Click create and wait a few seconds. You now own a full copy of the site.

Take a quick look around. The folder named docs holds the website. Every file in there can end up on the public web. Files outside docs, like the README, are notes for editors. They do not get published.

| **Keep the license file.** The code in the template is free to reuse. Photos, logos, and scout badges are not. You will swap those out in the next section anyway. |
| --- |


# 4. Make it yours

Do these jobs in order. The first two do most of the work.

## Job 1: Fix the facts in config.js

Open docs/config.js. Near the top you will see a block named CONFIG. It holds the facts the site uses again and again. Work down the block and replace each Pack 1125 fact with yours.

- **Pack.** pack number, name, tagline, town, and the schools or grades you serve

- **Charter.** charter group name and link

- **Council.** council name, short name, and district

- **Leaders.** leader names and roles

- **Meetings.** pack and den meeting pattern, time, place, and address

- **Contact.** contact email, Scoutbook link, and aid links

- **Dues.** dues for the year

- **Activities.** your next few events

- **Calendar.** your calendar ID and link. You will set this in section 7.

Be honest about what you do not know yet. The template marks gaps with a short note in the code. Keep that habit. Write to be announced on the page. Do not guess a date or a price.

One catch. Some facts also sit in the words of the pages. Change config.js first. Then search the pages for the old fact and fix each spot you find. Section 12 lists the pages that repeat facts.

## Job 2: Swap the old web address for yours

Each page names the site home address in a few hidden spots. Search tools call them canonical links and preview tags. Search engines use them. If you skip this job, search engines will point at the wrong site.

Your new home address takes one of two forms:

```
https://YOUR-ACCOUNT.github.io/YOUR-REPO/     (free GitHub address)
https://yourgroup.org/                          (your own domain, see section 8)
```

1.  In your editor, search the whole docs folder for this exact text:

```
https://dmvthrowers.club/pack1125-dumfries/
```

1.  Replace it with your new home address. Keep the slash at the end.

2.  Open docs/404.html. That page uses short paths that start with /pack1125-dumfries/. Replace that bit with your repo name, or with / if you use your own domain.

3.  Open docs/sitemap.xml. It lists each page once, with the same home address. Your search and replace will have fixed it. Give it a quick read to be sure.

4.  Open docs/robots.txt. It points at the sitemap. Fix that line too if your address changed.

If you plan to use your own domain from day one, do section 8 first, then use the domain as your home address here. It saves you doing this job twice.

## Job 3: Rewrite the pages

Now read each page like a new parent would. Change the words to fit your group. Keep the page shapes. Short pages work. A parent on a phone, in a parking lot, wants a time and a place. Give them that first. Put the nice story after.

- Home: meeting time and place up top. Next events under it.

- Join: who can join, three clear steps, dues in real numbers, and a note that help with cost exists if it does.

- FAQ: each answer shows up twice in that file. Once where people read it, and once in a data block at the top for search engines. Change both spots, word for word the same.

- Dens: one card per group. A troop can rename the page to Patrols. If you rename a page, you must add the new name to the menu, the footer, and sitemap.xml on every page. The checker will catch a miss, but save yourself the round trip and do all three at once.

Each page ends with a line that says Page updated, with a date. That date must match the date for the same page in docs/sitemap.xml. When you change a page, set both dates to today. The checker fails the change if they do not match. It sounds fussy. It pays off. A parent can see at a glance if a page is stale, and so can you.

## Job 4: Change the colors

Open docs/style.css. The colors sit at the top, in a block that starts with :root. Each color has a short name.

```
--navy: #003366;    main color, header and headings
--gold: #FFCC00;    bright accent
--red: #CE1126;     small accents only
--forest: #0A4F39;  second accent
--cream: #FFFEF7;   page background
```

Pack 1125 took navy and gold from its own flyer. Take yours from your group scarf, your charter group, or your school colors. Change the codes and save. That one block recolors the whole site. Keep the text dark and the background light. If you cannot read it at arm length on a phone, the colors are too close.

The words use two free fonts, Inter and Montserrat. The font files live in docs/fonts, so the site loads nothing from outside. Leave them alone unless you have a strong reason. New fonts mean new files and new license notes.

## Job 5: Replace the photos and logos

Take out every Pack 1125 picture. The pack badge, the council logo, the charter logo, and the gallery photos belong to that pack. Put yours in the same spots. Pictures live in docs/images. Gallery photos live in docs/images/gallery.

- Save each picture twice, once as .jpg or .png and once as .webp. Pages show them as a pair. The webp copy is smaller and loads fast. Most photo tools can export both.

- Keep each file under 500 KB. The checker blocks big files. A phone photo is often 3 or 4 MB. Shrink it first.

- Give each picture a width, a height, and a short text label in the page code. The template shows you the pattern. The label helps parents who use a screen reader.

- Read section 9 before you touch the gallery. Permission comes first.

No logo yet? Skip it. The header shows your group name in a colored box. That looks fine and it costs you nothing.

# 5. Turn on GitHub Pages

GitHub Pages is the part that puts your files on the web. You turn it on once.

1.  In your repo, open Settings, then Pages in the left menu.

2.  Find Build and deployment. Set Source to GitHub Actions.

3.  Stop there. Do not pick Deploy from a branch. That older setting skips the checks. The Actions setting runs the checks first, every time. A change that fails never reaches the live site.

4.  Make one small change to a page and merge it (section 10 shows you how). Or open the Actions tab, pick Build and deploy, and click Run workflow.

5.  Wait about a minute. Open your free GitHub address. You should see your site.

From now on the site rebuilds on its own in three cases. It rebuilds when you merge a change. It rebuilds each morning, which is how new calendar events show up. And it rebuilds when you click Run workflow by hand.

| **Site will not load?** Give it ten minutes the first time. Still blank? Open the Actions tab. A red run tells you which check failed. See Appendix C. |
| --- |


# 6. Protect the main branch

Your live site comes from one branch named main. Protect it. This takes five minutes and it stops the worst accidents. No one, not even you, will be able to push a change straight to the live site without a check first.

1.  Open Settings, then Rules, then Rulesets. Click New ruleset, then New branch ruleset.

2.  Name it Protect main. Set Enforcement to Active.

3.  Under Target branches, pick Include default branch.

4.  Under Bypass list, add Repository admin. That is your fire exit. The owner can still fix a true emergency.

5.  Turn on Restrict deletions and Block force pushes.

6.  Turn on Require a pull request before merging. Set required approvals to 0 for now. Raise it to 1 when a second person can review changes.

7.  Turn on Require status checks to pass. Add the three checks named check, validate, and browser.

8.  Save the ruleset.

That is the same setup Pack 1125 uses. It feels strict for a week. Then it feels normal, and one day it saves you from posting a half finished page to every parent in the group.

# 7. Add your Google Calendar

You have two choices here. You can show the calendar on the page. And you can let the site list upcoming events on its own. Most groups do the first one on day one and add the second one later.

## Choice A: Show the calendar on the page

The Calendar page holds a frame for your Google Calendar. It stays empty until a visitor clicks a button that says Show the Calendar. The calendar loads only after that click. So Google stays off the page until a person asks for it. The page loads fast, too.

1.  Open Google Calendar. Find your group calendar. Open Settings and sharing for that calendar.

2.  Find Access permissions for events. Tick Make available to public. Pick See all event details. Skip this step and visitors who are signed out will see a Google sign in box, not your events. This is the step groups miss most often.

3.  Find Integrate calendar. Copy the calendar ID. It looks like a long jumble of letters that ends in @group.calendar.google.com.

4.  Put that ID in three spots, all together. One spot is the calendar block in docs/config.js. The other two are in docs/calendar.html, in the data-src value and in the Open in Google Calendar link. Change one and miss the others and the page will point at two calendars at once.

5.  Merge the change. Click Show the Calendar on the live page and check the right events show up. Then test it signed out of Google, or in a private browser window. That is what a new parent sees.

## Choice B: Let the site list events on its own (pick this later if you like)

With this on, the site reads your calendar each morning when it rebuilds. It writes the next events onto the Calendar page, with dates and times. It also makes a file named calendar.ics that parents can save to their own calendars. Visitors never talk to Google. The pull happens behind the scenes. It works even if your calendar stays private.

1.  In Google Calendar, open Settings and sharing, then Integrate calendar. Copy the Secret address in iCal format. Treat it like a password. Do not paste it in a page, an email, or a chat.

2.  In your repo, open Settings, then Secrets and variables, then Actions. Click New repository secret.

3.  Name it CALENDAR_ICS_URL, in capitals, just like that. Paste the secret address as the value. Save it.

4.  You can also set two options on the Variables tab next door. CALENDAR_TZ sets your time zone. It starts as America/New_York, so change it if you live elsewhere. CALENDAR_SHOW_PLACES set to true shows each event place on the page. Leave it blank if you would rather keep places off.

5.  Open the Actions tab. Run Build and deploy once by hand. Then open your Calendar page and check the list looks right.

What the site takes from each event is small on purpose. Title, date, time, and place if you turned places on. Notes stay private. A note shows up only if it starts with the word Public, and then only the text after that word. So a phone number typed in the notes will not leak onto the web. Private events and cancelled events are skipped. Weekly meetings repeat as you would expect.

No secret? No harm done. The build step does nothing and the Calendar page stays just as you wrote it. That also means a fault can hide. Check the live Calendar page once a month with your own eyes. A green check on the build does not prove the events list is fresh.

Two short scripts do this work. scripts/sync_calendar.py reads the feed. scripts/publish_events.py writes the events into the page. You do not need to edit them. Know their names so you can point a helper to them.

# 8. Use your own domain

You do not need your own domain. The free GitHub address works fine. But a short address is easier to print on a flyer and easier to say out loud. Pack 1125 owns pack1125.org for that reason. If you bought a domain, point it at the site like this.

You will touch two places. Your domain registrar, where you bought the name. And your repo settings on GitHub. Do the registrar part first.

## Step 1: Set the records at your registrar

Open the DNS settings for your domain. DNS is the phone book of the web. Add these records. Delete any old records for the same names that point somewhere else. Two answers for one name will break things.

| **Type** | **Name** | **Value** | **What it does** |
| --- | --- | --- | --- |
| A | @ | 185.199.108.153 | Points your bare domain at GitHub Pages. |
| A | @ | 185.199.109.153 | Same job. GitHub uses four addresses. |
| A | @ | 185.199.110.153 | Add all four. |
| A | @ | 185.199.111.153 | Add all four. |
| CNAME | www | YOUR-ACCOUNT.github.io | Points www at GitHub. Use your own account name. Pack 1125 uses dmvthrowers.github.io. |


Those four numbers are the GitHub Pages addresses at the time this guide was written. Check them once against the GitHub Pages help page before you type them in. Numbers can change over the years. Trust the GitHub page over any guide, this one too.

## Step 2: Tell GitHub about the domain

1.  In your repo, open Settings, then Pages.

2.  Under Custom domain, type your bare domain, like yourgroup.org. Save it.

3.  Wait. GitHub checks the records and makes a security certificate for the name. It can take a few minutes. It can take a few hours.

4.  When the certificate is ready, tick Enforce HTTPS. Do not skip this. The padlock matters to parents.

5.  Test both forms on a phone, off your home wifi. Test yourgroup.org and www.yourgroup.org. Both should load your site.

Last job. Your site home address has now changed. Go back to section 4, Job 2, and swap the home address in the pages, the sitemap, and robots.txt to your new domain. Do it in one change so the site never points at two homes at once. Keep the old GitHub address in mind for a school year. Families will have it saved and printed on old flyers.

| **Handle with care.** A wrong DNS record can take your name off the web for hours. Make these changes when you have time to sit with them. Do not start this job ten minutes before a meeting. |
| --- |


# 9. Photos and permission

Read this whole section before you post your first photo. Youth groups get this wrong more than any other part. The fix is simple habits, done each time.

**The hard rules**

- Get written permission from a parent or guardian before you post a photo of a child. No permission on file means no photo. No exceptions for a great shot.

- Never put a child full name with a photo. Never add their school or contact details either. A caption says what happened and when. Fishing day, May. That is enough.

- List an adult leader name or contact detail only if that leader said yes.

- Follow your own council and Scouting America youth protection rules. If those rules say more than this guide, follow those rules.

**How Pack 1125 does it, as one way to copy**

Pack 1125 asks each family to fill in one short form per child. The form gives three choices. Opt in. Opt out. Or ask for a photo to come down. The pack checks the answers before each gallery update. The pack also blurs each child face in gallery photos, and takes removal requests the same day they arrive. You can copy that shape with a Google Form of your own. Link it from your Families page and your Privacy page.

**Before a photo goes up**

1.  Check permission for each child in the shot. One opt out means the whole photo stays off, unless you crop that child out in a way that truly removes them. Cropping is not a trick to get around a no.

2.  Strip the hidden data from the file. Phone photos carry the place they were taken. Most editors call this location or EXIF data. Export a clean copy with that data removed.

3.  Shrink the file under 500 KB. Save a .jpg and a .webp copy.

4.  Put both copies in docs/images/gallery. Add the photo to docs/gallery.html with a short caption. Activity and month only.

5.  Put the change through a pull request, like any other change. Check the live gallery on your phone when it lands.

| **Keep photos out of GitHub issues.** Your repo is public. A photo pasted into an issue or a pull request is public at once, with no checks. Have people email photos to your contact address. You clean them, then you post them. |
| --- |


If a parent asks you to take a photo down, do it that day. Take it down first. Say sorry in plain words. Tell your committee chair. Write down what went wrong so it does not happen again. Speed counts more than a perfect note.

# 10. How changes go live

No change goes straight to the live site. Each change takes the same path. Learn it once and you know the whole system.

1.  Propose the change. GitHub calls this a pull request, or PR for short. You edit files on a copy, then you ask to merge that copy into main.

2.  The checks run. Three jobs read your change. They take a few minutes.

3.  A person reads it. For wording and facts, a second pair of eyes helps. For a one word typo, you may merge your own change if your rules allow it.

4.  Merge it. The site rebuilds and the new page is live in about a minute.

You can edit right in your web browser. Open the file on GitHub. Click the pencil icon. Change the words. Leave the parts in angle brackets alone, those are the page structure. Click Commit changes, pick the choice that makes a new branch and a pull request, and send it in. CONTRIBUTING.md in the repo walks through those clicks, step by step. Keep it open the first few times.

**The three checks**

| **Check** | **What it looks for** |
| --- | --- |
| check | Broken links and picture paths. Missing picture labels and sizes. Missing titles. Pages left out of the menu, footer, or sitemap. Page updated dates that do not match the sitemap. Bad page code. JavaScript faults. It also runs the calendar tests. The main script is scripts/check_site.py. |
| validate | Bad HTML. It uses the same checker that sits behind validator.w3.org. A green run means the page code is sound. |
| browser | Real pages in a real browser. It opens each page at phone width (360 px) and desk width (1280 px). It fails on sideways scroll, on big access problems, on files loaded from outside the site, and on security policy errors. The script is scripts/check_browser.js. |


A fourth check runs once a month, not on each change. It tests the links that point off your site, to your council and to Scouting America. Its script is scripts/check_links.py. Outside sites go down for their own reasons, so a red run there is a to do list, not an emergency. Fix or remove the dead link when you can.

Run two checks yourself before you send a change, if you work on your own computer:

```
python3 scripts/check_site.py
for f in docs/*.js; do node --check "$f"; done
```

Look at your pages before you send them, too:

```
cd docs && python3 -m http.server 8000
Then open http://localhost:8000 in your browser.
```

| **Do not remove the browser job pin.** Open .github/workflows/check-site.yml and you will see the browser job set to run on ubuntu-24.04. Leave that line alone. Here is why. The browser tool in this template cannot set up on the newer Ubuntu image that GitHub now hands out by default. Pack 1125 learned this the hard way. In the fall of 2026 its site froze for weeks. Each build failed in seconds, before a single page got tested, and the live site stopped updating. Pinning the browser job to ubuntu-24.04 fixed it at once. Only move that pin after you have proof, on a test change, that the browser tool works on the new image. A green test run is proof. A hunch is not. |
| --- |


One topic per pull request. A date fix and a photo update in one request take longer to review and are harder to undo. Small requests get merged fast.

# 11. What it costs

Short answer. Nothing, plus your domain if you buy one.

| **Item** | **Cost** | **Notes** |
| --- | --- | --- |
| Hosting on GitHub Pages | $0 | Free while your repo is public. No traffic bill at group scale. |
| Site software | $0 | Plain pages. No site builder fee. No add ons to renew. |
| Calendar and photo form | $0 | Google Calendar and Google Forms on a free Google account. |
| Your own domain | Renewal once a year | Price depends on the name and the shop you buy it from. Check the renewal price before you buy, not just the first year price. This is the one bill that can lapse. Put the renewal date in your group calendar. |
| Your time | An hour here and there | A date change takes minutes. A gallery update takes a bit longer. |


That low cost is a choice, not luck. The moment you add a paid builder, a database, or a login system, you add bills and upkeep. This template says no to those things on purpose.

# 12. The jobs you will actually do

After setup, almost all the work is one of five small jobs.

| **Job** | **Where you do it** |
| --- | --- |
| Change an event | Change it in Google Calendar. Do not ask for a site edit. The site picks it up at the next build. Check the live Calendar page in meeting week. Rooms change. |
| Fix a date, time, or price | Edit the page that shows it, plus docs/config.js. Search for the old text. The same fact often shows on Home, Join, Calendar, FAQ, and Contact. |
| Change a leader | Edit docs/about.html and docs/contact.html. Get the person OK first. |
| Add photos | Follow section 9. Permission, clean file, gallery page. |
| Fix a dead outside link | Run the outside link check, or wait for the monthly run. Link to the real council or Scouting America page. Do not link to a copy of a form that someone saved elsewhere. Families need the current form. |


Each fall, give the site one hour. Check leader names. Check dues. Check meeting day and place with your school. Send the photo permission form out again. Run the outside link check. Open each page on your phone. That hour saves you a dozen small fixes in the busy weeks that follow.

# 13. Hand it over

Volunteers move on. Kids age out. Plan for that on day one, not in a rush in your last month. Hand over these six things, in this order. Sit with the next person while you do it, in the room or on a call.

1.  **Keys.** Repo access. Add the new person as a collaborator with write access. Watch them sign in and open the Actions tab and the Pages settings. If your group is leaving the account that owns the repo, move the repo to the group account.

2.  **Proof it works.** Show them one full change, start to finish. A pull request, green checks, a merge, and the live page updating. Once they have seen it, they can do it.

3.  **Domain.** Give them domain access, or a dated plan to move the domain to an account the group controls. A domain held in a past volunteer personal account is the loss that hurts most.

4.  **Calendar.** Share the group calendar with them, or pass them ownership. If you use the secret calendar feed from section 7, show them where the CALENDAR_ICS_URL secret lives. If that address ever gets reset, the secret needs a fresh value. Never write the value in a doc or an email.

5.  **Photo form.** Share or pass them the photo permission form and its answers. Show them the list of opt outs. That list is part of the job.

6.  **Contact email.** Point your contact email at the new lead or the committee chair. Send a test mail and see it arrive. Update the leader names on About and Contact.

Then tidy up. Once the new person can publish on their own, cut the old person access down or remove it, by agreement. Tell your committee chair the handover is done, with the date. Write that date in your group records.

Give the new person this guide and the MAINTENANCE.md file in the repo. That file is the short, site own version of these notes. If you changed how your site works, change that file too. A handover note that is wrong is worse than no note at all. The next person will trust it.

# Appendix A: File map

| **Path** | **What it is** |
| --- | --- |
| docs/ | The website. If a file sits in here, treat it as public. |
| docs/config.js | Group facts in one block, plus the mobile menu and the calendar button code. |
| docs/style.css | How the site looks. Colors sit at the top. |
| docs/*.html | One file per page. Each page repeats the same header, menu, and footer. |
| docs/images/gallery/ | Gallery photos. A .jpg and a .webp for each shot. |
| docs/fonts/ | Font files. The site loads no fonts from outside. |
| docs/sitemap.xml | List of pages for search engines, with one date per page. |
| scripts/check_site.py | Main checker. Links, pictures, dates, menu, sitemap, safety rules. |
| scripts/check_links.py | Outside link checker. Runs once a month. |
| scripts/sync_calendar.py | Reads the calendar feed. Works with publish_events.py. |
| scripts/publish_events.py | Writes calendar events onto the Calendar page at build time. |
| scripts/check_browser.js | Browser checker. Phone and desk widths. |
| .github/workflows/ | Three jobs that run on their own. Check site, Build and deploy, and Check outside links. |
| README.md | Full notes on the template. Read it when this guide feels too short. |
| CONTRIBUTING.md | How to suggest a change, click by click. |
| MAINTENANCE.md | Short upkeep and handover notes for your own site. Keep yours current. |


# Appendix B: First week checklist

Tick these off and the site is truly yours.

- ☐  Repo copied to your group account, set to Public.

- ☐  CONFIG block in docs/config.js holds your facts, not Pack 1125 facts.

- ☐  Old home address swapped for yours in docs, sitemap.xml, robots.txt, and 404.html.

- ☐  Each page read once and rewritten in your group words.

- ☐  Page updated dates and sitemap dates match, page by page.

- ☐  Colors set in docs/style.css. Text is easy to read on a phone.

- ☐  Pack 1125 photos and logos out. Your photos in, with permission on file.

- ☐  GitHub Pages source set to GitHub Actions. Site loads at the free GitHub address.

- ☐  Protect main ruleset on. Three checks required: check, validate, browser.

- ☐  Calendar shared as public. Show the Calendar tested while signed out.

- ☐  If you use it: CALENDAR_ICS_URL secret set, and one hand run of Build and deploy done.

- ☐  If you use it: domain records set, custom domain saved, HTTPS on, both forms tested on a phone.

- ☐  Second person added as collaborator. They have watched one change go live.

- ☐  This guide and your passwords stored with your group records, not just in your head.

# Appendix C: If something breaks

First, breathe. A failed build does not take your site down. GitHub Pages keeps showing the last good copy. Your site may be a day stale. It is not gone. Tell families urgent news by email or your usual channel and fix the site after.

1.  Open the repo Actions tab. Open the newest run that failed.

2.  Note which job failed. Check, validate, or browser. Or the deploy step itself.

3.  Read the log for that job before you change a thing. The log names the page and the rule in most cases.

4.  Common fix one. A date mismatch. You changed a page but not its sitemap date. Set both to today.

5.  Common fix two. A dead outside link. Swap it for the live council or Scouting America page, or take the link out.

6.  Common fix three. The browser job dies in seconds, before it tests a page. Check the ubuntu-24.04 pin in .github/workflows/check-site.yml. See the note in section 10. Do not guess past this one.

7.  Fix the cause, send it as a pull request, and watch the run go green. Then open the live page and see your change there.

8.  Write down what broke and what fixed it, in MAINTENANCE.md or in a repo issue. The next person will hit the same wall if you do not.

If GitHub itself is down, wait. Do not rebuild your site in a panic during a fault that is not yours. Check again in an hour.

# Appendix D: Words in this guide

| **Word** | **What it means here** |
| --- | --- |
| Repo (repository) | The folder on GitHub that holds your site files and every old copy of them. |
| Branch | A side copy where you draft a change. Main is the live branch. |
| Pull request (PR) | A request to merge a draft change into main. Checks and a review happen here. |
| Merge | To accept a change into main. The site rebuilds right after. |
| GitHub Pages | The free GitHub service that puts your docs folder on the web. |
| GitHub Actions | The part of GitHub that runs your checks and builds on its own. |
| Secret | A value stored in repo settings that no one can read back. Used here for the calendar feed address. |
| DNS record | A phone book entry for your domain. A records point at a server. A CNAME points at another name. |
| Static site | Pages that are the same for each visitor. No server code, no database. |
| Sitemap | A list of your pages for search engines, with a date for each page. |


*That is the whole job. Copy the site. Make it yours. Keep the permission rule. Leave the checks on. Pass it on with care when your turn ends.*
