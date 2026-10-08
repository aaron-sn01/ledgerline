# Ledgerline manual

*Version 2026-10-08 · 54. This manual is updated together with every new version of the app; the version number in **Settings → Backup & export** should match.*

Ledgerline is your personal budget and wealth app. It is one web page (`index.html`) hosted on GitHub Pages, plus a small price updater that runs on GitHub. Your entries never leave your devices except as an encrypted sync file in your own GitHub account.

This manual has two parts. Sections 1 to 11 are step-by-step instructions for you. Section 12 is a technical description for an AI assistant or a developer who works on the app.

## 1. What lives where

Your GitHub repository (`aaron-sn01/ledgerline`) contains:

- `index.html`: the whole app.
- `MANUAL.md`: this manual.
- `fetch_prices.py`: downloads ETF prices from Yahoo Finance.
- `fetch_compositions.py`: downloads what each ETF holds (sectors and countries), once a month.
- `tickers.json`: the list of ETFs the updater fetches.
- `.github/workflows/update-prices.yml`: tells GitHub when to run the two scripts.
- `prices.json` and `compositions.json`: written by the updater. Never edit these by hand.

Your data (entries, plan, holdings, debts, settings) is stored inside the app on each device. If sync is on, an encrypted copy is kept in a private GitHub Gist. The app's code contains **no personal data**: a new device starts empty (with a welcome note) and gets your data when you connect sync or restore a backup. Because the repository is public, nothing personal should ever be written into `index.html` or the other files.

## Installing the app

Ledgerline is a web page that you install like an app, so it opens full screen with its own icon:

- **iPhone**: open the link in **Safari** → tap **Share** (the square with an arrow) → **Add to Home Screen** → **Add**. Open it from the new icon.
- **iPad**: in **Safari**, tap **Share** at the top right → **Add to Home Screen** → **Add**.
- **Mac**: in **Safari** (macOS 14 or later), menu **File → Add to Dock** → **Add**. In **Chrome**: **⋮** → **Cast, save and share** → **Create shortcut…**, tick **Open as window** → **Create**.
- **Windows**: in **Edge**, **⋯** → **Apps** → **Install this site as an app** → **Install**. In **Chrome**: **⋮** → **Cast, save and share** → **Create shortcut…**, tick **Open as window** → **Create**. Then pin it to the taskbar from the Start menu.
- **Android**: in **Chrome**, **⋮** → **Add to Home screen** (or **Install app**).

The installed app keeps its **own data**, separate from the same page in a browser tab. Set it up in the installed app, and use sync or a backup to move data between them. The same steps are under **Settings → Install the app**, which highlights the device you're on.

**Do I need a GitHub account?** Only for sync between your own devices and for the Apple Pay automation. Everything else works without one; your data then simply lives on that one device (move it with **Download backup** and **Restore from backup**).

## 2. Everyday use

1. **Add spending** on the Today page: type a name and amount. Ledgerline suggests a category; tap another one if it's wrong. It learns from every correction.
2. **Import instead of typing**: tap **Import** and choose screenshots or PDF statements (Trade Republic, Sparkasse, flatex, Coinbase). Check the review list, untick what you don't want, then tap **Add selected**.
   - **Trade Republic screenshots**: the transaction list (anything under "Upcoming" is skipped, because it hasn't happened yet; the weekly saveback and round-up entries are counted) or **one opened payment** (useful for a single purchase; its "Benefits" are left out, because Trade Republic pays saveback and round-ups together once a week and the list shows that weekly entry).
   - **Sparkasse screenshots**: the account list, or **one opened payment** ("Umsatzdetails"): name, amount, booking date and reference are read. If it's one of your fixed costs (for example your phone bill from Telefonica, which is O2), it's recognised and skipped, because the plan already counts it.
   - **Duplicates**: an entry that's already in Ledgerline, or that appears in two of the files you import, is unticked with a note saying which entry it matches. Repeated purchases (several €3.00 tickets) are counted separately: each entry can only match one other, payments in the same file never count as duplicates, and different times of day (Apple Pay) mean different payments. If something is unticked wrongly, tick it.
   - **Paste instead of saving**: take a screenshot, tap its thumbnail, then **Done → Copy and Delete**. In Ledgerline tap **Import → Paste screenshot** (if the iPhone asks, tap **Allow Paste**). If the button doesn't work, tap the dashed box next to it and choose **Paste**. On a Mac, ⌘V works while the Import window is open.
3. **Browse days**: the app always opens on the Overview, also when you come back to it after more than 10 minutes (shorter trips to another app keep your place). On Today, use the arrows next to the date to see earlier or later days. New entries go on the day you're looking at.
4. **Monthly review**: opens by itself after a month ends. Correct share counts and your cash total there.
5. **Apple Pay, automatically**: set up the Shortcuts automation once (**Settings → Apple Pay automation**, steps below) and every Apple Pay payment you make at a card terminal (iPhone or Watch held to the reader) arrives in Ledgerline by itself, either for you to confirm or added straight away. Online and in-app Apple Pay isn't included.
6. **Undo**: after deleting something or importing, an **Undo** button appears for a few seconds.
7. **Help**: every box has a **?** next to its title that explains what it shows.
8. **Tour**: **Settings → Backup & export → Take the tour** (or **More → Take the tour** on iPhone) walks through the app in 11 stops, including where to enter your fixed costs and the Apple Pay automation. "Look around first" in the setup wizard runs it on sample data; **Set up my own** clears the sample data and starts the setup.
9. **Setup help for your AI**: on the Manual page and in **Settings → Backup & export**. A text to give ChatGPT, Claude or similar; it guides you through installing, sync and the Apple Pay automation one step at a time, and never asks for your token, passphrase or bank data.
10. **What's new**: after each update, a short note lists the changes once.
11. **Back up**: after each monthly review, go to **Settings → Backup & export → Download backup** and keep the file in iCloud Drive or similar.

### Setting up the Apple Pay automation (iPhone, once)

**You need:** iOS 17 or later, your card in Apple Wallet, and sync working on the iPhone (section 9). The same steps are in the app under **Settings → Apple Pay automation** (type "Apple Pay" in the Settings search box), with buttons to copy the two values you need. Keep that page open while you work in Shortcuts.

**In Ledgerline**

1. Go to **Settings → Apple Pay automation**. Choose **Ask me to confirm** or **Add straight away**.
2. Note the two values there: the **web address** (ending in `/comments`) and the **Authorization** value (starting with `Bearer`). You'll copy each one when needed.

**In the Shortcuts app**

1. Open **Shortcuts** and tap **Automation** in the bar at the bottom (not "Shortcuts"). Tap **+** at the top right (or **New Automation**).
2. A list of triggers appears (Time of Day, Alarm, Email, …). Scroll down and tap **Transaction**, the one with the Wallet icon ("When I tap my card"). If you see actions such as *Open Card*, *Request Payment* or *Send Payment* instead, you're adding an action to a shortcut, not creating an automation: close it and start again from the Automation tab.
3. Under **Card**, select the card(s) you pay with. Leave Merchant and Category as they are. Choose **Run Immediately**; switch off **Notify When Run** if you prefer. Tap **Next**.
4. Tap **New Blank Automation**, then **Add Action**. Search for **Get Contents of URL** and tap it.

   *On newer iOS versions* the automation opens as a shortcut beginning with **"When Any Card is tapped"**, followed by Categories, Merchants and switches for **Automation** (leave on) and **Notify**. That is the right screen. Tap **Any Card** to pick your card if you like, then add the action with the **Search** box at the bottom. There, the payment details are called **Transaction** or **Shortcut Input**; use whichever appears in steps 10 and 11. When finished, tap the back arrow at the top left to save.
5. Tap the blue word **URL** and paste the web address from Ledgerline.
6. Tap the small arrow **›** next to it. Set **Method** to **POST**.
7. Under **Headers**, tap **Add new header**. Key: `Authorization`. Text: paste the Authorization value from Ledgerline.
8. Under **Request Body**, choose **JSON**, tap **Add new field → Text**, and type `body` as the key.
9. In the value box type `ledgerline|` (on the iPhone keyboard the `|` is under **123 → #+=**).
10. In the bar above the keyboard tap **Shortcut Input**. Tap the inserted bubble and choose **Amount**.
11. Type `|`, insert **Shortcut Input** again, tap it and choose **Merchant**. The value now reads `ledgerline|Amount|Merchant`.
12. Tap **Done**.
13. Tap **▶** once. When iOS asks whether the shortcut may connect to **api.github.com**, tap **Allow** (or **Always Allow**). Without this, the automation fails silently when it runs on its own. The test run arrives without an amount; Ledgerline lists it as unreadable and removes it with one tap.

**Online and in-app Apple Pay** don't trigger the automation: iOS only offers it for tapping your iPhone or Watch at a terminal. Add online purchases with quick-add, or let the monthly statement import catch them.

**Test it**: pay for something small with Apple Pay at a shop terminal, then open Ledgerline. A banner shows the payment, or it's already added. Running the automation by hand doesn't work, because without a real payment there's no amount or shop.

**Checking what arrived**: **Check for payments now** in Ledgerline shows the time of the last check, how many payments are waiting, and anything that arrived without an amount (with a sample of what came in). To test only the connection, tap ▶ in the automation: Shortcuts then shows GitHub's answer (a block of text with an `"id"` means it worked; "Bad credentials" or "Not Found" mean the token or address is wrong). A hand-run arrives without an amount, which Ledgerline lists as unreadable; remove it with one tap.

**If nothing arrives**: on the iPhone open **Settings → Apps → Wallet** and turn on **Mobile Data**; check the automation still says **Run Immediately**; use **Check for payments now** in Ledgerline; and if you ever replace your GitHub token, paste the new one into the automation as well. While a payment waits for Ledgerline it sits unencrypted on your sync file (amount and shop only), and it's deleted as soon as it's picked up.

## Sharing Ledgerline with friends and family

Anyone can use Ledgerline through your link (https://aaron-sn01.github.io/ledgerline/). Their data stays on their own devices; nobody sees anyone else's, including you.

1. Send them the link: https://aaron-sn01.github.io/ledgerline/. They install it as described in **Installing the app** above (iPhone, iPad, Mac, Windows, Android).
2. The **setup wizard** opens the first time: name, currency, monthly income, fixed costs, investment plans, cash and savings goal. Every step can be skipped; everything can be changed later in Settings (**Settings → Backup & export → Run the setup again** reopens it).
3. For sync between their own devices and the Apple Pay automation, they need **their own** free GitHub account and token (sections 9 and 2); nobody can use someone else's. Without GitHub everything else works on one device.
4. When you upload a new version, they get it automatically the next time they open the app. Their data is upgraded on first launch, like yours.
5. ETF prices come from your `tickers.json`. If someone holds a fund that isn't listed, add it (section 5) or they enter its price by hand.

### Banks Ledgerline doesn't know yet

The importer has dedicated readers for Trade Republic, Sparkasse, flatex and Coinbase. For any other bank it makes a best effort: every line with a date and an amount is offered in the review, marked "layout not known yet: please check each line". Check direction (spent or received), amount and name before adding. To get a proper reader for a bank, send a sample screenshot or PDF with personal details blacked out to whoever maintains the app; it's added in the next update, for everyone with that bank.

### Privacy and security

- **Stored on the device only**, in the browser's storage. There is no Ledgerline server or account; whoever shared the app can't see anyone's data.
- **Not encrypted on the device itself**; it's protected by the device lock. Add Face ID, Touch ID or a PIN under **Settings → App lock** for extra protection.
- **Sync is optional and end-to-end encrypted** with your passphrase before it reaches your own GitHub account. Lose the passphrase and the sync copy can't be recovered.
- **Imports are read on the device**; files are never uploaded. The reading tools are downloaded once from public code servers (cdnjs, jsDelivr).
- **Prices** come from a public GitHub file and CoinGecko. These requests contain no personal data, but like any web request they reveal your internet address.
- **Apple Pay automation** (optional): amount and shop name wait unencrypted in your own GitHub sync file briefly, then are deleted.
- **Backups are your job**: clearing browser data or removing the home-screen app deletes the data on that device.
- **Trust**: the code is public. Updates come from whoever maintains the app.

The same text is shown in the setup wizard and under **Settings → Backup & export**.

## 3. Updating the app to a new version

1. Download the new `index.html`.
2. In your repository, click **Add file → Upload files**, drop the file in (the name must be exactly `index.html`) and click **Commit changes**.
3. Open the **Actions** tab and wait for **pages build and deployment** to show a green tick (1 to 2 minutes, longer if GitHub is busy).
4. The app notices the new version by itself (when it opens, when you return to it, and every 30 minutes) and shows **New version available → Reload**. If it doesn't, press ⌘R on the Mac, or quit the app fully (⌘Q, or swipe it away on iPhone) and open it again. Never remove the app from the Dock or home screen to update it: that deletes its data on that device.

Your data carries over automatically. New versions upgrade old data on first launch.

To change any other file (for example `tickers.json`): open the file on GitHub, click the **pencil** icon, edit, then **Commit changes**.

## 4. Prices

- ETF prices update every 2 hours on weekdays between 09:23 and 23:23 German time. Nothing updates at night or on weekends because exchanges are closed.
- **Refresh prices** on the Wealth page checks for a newer price file; it can't make GitHub fetch new prices sooner.
- To fetch now: **Actions → Update prices → Run workflow**. A run by hand also refreshes the ETF compositions.
- Ethereum and other crypto prices come live from CoinGecko.
- If a price shows "—": open **Settings → Price updater**, which lists any fund the last run failed for. Check that fund's Yahoo symbol in `tickers.json`.

## 5. Adding a new investment

### An ETF, stock or bond ETF with automatic prices

1. Find its **Yahoo Finance symbol**. For Xetra listings it usually ends in `.DE` (for example `EUNL.DE`). Search the ISIN on finance.yahoo.com to find it.
2. In Ledgerline: **Wealth → Add holding**. Choose **ETF or stock**, then enter the name, ISIN, Yahoo symbol, broker and number of shares. Pick the **asset class** (Stocks, Bonds, Real estate, and so on).
3. On GitHub, edit `tickers.json` and add a line inside the list, separated from the others by a comma:

   ```
   { "symbol": "VAGF.DE", "isin": "IE00BG47KH54", "name": "Vanguard Global Aggregate Bond" }
   ```

4. Run the workflow by hand (section 4) so the price appears straight away.
5. Optional, for the sector and country charts (stocks only): iShares and Xtrackers funds can get automatic compositions. Copy an existing iShares or Xtrackers entry in `tickers.json` and adjust it. Without this, the fund still counts in Asset types but shows as "Not known" in sectors and countries.

### Crypto

**Add holding → Crypto**, then enter the CoinGecko id (the word in the CoinGecko web address, for example `bitcoin`). Prices come automatically.

### Anything without an automatic price (private equity, a pension, a property share)

**Add holding → Other investment** or **Private equity**, and enter the price yourself. Update the price when you get a new statement, or import the statement.

### A new asset class

In the holding dialog, choose **Asset class → + New asset class…** and type a name. It appears as its own slice in Asset types and gets a cautious default return assumption in the projection.

### Savings plans

**Settings → Recurring plan → Investment plans**: add the plan, link it to the holding and set the day of the month. Ledgerline then adds the shares automatically each month.

## 6. Changing your plan and settings

- **Income, fixed costs, annual costs, investment plans**: **Settings → Recurring plan**. A change there applies straight away to the current month and every month after it that's already prepared, item by item; whatever you changed for one month only (Month → Edit this month's plan) stays as it is. Past months never change. Set the real deduction day of each item; the cash outlook and the budget use it. To change one month only, use **Month → Edit this month's plan**.
- **Income paid in advance** (for example a stipend paid on the 29th for the following month): enter the real payment day and tick **Paid in advance**. It counts for the month it's meant for, Ledgerline expects it on that day of the month before, and from the moment it arrives it's kept aside for next month instead of being counted as savings. Imports recognise such a payment as next month's planned income. If the timing changes later, change the item and apply it from that month onward.
- **Savings-rate goal**: **Settings → Savings-rate goal**. Add a goal change from a given month (for example 20% from 03/2027). The switch below it decides whether the cash part of the goal is set aside before your spending budget.
- **Spending categories**: **Settings → Categories**. Add, rename, recolor or delete them. The amount box next to each is an optional monthly limit; leave it empty for none.
- **Fixed-cost groups** (Housing, Insurance and so on): **Settings → Fixed-cost groups**.
- **Month outlook**: "Likely to savings" and the projected savings rate assume your usual day-to-day spending for the rest of the month. One-off big purchases (at least €100 and at least five times your usual purchase, like a yearly ticket) are counted once but not projected onto the remaining days. "Invested" shows what's been invested so far, with the plans still to come listed below it.
- **Wealth over time**: choose 1M, 3M, 6M, 1Y or All. The summary above the chart counts only from the day you started tracking. Anything earlier (the dashed line) is an estimate made from your current holdings at past prices, so it shows how the market moved, not how much you actually had.
- **Language**: English or German, under **Settings → Budget → Language** (also offered on the wizard's first screen). German shows dates as 06.10.2026, decimals with a comma, and can switch numbers to 1.234,56 €. Default names (categories, asset classes, fixed-cost groups) switch language too; names you chose yourself stay as they are. The Manual page shows the German version.
- **Finding a setting**: use the search box or the group buttons (Plan, Money, Investments, Devices, Advanced) at the top of Settings.
- **Settings layout**: Recurring plan spans the full width; the other boxes flow in two columns (one on a phone).
- **Box layout**: tap a box's title to collapse it. **Rearrange boxes** at the bottom of each page lets you drag boxes around. Both are remembered per device.

## 7. Cash and accounts

Ledgerline treats all your accounts as one cash total. A month's budget is kept aside from that total until the month ends; the rest counts as cash savings.

- To correct the total: **Wealth → Cash savings → Update balance**. You can list each account separately and the total adds up by itself. When you add your first account, your existing total is kept as a row "My accounts so far", so nothing is lost; split it into separate accounts whenever you like.
- **Accounts stay current**: money you add to or take from cash savings (interest, spending paid from savings, repayments, sales) is added to the account with the same currency. If you have none in that currency yet, one is created for you (for example "CAD account"), so Each currency shows it as that currency. **Update balance** therefore opens with each account's current balance, and the total, the savings line and **Each currency** always agree. Correct any account there; that becomes its new starting point.
- **Opening a savings account** changes nothing in how Ledgerline works: add it as another account row in **Update balance**. Moving money between your own accounts is never spending; the importer skips such transfers.
- Interest goes in as **Money in → Cash savings**. The importer does this automatically for interest lines.

## Currencies

Everything is shown in your **home currency** (the setup wizard asks for it; change it under **Settings → Budget → Currency**). If you live, earn or invest in more than one currency, tick **I use more than one currency** under it. Then:

- **Entries**: a currency picker sits next to the amount on Today and in the entry editor. A £12.00 purchase is saved as £12.00 and converted at that day's rate; the original amount stays visible in the entry list.
- **Plan**: each income, fixed cost and investment plan can have its own currency (a CHF salary, rent in GBP). The month's budget uses the rate on the payment day; until then today's rate.
- **Accounts**: in **Update balance**, each account gets a currency; the total is converted.
- **Holdings**: each holding has a price currency, taken from the price file (a US-listed fund in USD) or chosen in its dialog. Its value is converted at today's rate, its history at each day's rate.
- **Debts**: choose the debt's currency when adding it. Its card shows amounts in that currency, plus the converted total; repayments are converted at the day's rate.
- **Wealth**: the net worth is converted into your home currency at current ECB rates; below it, as soon as you hold more than one currency, **each currency is listed on its own**, not converted (holdings in their price currency, accounts, debts). The **Currencies** chart under Asset types shows the same money split by currency.
- **Changing the home currency** converts entries at the rate of their own day; plan items, holdings, accounts and debts keep their currency and are converted automatically.
- **Exchange rates** are the ECB's official daily reference rates (about 30 currencies, including USD, GBP, CHF, CAD and SGD), plus the UAE dirham, Saudi and Qatari riyal, Omani rial and Bahraini and Jordanian dinar through their official fixed peg to the US dollar, loaded from frankfurter.app and kept on the device, so the app works offline with the last known rates. **Refresh** under the currency setting loads them again.

With only one currency in use, nothing changes: every number is exactly as before.

## 8. Debt

- **Debt → Add a debt**: enter the amount left, the interest rate (0 for interest-free) and optionally a target date.
- **Repayment plan**: tick "Repay with a fixed monthly instalment" and set the amount and day. It becomes a fixed cost in each month's budget and comes off the balance automatically, after interest.
- One-off repayments: **Record repayment** on the Debt page, from cash savings or from that month's budget.

## 9. Sync between devices

Sync keeps your devices in step through an encrypted file in **your own free GitHub account**. Without it, everything works on one device; with it, phone and laptop show the same data. You set it up once, in about 10 minutes.

**A. Create a GitHub account** (skip if you have one)

1. Go to **github.com/signup**, enter your email, a password and a username, and follow the steps.
2. Confirm your email address with the code or link GitHub sends you.

**B. Create a token** (the key Ledgerline uses to reach your sync file)

1. Signed in to GitHub, open **github.com/settings/tokens/new**. If GitHub asks which kind, choose **Tokens (classic)**.
2. **Note**: type "Ledgerline". **Expiration**: choose **No expiration**.
3. Under the list of permissions, tick **only gist**. Nothing else.
4. Click **Generate token** at the bottom. Copy the token (it starts with `ghp_`) and save it in your password manager: GitHub shows it only once.

**C. Connect your devices**

- **First device**: in Ledgerline, **Settings → Sync between devices**: paste the token, choose a passphrase (at least 8 characters; save it in your password manager, it can't be recovered), leave **Sync ID** empty, and click **Create sync file**. The **Sync ID** then appears in that box with a **Copy** button and stays visible there; it's also the code at the end of the sync file's address on gist.github.com.
- **Every other device**: the same token, **that** Sync ID and the same passphrase, then **Connect**. On a new device, the setup wizard's "I already use Ledgerline on another device" leads straight there.
- All devices must show the **same Sync ID**. If one differs, click **Disconnect this device** there and connect with the right ID; its data is merged in.
- Each person uses their own account and token; never share yours.

## 10. App lock

**Settings → App lock**: Face ID / Touch ID with a PIN as fallback, set separately on each device. The app locks after 2 minutes in the background.

## 11. Troubleshooting

- **Prices look old**: see section 4. A red **Update prices** run in Actions shows the reason when you open it; the next run usually fixes itself.
- **App didn't update after uploading**: check the file is named exactly `index.html`, wait for the green tick on **pages build and deployment**, then reload. If deployments stay "Queued", check githubstatus.com; GitHub may be having problems.
- **"Sync problem, see Settings"**: open **Settings → Sync between devices** for the exact reason. "Slow down" means GitHub's rate limit, which clears on its own. "Refused access" means the token is missing the gist permission.
- **Something looks wrong after an import**: open the entry from the Month page and edit or delete it.
- **Apple Pay payments don't arrive**: see the end of section 2.
- **Demo data** (**Settings → Backup & export → Preview with demo data**): never overwrites your data. It adds sample entries from January to today, marked as demo, and syncs to your other devices like any entry. While it's there, your budget, savings rate and charts include it. **Remove demo data** in the same place deletes exactly those entries and puts your start month, cash total and milestones back (an **Undo** appears for a few seconds). To try it without touching your data at all, use it in a separate browser (for example a Safari tab instead of your home-screen app) with sync not connected.
- **Erase all data in this browser** (Settings → Backup & export) only affects the browser or installed app you press it in; other browsers, other devices, your sync file and backups stay as they are.
- **Start over on a device**: **Settings → Backup & export** to save a backup first, then restore it later with **Restore from backup**.

## 12. For an AI assistant or developer

Read this section before changing anything. The owner is not a programmer: give back complete files that can be uploaded as they are, and explain any GitHub steps one click at a time.

### Constraints

- The app is a single self-contained `index.html`: vanilla JavaScript, no framework, no build step, no package manager. Keep it that way.
- External code is only loaded lazily, when needed, from cdnjs.cloudflare.com or cdn.jsdelivr.net: PDF.js for PDF text and Tesseract.js for screenshot OCR. Everything else is inline.
- Network access is limited to: the GitHub API (encrypted Gist sync), ECB exchange rates from frankfurter.app, `prices.json` and `compositions.json` from the same repository (raw.githubusercontent.com first, then the same origin), CoinGecko for crypto, and the two CDNs. No analytics and no other servers.
- Personal data stays on the device. Imports are parsed locally.
- **The repository is public. Never write personal data into the code** (no names, amounts, holdings or share counts in seed data, defaults or examples). `seedPlan`, `seedHoldings` and `seedDebts` are deliberately empty; a new device is filled by sync or a backup.
- UI text is American English. **Dates are always displayed day/month/year** (05/10/2026), via `fmtDate`, `fmtDateTime` and the date-box enhancer. Never show month/day.

### Code layout of index.html

The file is a sequence of blocks, in this order. Later blocks may use earlier ones; the boot block must stay last.

1. `<head>` and `<style>`: design tokens as CSS variables (light and dark), layout, components, print styles for the PDF summary.
2. Core script: constants and storage keys, formatting helpers (money in integer cents, `fmt`, `fmtDate`), icons, categories and seed data, `defaultState` and `migrate`, the budget engine (`computeMonth`, `aggregate`, weekday model, odds simulation), cash (`cashSavings`, cash outlook), wealth (`wealth`, `wealthSeries`, prices via `Prices`), debt (`debtLedger`, `debtStatus`, `debtPlansFor`), projection (Monte Carlo), diversification, charts (`sankeySVG`, `flowNodes`, and others), sync (`Sync`, AES-GCM with a PBKDF2 key) and app lock (`Lock`, WebAuthn and PIN).
3. UI script: `render()`, one `view…()` function per page, dialogs, the `ACTIONS` map (every button has `data-act="name"`), input binding, collapsible boxes (`decoratePanels`).
4. Importer: `IMP` (pure parsers per document type, plus `IMP.genericPdf` as a best-effort fallback for unknown banks: Trade Republic, Sparkasse, flatex, Coinbase), classification in `buildProposals` (transfers, fixed-cost and plan matching, refunds, duplicates, categories), and the review dialog. Duplicates are found with `align()`, an order-preserving one-to-one pairing of same-amount, similar-name entries within 2 days (and 15 minutes when both have a time); entries from the same file are never paired. Don't replace this with a simple "same amount within a few days" check: it merges repeated purchases.
5. PDF summary: section builders and fit-to-one-page printing.
6. Overview: savings rate and goal, typical month, category trends and limits, Ways to save, net-worth change, the More sheet.
   Extras (after the date boxes and the manual): the Apple Pay inbox (`Inbox`: reads and deletes comments of the form `ledgerline|amount|merchant` on the sync Gist and feeds them through the normal import review), "?" help (`HELP`, one text per box title, plus `HELP_BY_VIEW` for boxes titled with the user's own text; every new box needs an entry), Settings search and groups, `Undo`, nudges, and milestone celebrations. They hook in through `window.AFTER_RENDER`, a list of functions that runs after every render.
7. Arrange mode: drag-and-drop box order (`applyLayout`).
8. Date boxes: replaces native date inputs with day/month/year text boxes.
9. Manual (this text, plus `MANUAL_DE`, the German user manual), extras (see above), the setup wizard (`openWizard`), which opens once on a device without data or sync, and German (`DE`, `DE_BLOCK`, `DE_PAT`, `HELP_DE`). The interface is written in English; with German selected, a translation pass swaps every rendered text: whole formatted paragraphs (`DE_BLOCK`), single texts (`DE`), then sentences with numbers (`DE_PAT`, regular expressions). Untranslated text stays English. **New or changed English text needs a matching German entry**; the source dictionaries are in `i18n/` in the working files (generated into the `DE…` constants).
10. Boot: starts sync, the lock and the first render. It must stay the final script.

### Data model

Stored in localStorage under `ledgerline:data:v2` (UI state under `ledgerline:ui:v2`, collapsed boxes and layout under their own keys). Shape:

- `schema`: version number. Bump it in `defaultState` and add a step in `migrate()` whenever the stored shape changes; old data must keep working.
- `settings`: the recurring plan (`recurring.income`, `bills`, `annual`, `savings`), `categories` (with optional `limit`), `fixedGroups`, `cash` (`amount`, `date`, `mode: 'accounts'`), `cashAccounts`, `savingsGoals`, `goalInBudget`, `assetClasses`, `projection`, sync and price settings.
- `months`: `{ "YYYY-MM": plan }`, a copy of the plan per month so changes to one month don't affect others.
- `transactions`: `{ id: { name, amount, date, type, category, … } }`. `type` is `out` (spending), `in` (money in), `invest` (with `accountId` and `source` budget, bonus or savings), `debt` (with `debtId`), or `sell` (with shares, gross, tax and fees).
- `holdings`: `{ id: { name, isin, symbol, kind, assetClass, broker, base: { shares, date, at }, manualPrice, coingeckoId } }`. Share counts are `base` plus plan executions and transactions after `base.date`.
- `debts`: `{ id: { name, original, rate, plan: { on, amount, day, start }, base: { balance, date }, target } }`.

Currencies (`4m_fx` block): every amount is stored in the home currency (`settings.currency`); an entry in another currency also keeps `cur` and `orig` (original cents). Plan items, holdings (`cur`, else the price file's `currency`, else a guess from the symbol), cash accounts and debts can carry `cur` and are converted when read (`fxPlan`, `quoteOf`/`priceOn` wrappers, `debtTxAmount`, `totalDebt`). Rates: `FX.rate(cur, iso)` (EUR-based, latest published day on or before the date), `fxConv(cents, from, to, iso)`. With no foreign `cur` anywhere, conversion returns its input unchanged; keep it that way. `fetch_prices.py` stores each quote's `currency` (London pence converted to pounds).

Rules: amounts are integers in cents; dates are stored as ISO `YYYY-MM-DD`; every object carries `updatedAt`; deleting sets `deleted: true` (needed for sync, which merges per object, last write wins). Never rename storage keys.

### Price pipeline

GitHub Actions runs `fetch_prices.py` every 2 hours on weekdays, and `fetch_compositions.py` monthly and on manual runs, then commits `prices.json` (quotes plus about 400 days of daily closes) and `compositions.json`. The app shows each file's timestamp. To support a new fund, add it to `tickers.json`.

### Testing a change

1. In the repository folder, run `python3 -m http.server 8765` and open http://localhost:8765/.
2. **Settings → Backup & export → Preview with demo data** fills ten months of entries so every chart has content.
3. Check every page at desktop width and at phone width (390 px), in light and dark mode. Check that no page scrolls sideways and that no date shows month/day.
4. Check that the money-flow diagram balances: everything into "Money in" equals everything out of it.
5. Check that an existing backup still loads (migration).

### Handing back a change

Return the complete updated `index.html`, plus any other changed files, with upload steps. **Every new version adds an entry at the top of `CHANGELOG`** (shown once as "What's new"). **Significant new features also update the tour** (`TOUR_STEPS`, English and German) and, where relevant, the setup help (`SETUP_HELP_EN`, `SETUP_HELP_DE`); small fixes don't. **Every change to the app must come with an updated manual**: edit `MANUAL.md` and the copy embedded in `index.html` (the `MANUAL_MD` constant) together, raise `APP_VERSION` (shown in Settings) and the version line at the top of this manual to the same value. Keep features working that the owner relies on: the importer, the Apple Pay inbox, sync, app lock, the savings-rate goal in the budget, day/month/year dates, and collapsed and arranged boxes.
