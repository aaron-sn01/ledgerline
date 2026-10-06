# Ledgerline manual

*Version 2026-10-06 · 19. This manual is updated together with every new version of the app; the version number in **Settings → Backup & export** should match.*

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

## 2. Everyday use

1. **Add spending** on the Today page: type a name and amount. Ledgerline suggests a category; tap another one if it's wrong. It learns from every correction.
2. **Import instead of typing**: tap **Import** and choose screenshots or PDF statements (Trade Republic, Sparkasse, flatex, Coinbase). Check the review list, untick what you don't want, then tap **Add selected**.
   - **Duplicates**: an entry that's already in Ledgerline, or that appears in two of the files you import, is unticked with a note saying which entry it matches. Repeated purchases (several €3.00 tickets) are counted separately: each entry can only match one other, payments in the same file never count as duplicates, and different times of day (Apple Pay) mean different payments. If something is unticked wrongly, tick it.
   - **Paste instead of saving**: take a screenshot, tap its thumbnail, then **Done → Copy and Delete**. In Ledgerline tap **Import → Paste screenshot** (if the iPhone asks, tap **Allow Paste**). If the button doesn't work, tap the dashed box next to it and choose **Paste**. On a Mac, ⌘V works while the Import window is open.
3. **Browse days**: the app always opens on the Overview. On Today, use the arrows next to the date to see earlier or later days. New entries go on the day you're looking at.
4. **Monthly review**: opens by itself after a month ends. Correct share counts and your cash total there.
5. **Apple Pay, automatically**: set up the Shortcuts automation once (**Settings → Apple Pay automation**, steps below) and every Apple Pay payment arrives in Ledgerline by itself, either for you to confirm or added straight away.
6. **Undo**: after deleting something or importing, an **Undo** button appears for a few seconds.
7. **Help**: the **?** next to a box title explains what that box means.
8. **Back up**: after each monthly review, go to **Settings → Backup & export → Download backup** and keep the file in iCloud Drive or similar.

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

**Test it**: pay for something small with Apple Pay, then open Ledgerline. A banner shows the payment, or it's already added. Running the automation by hand doesn't work, because without a real payment there's no amount or shop.

**If nothing arrives**: on the iPhone open **Settings → Apps → Wallet** and turn on **Mobile Data**; check the automation still says **Run Immediately**; use **Check for payments now** in Ledgerline; and if you ever replace your GitHub token, paste the new one into the automation as well. While a payment waits for Ledgerline it sits unencrypted on your sync file (amount and shop only), and it's deleted as soon as it's picked up.

## 3. Updating the app to a new version

1. Download the new `index.html`.
2. In your repository, click **Add file → Upload files**, drop the file in (the name must be exactly `index.html`) and click **Commit changes**.
3. Open the **Actions** tab and wait for **pages build and deployment** to show a green tick (1 to 2 minutes, longer if GitHub is busy).
4. Close the app fully and open it again. On a Mac, ⌘R reloads.

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

- **Income, fixed costs, annual costs, investment plans**: **Settings → Recurring plan**. Set the real deduction day of each item; the cash outlook and the budget use it. To change one month only, use **Month → Edit this month's plan**.
- **Savings-rate goal**: **Settings → Savings-rate goal**. Add a goal change from a given month (for example 20% from 03/2027). The switch below it decides whether the cash part of the goal is set aside before your spending budget.
- **Spending categories**: **Settings → Categories**. Add, rename, recolor or delete them. The amount box next to each is an optional monthly limit; leave it empty for none.
- **Fixed-cost groups** (Housing, Insurance and so on): **Settings → Fixed-cost groups**.
- **Finding a setting**: use the search box or the group buttons (Plan, Money, Investments, Devices, Advanced) at the top of Settings.
- **Settings layout**: Recurring plan spans the full width; the other boxes flow in two columns (one on a phone).
- **Box layout**: tap a box's title to collapse it. **Rearrange boxes** at the bottom of each page lets you drag boxes around. Both are remembered per device.

## 7. Cash and accounts

Ledgerline treats all your accounts as one cash total. A month's budget is kept aside from that total until the month ends; the rest counts as cash savings.

- To correct the total: **Wealth → Cash savings → Update balance**. You can list each account separately and the total adds up by itself.
- **Opening a savings account** changes nothing in how Ledgerline works: add it as another account row in **Update balance**. Moving money between your own accounts is never spending; the importer skips such transfers.
- Interest goes in as **Money in → Cash savings**. The importer does this automatically for interest lines.

## 8. Debt

- **Debt → Add a debt**: enter the amount left, the interest rate (0 for interest-free) and optionally a target date.
- **Repayment plan**: tick "Repay with a fixed monthly instalment" and set the amount and day. It becomes a fixed cost in each month's budget and comes off the balance automatically, after interest.
- One-off repayments: **Record repayment** on the Debt page, from cash savings or from that month's budget.

## 9. Sync between devices

- **Only the first device** creates the sync file: leave Sync ID empty, enter your GitHub token and a passphrase, and click **Create sync file**.
- **Every other device**: enter the same token, **that** Sync ID and the same passphrase, then click **Connect**.
- All devices must show the **same Sync ID**. If one differs, click **Disconnect this device** there and connect with the right ID; its data is merged in.
- Keep the token, Sync ID and passphrase in your password manager. The passphrase cannot be recovered.
- The token is a classic GitHub token with only the **gist** permission.

## 10. App lock

**Settings → App lock**: Face ID / Touch ID with a PIN as fallback, set separately on each device. The app locks after 2 minutes in the background.

## 11. Troubleshooting

- **Prices look old**: see section 4. A red **Update prices** run in Actions shows the reason when you open it; the next run usually fixes itself.
- **App didn't update after uploading**: check the file is named exactly `index.html`, wait for the green tick on **pages build and deployment**, then reload. If deployments stay "Queued", check githubstatus.com; GitHub may be having problems.
- **"Sync problem, see Settings"**: open **Settings → Sync between devices** for the exact reason. "Slow down" means GitHub's rate limit, which clears on its own. "Refused access" means the token is missing the gist permission.
- **Something looks wrong after an import**: open the entry from the Month page and edit or delete it.
- **Apple Pay payments don't arrive**: see the end of section 2.
- **Start over on a device**: **Settings → Backup & export** to save a backup first, then restore it later with **Restore from backup**.

## 12. For an AI assistant or developer

Read this section before changing anything. The owner is not a programmer: give back complete files that can be uploaded as they are, and explain any GitHub steps one click at a time.

### Constraints

- The app is a single self-contained `index.html`: vanilla JavaScript, no framework, no build step, no package manager. Keep it that way.
- External code is only loaded lazily, when needed, from cdnjs.cloudflare.com or cdn.jsdelivr.net: PDF.js for PDF text and Tesseract.js for screenshot OCR. Everything else is inline.
- Network access is limited to: the GitHub API (encrypted Gist sync), `prices.json` and `compositions.json` from the same repository (raw.githubusercontent.com first, then the same origin), CoinGecko for crypto, and the two CDNs. No analytics and no other servers.
- Personal data stays on the device. Imports are parsed locally.
- **The repository is public. Never write personal data into the code** (no names, amounts, holdings or share counts in seed data, defaults or examples). `seedPlan`, `seedHoldings` and `seedDebts` are deliberately empty; a new device is filled by sync or a backup.
- UI text is American English. **Dates are always displayed day/month/year** (05/10/2026), via `fmtDate`, `fmtDateTime` and the date-box enhancer. Never show month/day.

### Code layout of index.html

The file is a sequence of blocks, in this order. Later blocks may use earlier ones; the boot block must stay last.

1. `<head>` and `<style>`: design tokens as CSS variables (light and dark), layout, components, print styles for the PDF summary.
2. Core script: constants and storage keys, formatting helpers (money in integer cents, `fmt`, `fmtDate`), icons, categories and seed data, `defaultState` and `migrate`, the budget engine (`computeMonth`, `aggregate`, weekday model, odds simulation), cash (`cashSavings`, cash outlook), wealth (`wealth`, `wealthSeries`, prices via `Prices`), debt (`debtLedger`, `debtStatus`, `debtPlansFor`), projection (Monte Carlo), diversification, charts (`sankeySVG`, `flowNodes`, and others), sync (`Sync`, AES-GCM with a PBKDF2 key) and app lock (`Lock`, WebAuthn and PIN).
3. UI script: `render()`, one `view…()` function per page, dialogs, the `ACTIONS` map (every button has `data-act="name"`), input binding, collapsible boxes (`decoratePanels`).
4. Importer: `ImportCore.parse` (pure parsers per document type: Trade Republic, Sparkasse, flatex, Coinbase), classification in `buildProposals` (transfers, fixed-cost and plan matching, refunds, duplicates, categories), and the review dialog. Duplicates are found with `align()`, an order-preserving one-to-one pairing of same-amount, similar-name entries within 2 days (and 15 minutes when both have a time); entries from the same file are never paired. Don't replace this with a simple "same amount within a few days" check: it merges repeated purchases.
5. PDF summary: section builders and fit-to-one-page printing.
6. Overview: savings rate and goal, typical month, category trends and limits, Ways to save, net-worth change, the More sheet.
   Extras (after the date boxes and the manual): the Apple Pay inbox (`Inbox`: reads and deletes comments of the form `ledgerline|amount|merchant` on the sync Gist and feeds them through the normal import review), "?" help (`HELP`), Settings search and groups, `Undo`, nudges, and milestone celebrations. They hook in through `window.AFTER_RENDER`, a list of functions that runs after every render.
7. Arrange mode: drag-and-drop box order (`applyLayout`).
8. Date boxes: replaces native date inputs with day/month/year text boxes.
9. Manual (this text) and extras (see above).
10. Boot: starts sync, the lock and the first render. It must stay the final script.

### Data model

Stored in localStorage under `ledgerline:data:v2` (UI state under `ledgerline:ui:v2`, collapsed boxes and layout under their own keys). Shape:

- `schema`: version number. Bump it in `defaultState` and add a step in `migrate()` whenever the stored shape changes; old data must keep working.
- `settings`: the recurring plan (`recurring.income`, `bills`, `annual`, `savings`), `categories` (with optional `limit`), `fixedGroups`, `cash` (`amount`, `date`, `mode: 'accounts'`), `cashAccounts`, `savingsGoals`, `goalInBudget`, `assetClasses`, `projection`, sync and price settings.
- `months`: `{ "YYYY-MM": plan }`, a copy of the plan per month so changes to one month don't affect others.
- `transactions`: `{ id: { name, amount, date, type, category, … } }`. `type` is `out` (spending), `in` (money in), `invest` (with `accountId` and `source` budget, bonus or savings), `debt` (with `debtId`), or `sell` (with shares, gross, tax and fees).
- `holdings`: `{ id: { name, isin, symbol, kind, assetClass, broker, base: { shares, date, at }, manualPrice, coingeckoId } }`. Share counts are `base` plus plan executions and transactions after `base.date`.
- `debts`: `{ id: { name, original, rate, plan: { on, amount, day, start }, base: { balance, date }, target } }`.

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

Return the complete updated `index.html`, plus any other changed files, with upload steps. **Every change to the app must come with an updated manual**: edit `MANUAL.md` and the copy embedded in `index.html` (the `MANUAL_MD` constant) together, raise `APP_VERSION` (shown in Settings) and the version line at the top of this manual to the same value. Keep features working that the owner relies on: the importer, the Apple Pay inbox, sync, app lock, the savings-rate goal in the budget, day/month/year dates, and collapsed and arranged boxes.
