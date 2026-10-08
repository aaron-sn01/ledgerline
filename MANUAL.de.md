# Ledgerline-Anleitung

*Version 2026-10-08 · 82. Diese Anleitung wird mit jeder neuen Version der App aktualisiert; die Versionsnummer unter **Einstellungen → Backup & Export** sollte übereinstimmen.*

Ledgerline ist eine persönliche Budget- und Vermögens-App. Sie besteht aus einer einzigen Webseite (`index.html`) auf GitHub Pages und einem kleinen Kurs-Updater, der auf GitHub läuft. Deine Einträge verlassen deine Geräte nie, außer als verschlüsselte Sync-Datei in deinem eigenen GitHub-Konto.

Die Abschnitte 1 bis 11 sind Schritt-für-Schritt-Anleitungen. Abschnitt 12 ist eine technische Beschreibung für KI-Assistenten und Entwickler und bleibt auf Englisch.

## 1. Was wo liegt

Das GitHub-Repository der App enthält:

- `index.html`: die ganze App.
- `MANUAL.md`: diese Anleitung (auf Englisch; die deutsche Fassung ist in die App eingebaut).
- `fetch_prices.py`: lädt ETF-Kurse von Yahoo Finance.
- `fetch_compositions.py`: lädt einmal im Monat, was jeder ETF enthält (Sektoren und Länder).
- `tickers.json`: die Liste der ETFs, deren Kurse geladen werden.
- `.github/workflows/update-prices.yml`: legt fest, wann GitHub die beiden Skripte ausführt.
- `prices.json` und `compositions.json`: schreibt der Updater. Nie von Hand bearbeiten.

Deine Daten (Einträge, Plan, Positionen, Schulden, Einstellungen) liegen in der App auf jedem Gerät. Mit Sync liegt eine verschlüsselte Kopie in einem privaten GitHub-Gist. Der Code der App enthält **keine persönlichen Daten**: Ein neues Gerät startet leer und bekommt deine Daten, sobald du Sync verbindest oder ein Backup wiederherstellst.

## Die App installieren

Ledgerline ist eine Webseite, die du wie eine App installierst; sie öffnet sich dann im Vollbild mit eigenem Symbol:

- **iPhone**: Link in **Safari** öffnen → auf **Teilen** tippen (das Quadrat mit Pfeil) → **Zum Home-Bildschirm** → **Hinzufügen**. Über das neue Symbol öffnen.
- **iPad**: in **Safari** oben rechts auf **Teilen** → **Zum Home-Bildschirm** → **Hinzufügen**.
- **Mac**: in **Safari** (ab macOS 14) Menü **Ablage → Zum Dock hinzufügen** → **Hinzufügen**. In **Chrome**: **⋮** → **Streamen, speichern und teilen** → **Verknüpfung erstellen …**, **Als Fenster öffnen** anhaken → **Erstellen**.
- **Windows**: in **Edge** **⋯** → **Apps** → **Diese Website als App installieren** → **Installieren**. In **Chrome**: **⋮** → **Streamen, speichern und teilen** → **Verknüpfung erstellen …**, **Als Fenster öffnen** anhaken → **Erstellen**. Danach im Startmenü an die Taskleiste anheften.
- **Android**: in **Chrome** **⋮** → **Zum Startbildschirm hinzufügen** (oder **App installieren**).

Die installierte App hat ihre **eigenen Daten**, getrennt von derselben Seite in einem Browser-Tab. Richte sie in der installierten App ein und nutze Sync oder ein Backup, um Daten zu übertragen. Dieselben Schritte stehen unter **Einstellungen → App installieren**, wo dein aktuelles Gerät hervorgehoben ist.

**Brauche ich ein GitHub-Konto?** Nur für Sync zwischen deinen eigenen Geräten und für die Apple-Pay-Automation. Alles andere funktioniert ohne; deine Daten liegen dann einfach auf diesem einen Gerät (übertragen mit **Backup herunterladen** und **Aus Backup wiederherstellen**).

## 2. Alltag

1. **Ausgaben erfassen** auf der Seite Heute: Name und Betrag eingeben. Ledgerline schlägt eine Kategorie vor (es kennt gängige Läden und Dienste in Deutschland, Österreich, Großbritannien, den VAE, Oman, Singapur und Kanada); tippe auf eine andere, wenn sie nicht passt. Es lernt aus jeder Korrektur.
2. **Importieren statt tippen**: Tippe auf **Importieren** und wähle Screenshots oder PDF-Auszüge (Trade Republic, Scalable Capital, Sparkasse, comdirect, Wise, Finanzguru, flatex, Coinbase). Prüfe die Liste, entferne Häkchen bei allem, was du nicht willst, und tippe auf **Ausgewählte hinzufügen**.
   - **Trade-Republic-Screenshots**: die Umsatzliste (alles unter „Anstehend“ wird übersprungen, weil es noch nicht passiert ist; die wöchentlichen Saveback- und Aufrundungs-Einträge zählen) oder **eine geöffnete Zahlung** (praktisch für einen einzelnen Kauf; ihre „Vorteile“ bleiben außen vor, weil Trade Republic Saveback und Aufrundungen einmal pro Woche gesammelt zahlt und die Liste diesen Wocheneintrag zeigt).
   - **Sparkasse-Screenshots**: die Umsatzliste oder **eine geöffnete Zahlung** („Umsatzdetails“): Name, Betrag, Buchungsdatum und Verwendungszweck werden gelesen. Ist es eine deiner Fixkosten (etwa die Handyrechnung von Telefonica, also O2), wird sie erkannt und übersprungen, weil der Plan sie schon zählt.
   - **Scalable-Capital-Screenshots**: einen Fonds öffnen („Ihre Position“) für die genauen Anteile; den Tagesgeld-Bildschirm („Guthaben“) für den Stand; die Portfolio-Übersicht aktualisiert Fonds, die du schon hast, über ihren Wert (sie zeigt keine Anteile; für neue Fonds den Fonds-Bildschirm nutzen).
   - **Weitere Bildschirme**: Umsatzlisten von Scalable (Sparplan-Käufe zu einem Plan in Ledgerline werden erkannt und übersprungen, mit den gekauften Anteilen; Käufe aus einem Plan, den Ledgerline noch nicht kennt, erscheinen ohne Häkchen zum Hinzufügen, und nach zwei Monaten mit demselben Kauf schlägt die Übersicht vor, den Plan anzulegen; Ein- und Auszahlungen sind Überträge; Zinsen und Ausschüttungen werden gezählt), comdirect-Umsätze und die comdirect-Kontoübersicht (Stände, abgeglichen mit „Gesamt“), der Sparkasse-Startbildschirm der **Wise**-Startbildschirm (Wochentage wie „Dienstag“ werden zum letzten solchen Datum; Aufladungen zählen als Überträge) und **Finanzguru** („Alle Buchungen“; die Kategorie wird für Namen genutzt, die Ledgerline noch nicht kennt). Finanzguru sammelt schon die Zahlungen deiner verbundenen Banken; importiere für denselben Zeitraum also entweder Finanzguru oder diese Banken. Ledgerline entfernt erkannte Doppelte und zeigt einen Hinweis, wenn du beides kombinierst.
   - **Dunkelmodus**-Screenshots funktionieren so gut wie helle. Geldeingänge werden zusätzlich an ihrer Farbe erkannt (grün oder türkis), damit ein übersehenes Minuszeichen keine Ausgabe zur Einnahme macht. Unklares (ein unlesbarer Betrag oder ein unlesbares Datum) wird in der Prüfung markiert.
   - **Fonds über den Namen zuordnen** (Screenshots enthalten keine ISIN): Ledgerline vergleicht die Wörter, die Fonds unterscheiden, und ignoriert Anbieter- und Anteilsklassen-Wörter (Core, UCITS ETF, Acc, EUR …); Abkürzungen wie EM oder WLD werden verstanden. Eine grobe Übereinstimmung reicht („Core Stoxx Europe 600 EUR (A…“ = Amundi Core Stoxx Europe 600), aber verschiedene Indizes bleiben getrennt (MSCI World ≠ Emerging Markets ≠ World Information Technology), ebenso derselbe Index von zwei Anbietern. Passt keine Position, wähle sie in der Prüfung selbst.
   - **Kontostände**: Ein Stand im Screenshot (Sparkasse „Kontostand am“, Scalable „Guthaben“) erscheint in der Prüfung unter **Kontostände**; mit Häkchen wird er als Stand dieses Kontos gespeichert (Ersparnisse → Saldo aktualisieren).
   - **Doppelte Einträge**: Was schon in Ledgerline ist oder in zwei importierten Dateien vorkommt, wird mit einem Hinweis abgewählt. Wiederholte Käufe (mehrere Fahrscheine zu 3,00 €) zählen einzeln: Jeder Eintrag kann nur zu einem anderen passen, Zahlungen aus derselben Datei gelten nie als doppelt, und unterschiedliche Uhrzeiten (Apple Pay) bedeuten unterschiedliche Zahlungen. Ist etwas zu Unrecht abgewählt, setz das Häkchen.
   - **Einfügen statt speichern**: Screenshot machen, auf die Vorschau tippen, dann **Fertig → Kopieren und löschen**. In Ledgerline auf **Importieren → Screenshot einfügen** tippen (falls das iPhone fragt: **Einfügen erlauben**). Klappt die Taste nicht, tippe in das gestrichelte Feld daneben und wähle **Einfügen**. Auf dem Mac funktioniert ⌘V, solange das Importfenster offen ist.
3. **Tage durchblättern**: Die App öffnet immer mit der Übersicht, auch wenn du nach mehr als 10 Minuten zurückkehrst (kürzere Abstecher in eine andere App behalten deine Stelle). Auf der Seite Heute blätterst du mit den Pfeilen neben dem Datum zu früheren oder späteren Tagen. Neue Einträge landen an dem Tag, den du gerade ansiehst.
4. **Monatsrückblick**: öffnet sich nach Monatsende von selbst. Korrigiere dort Anteile und deine Kontosumme.
5. **Apple Pay automatisch**: Richte einmal die Kurzbefehle-Automation ein (**Einstellungen → Apple-Pay-Automation**, Schritte unten). Dann kommt jede Apple-Pay-Zahlung an einem Kartenterminal (iPhone oder Apple Watch an das Lesegerät gehalten) von selbst in Ledgerline an, zum Bestätigen oder direkt eingetragen. Apple Pay online und in Apps gehört nicht dazu.
6. **Rückgängig**: Nach dem Löschen oder Importieren erscheint für ein paar Sekunden **Rückgängig**.
7. **Hilfe**: Jede Box hat neben ihrem Titel ein **?**, das erklärt, was sie zeigt.
8. **Tour**: **Einstellungen → Backup & Export → Tour starten** (auf dem iPhone **Mehr → Tour starten**) führt in 11 Stationen durch die App, auch dazu, wo du deine Fixkosten einträgst, und zur Apple-Pay-Automation. „Erst mal umsehen“ in der Einrichtung zeigt sie mit Beispieldaten; **Eigenes einrichten** entfernt die Beispieldaten und startet die Einrichtung.
9. **Einrichtungshilfe für deine KI**: auf der Seite Anleitung und unter **Einstellungen → Backup & Export**. Ein Text für ChatGPT, Claude o. Ä.; er führt dich Schritt für Schritt durch Installation, Sync und Apple-Pay-Automation und fragt nie nach Token, Passphrase oder Bankdaten.
10. **Neu**: Nach jedem Update zeigt ein kurzer Hinweis einmal die Änderungen.
11. **Backup**: Nach jedem Monatsrückblick unter **Einstellungen → Backup & Export → Backup herunterladen** sichern und die Datei in iCloud Drive o. Ä. ablegen.

### Apple-Pay-Automation einrichten (iPhone, einmalig)

**Voraussetzungen:** iOS 17 oder neuer, deine Karte in Apple Wallet und Sync auf dem iPhone (Abschnitt 9). Dieselben Schritte stehen in der App unter **Einstellungen → Apple-Pay-Automation** (tippe „Apple Pay“ in die Einstellungssuche), mit Tasten zum Kopieren der beiden Werte. Lass diese Seite offen, während du in Kurzbefehle arbeitest.

**In Ledgerline**

1. Öffne **Einstellungen → Apple-Pay-Automation** und wähle **Vorher fragen** oder **Direkt hinzufügen**.
2. Dort stehen die beiden Werte: die **Webadresse** (endet auf `/comments`) und der **Authorization**-Wert (beginnt mit `Bearer`).

**In der App Kurzbefehle**

1. Öffne **Kurzbefehle** und tippe unten in der Leiste auf **Automation** (nicht „Kurzbefehle“). Tippe oben rechts auf **+** (oder **Neue Automation**).
2. Eine Liste von Auslösern erscheint (Tageszeit, Wecker, E-Mail, …). Scrolle nach unten und tippe auf **Transaktion** (Wallet-Symbol). Siehst du stattdessen Aktionen wie *Karte öffnen* oder *Zahlung senden*, fügst du gerade einem Kurzbefehl eine Aktion hinzu: schließen und im Tab Automation neu beginnen.
3. Wähle unter **Karte** deine Karte(n), lass Händler und Kategorie, wie sie sind, wähle **Sofort ausführen** und tippe auf **Weiter**.
4. Tippe auf **Neue leere Automation**, dann **Aktion hinzufügen**. Suche **Inhalte von URL abrufen** und tippe darauf.

   *Auf neueren iPhones* öffnet sich die Automation als Kurzbefehl, der mit **„Wenn eine beliebige Karte verwendet wird“** beginnt, mit Schaltern für **Automation** (eingeschaltet lassen) und **Mitteilen**. Das ist richtig. Füge die Aktion über das **Suchfeld** unten hinzu. Die Zahlungsdaten heißen dort **Transaktion** oder **Kurzbefehleingabe**.
5. Tippe auf das blaue Wort **URL** und füge die Webadresse aus Ledgerline ein.
6. Tippe auf den Pfeil **›** daneben und stelle **Methode** auf **POST**.
7. Tippe unter **Header** auf **Neuen Header hinzufügen**. Schlüssel: `Authorization`. Text: den Authorization-Wert aus Ledgerline einfügen.
8. Wähle unter **Anfragetext** die Option **JSON**, tippe auf **Neues Feld hinzufügen → Text** und gib `body` als Schlüssel ein.
9. Gib im Feld daneben (beschriftet mit „Text“) `ledgerline|` ein (auf der iPhone-Tastatur liegt `|` unter **123 → #+=**).
10. Tippe in der Leiste über der Tastatur auf die Zahlungsvariable (**Transaktion** oder **Kurzbefehleingabe**), dann auf die eingefügte Blase, und wähle **Betrag**.
11. Tippe `|`, füge dieselbe Variable erneut ein, tippe darauf und wähle **Händler**. Das Feld lautet jetzt `ledgerline|Betrag|Händler`, mit Betrag und Händler als farbige Blasen.
12. Tippe auf **Fertig** bzw. den Zurück-Pfeil, um zu speichern.
13. Tippe einmal auf **▶**. Wenn iOS fragt, ob der Kurzbefehl eine Verbindung zu **api.github.com** herstellen darf, tippe auf **Erlauben** (oder **Immer erlauben**). Ohne das scheitert die Automation unbemerkt, wenn sie von selbst läuft. Der Testlauf kommt ohne Betrag an; Ledgerline zeigt ihn als unlesbar und entfernt ihn mit einem Tipp.

**Apple Pay online und in Apps** löst die Automation nicht aus: iOS bietet sie nur für das Halten von iPhone oder Apple Watch an ein Terminal. Online-Käufe erfasst du per Schnelleintrag, oder der monatliche Auszugsimport erfasst sie.

**Testen**: Bezahle etwas Kleines mit Apple Pay an einem Kassenterminal und öffne Ledgerline. Ein Hinweis zeigt die Zahlung, oder sie ist schon eingetragen. Die Automation von Hand auszuführen funktioniert nicht, weil es ohne echte Zahlung keinen Betrag und keinen Händler gibt.

**Prüfen, was angekommen ist**: **Jetzt nach Zahlungen suchen** in Ledgerline zeigt die Uhrzeit der letzten Prüfung, wie viele Zahlungen warten und was ohne Betrag ankam (mit einem Beispiel). Um nur die Verbindung zu testen, tippe in der Automation auf ▶: Kurzbefehle zeigt dann GitHubs Antwort (ein Textblock mit `"id"` heißt: hat funktioniert; „Bad credentials“ oder „Not Found“ heißen: Token oder Adresse stimmt nicht). Ein Testlauf von Hand kommt ohne Betrag an und erscheint als unlesbar; mit einem Tipp entfernen.

**Wenn nichts ankommt**: Öffne in der **Einstellungen-App des iPhones** (nicht in Ledgerline) **Apps → Wallet** und schalte **Mobile Daten** ein; prüfe, ob die Automation noch auf **Sofort ausführen** steht; tippe in Ledgerline auf **Jetzt nach Zahlungen suchen**; und wenn du dein GitHub-Token ersetzt, trag das neue auch in der Automation ein. Solange eine Zahlung auf Ledgerline wartet, liegt sie unverschlüsselt (nur Betrag und Händler) in deiner Sync-Datei und wird gelöscht, sobald sie abgeholt ist.

### Banken, die Ledgerline noch nicht kennt

Für Trade Republic, Scalable Capital, Sparkasse, comdirect, Wise, Finanzguru, flatex und Coinbase gibt es eigene Leser, dazu weitere Bank-Listen mit Datumsüberschriften. Bei allen anderen Banken versucht Ledgerline sein Bestes: Jede Zeile mit Datum und Betrag wird in der Prüfung vorgeschlagen, markiert mit „Layout noch unbekannt: bitte jede Zeile prüfen“. Prüfe Richtung (ausgegeben oder erhalten), Betrag und Name. Für einen richtigen Leser schickst du einen Beispiel-Screenshot oder ein PDF mit geschwärzten persönlichen Daten an die Person, die die App pflegt; er kommt mit dem nächsten Update, für alle mit dieser Bank.

### Datenschutz und Sicherheit

- **Nur auf dem Gerät gespeichert**, im Speicher des Browsers. Es gibt keinen Ledgerline-Server und kein Konto; wer dir die App geschickt hat, sieht deine Daten nicht.
- **Auf dem Gerät selbst nicht verschlüsselt**; geschützt durch die Gerätesperre. Unter **Einstellungen → App-Sperre** kannst du Face ID, Touch ID oder eine PIN hinzufügen.
- **Sync ist optional und Ende-zu-Ende-verschlüsselt** mit deiner Passphrase, bevor er dein eigenes GitHub-Konto erreicht. Ohne Passphrase lässt sich die Sync-Kopie nicht wiederherstellen.
- **Importe werden auf dem Gerät gelesen**; Dateien werden nie hochgeladen. Die Lesewerkzeuge werden einmalig von öffentlichen Code-Servern (cdnjs, jsDelivr) geladen.
- **Kurse** kommen aus einer öffentlichen GitHub-Datei und von CoinGecko. Diese Anfragen enthalten keine persönlichen Daten, verraten aber wie jede Webanfrage deine Internetadresse.
- **Apple-Pay-Automation** (optional): Betrag und Händler liegen kurz unverschlüsselt in deiner eigenen Sync-Datei und werden dann gelöscht.
- **Backups sind deine Aufgabe**: Browserdaten löschen oder die App vom Home-Bildschirm entfernen löscht die Daten auf diesem Gerät.
- **Vertrauen**: Der Code ist öffentlich. Updates kommen von der Person, die die App pflegt.

## Ledgerline mit Freunden und Familie teilen

Jeder kann Ledgerline über denselben Link nutzen. Die Daten bleiben auf den eigenen Geräten; niemand sieht die Daten anderer.

1. Link schicken: https://aaron-sn01.github.io/ledgerline/. Installiert wird wie oben unter **Die App installieren** beschrieben (iPhone, iPad, Mac, Windows, Android).
2. Beim ersten Öffnen startet die **Einrichtung**: Name, Währung, Sprache, Monatseinkommen, Fixkosten, Sparpläne, Bargeld und Sparziel. Jeder Schritt lässt sich überspringen, alles später in den Einstellungen ändern (**Einstellungen → Backup & Export → Einrichtung erneut starten**).
3. Für Sync zwischen den eigenen Geräten und die Apple-Pay-Automation braucht jede Person ein **eigenes** kostenloses GitHub-Konto und Token (Abschnitte 9 und 2); fremde lassen sich nicht nutzen. Ohne GitHub funktioniert alles andere auf einem Gerät.
4. Neue Versionen kommen automatisch beim nächsten Öffnen an; die Daten werden beim ersten Start angepasst.
5. ETF-Kurse kommen aus `tickers.json`. Fehlt ein Fonds, kann er dort ergänzt werden (Abschnitt 5), oder man gibt den Kurs von Hand ein.

## 3. Die App auf eine neue Version bringen

1. Die neue `index.html` herunterladen.
2. Im Repository **Add file → Upload files** wählen, die Datei hineinziehen (Name genau `index.html`) und **Commit changes** klicken.
3. Im Tab **Actions** warten, bis **pages build and deployment** einen grünen Haken zeigt (1 bis 2 Minuten, länger, wenn GitHub ausgelastet ist).
4. Die App bemerkt die neue Version von selbst (beim Öffnen, beim Zurückkehren und alle 30 Minuten) und zeigt **Neue Version verfügbar → Neu laden**. Falls nicht, auf dem Mac ⌘R drücken oder die App ganz beenden (⌘Q bzw. auf dem iPhone wegwischen) und neu öffnen. Die App nie aus dem Dock oder vom Home-Bildschirm entfernen, um sie zu aktualisieren: Das löscht ihre Daten auf diesem Gerät.

Deine Daten bleiben erhalten; neue Versionen passen alte Daten beim ersten Start automatisch an.

## 4. Kurse

- ETF-Kurse werden werktags alle 2 Stunden zwischen 09:23 und 23:23 Uhr deutscher Zeit aktualisiert. Nachts und am Wochenende nicht, weil die Börsen geschlossen sind.
- **Kurse aktualisieren** auf der Seite Vermögen prüft auf eine neuere Kursdatei; GitHub lädt dadurch nicht früher neue Kurse.
- Sofort laden: **Actions → Update prices → Run workflow**. Ein manueller Lauf aktualisiert auch die ETF-Zusammensetzungen.
- Kryptokurse kommen live von CoinGecko.
- Zeigt ein Kurs „—“: **Einstellungen → Kurs-Updater** nennt Fonds, bei denen der letzte Lauf fehlschlug. Prüfe dann das Yahoo-Symbol in `tickers.json`.

## 5. Ein neues Investment hinzufügen

### ETF, Aktie oder Anleihe-ETF mit automatischen Kursen

1. Das **Yahoo-Finance-Symbol** suchen (bei Xetra meist mit `.DE` am Ende, z. B. `EUNL.DE`; die ISIN auf finance.yahoo.com suchen).
2. In Ledgerline: **Vermögen → Position hinzufügen**, **ETF oder Aktie** wählen, Name, ISIN, Symbol, Broker, Anteile und **Anlageklasse** eintragen.
3. Auf GitHub `tickers.json` bearbeiten und eine Zeile in die Liste einfügen, durch Komma getrennt:

   ```
   { "symbol": "VAGF.DE", "isin": "IE00BG47KH54", "name": "Vanguard Global Aggregate Bond" }
   ```

4. Den Workflow von Hand starten (Abschnitt 4), damit der Kurs sofort erscheint.
5. Optional für die Sektor- und Länderdiagramme (nur Aktien): iShares- und Xtrackers-Fonds bekommen automatische Zusammensetzungen; einen vorhandenen Eintrag in `tickers.json` kopieren und anpassen.

### Krypto

**Position hinzufügen → Krypto** und die CoinGecko-ID eintragen (das Wort in der CoinGecko-Adresse, z. B. `bitcoin`).

### Alles ohne automatischen Kurs (Private Equity, Rente, Immobilienanteil)

**Position hinzufügen → Sonstiges Investment** oder **Private Equity** und den Kurs selbst eintragen; bei neuen Auszügen aktualisieren oder den Auszug importieren.

### Eine neue Anlageklasse

Im Positionsdialog **Anlageklasse → + Neue Anlageklasse …** wählen und einen Namen eingeben.

### Sparpläne

**Einstellungen → Dauerplan → Sparpläne**: Plan anlegen, mit der Position verknüpfen und den Tag im Monat setzen. Ledgerline fügt dann jeden Monat automatisch Anteile hinzu.

## 6. Plan und Einstellungen ändern

- **Einkommen, Fixkosten, jährliche Kosten, Sparpläne**: **Einstellungen → Dauerplan**, jeweils mit dem echten Abbuchungstag. Nur einen Monat ändern: **Monat → Plan dieses Monats bearbeiten**. Eine Änderung dort gilt sofort für den laufenden und alle schon angelegten Folgemonate, Eintrag für Eintrag; was du nur für einen Monat geändert hast (Monat → Plan dieses Monats bearbeiten), bleibt. Vergangene Monate ändern sich nie.
- **Plan-Vorschläge aus deinen Importen**: Zeigen importierte Auszüge, dass ein Einkommen oder eine Fixkosten-Zahlung an einem deutlich anderen Tag kommt als im Plan (mehr als eine Woche Abstand, drei Monate in Folge, jedes Mal innerhalb einer Woche um denselben Tag), oder dauerhaft mit anderem Betrag, schlägt die Übersicht eine Anpassung vor: **Ändern** passt den Plan ab diesem Monat an, **Behalten** lässt ihn und fragt für diesen Tag oder Betrag nicht wieder. Verschiebungen durch Wochenenden und Feiertage werden ignoriert.
- **Anteile aus Sparplänen**: Ledgerline schätzt jeden Sparplan-Kauf als Planbetrag ÷ Kurs des Tages. Zeigt ein Import die tatsächlich gekauften Anteile (Scalable-Umsatzlisten, Broker-Abrechnungen), ersetzt genau diese Zahl die Schätzung für diesen Monat, sodass die Anteile unter Vermögen zu deinem Broker passen.
- **Regelmäßige Zahlungen, die nicht im Plan sind**: Nach drei Zahlungen an (oder von) demselben Namen, mit gleichem Betrag und festem Rhythmus (jede Woche, alle zwei Wochen oder jeden Monat), bietet die Übersicht an, sie in den Plan aufzunehmen: als Fixkosten oder Einkommen, ab nächstem Monat (dieser Monat hat die Zahlungen schon als Einträge). Der Plan rechnet in Monaten; eine wöchentliche Zahlung wird daher als Monatsbetrag aufgenommen (Betrag × 52 ÷ 12). Die einzelne Zahlung wird gemerkt, damit spätere Importe sie weiter erkennen.
- **Im Voraus gezahltes Einkommen** (etwa ein Stipendium, das am 29. für den Folgemonat gezahlt wird): echten Zahltag eintragen und **Im Voraus gezahlt** anhaken. Es zählt für den Monat, für den es gedacht ist; Ledgerline erwartet es an diesem Tag im Vormonat und legt es ab dem Eingang für den nächsten Monat zurück, statt es als Ersparnis zu zählen. Importe erkennen eine solche Zahlung als geplantes Einkommen des nächsten Monats. Ändert sich der Zeitpunkt später, ändere den Eintrag und übernimm ihn ab diesem Monat.
- **Sparquoten-Ziel**: **Einstellungen → Sparquoten-Ziel**, optional mit Änderung ab einem Monat. Der Schalter darunter legt den Bargeld-Anteil des Ziels vor deinem Ausgabebudget zurück.
- **Kategorien**: **Einstellungen → Kategorien**: hinzufügen, umbenennen, umfärben, löschen; das Betragsfeld ist ein optionales Monatslimit.
- **Sprache, Währung, Zahlenformat**: **Einstellungen → Budget**.
- **Einstellungen finden**: Suchfeld oder Gruppentasten (Plan, Geld, Investments, Geräte, Erweitert).
- **50/30/20** (Seite Monat), nach der Faustregel: alle Ausgaben des Monats, auch Fixkosten, nach **Bedarf** (Ziel 50 % des Einkommens) und **Wünschen**; was vom Einkommen nicht ausgegeben wird, zählt als **gespart** (Sparpläne, Ersparnisse, Tilgung). Das Sparziel ist **dein Sparquoten-Ziel** aus den Einstellungen, Wünsche bekommen den Rest; bei 15 % Ziel steht in der Box also **50/35/15**, und sie folgt jeder Änderung des Ziels. Fixkosten zählen nach ihrer Gruppe, ein Abo ist also ein Wunsch, obwohl es fix ist; Alltagsausgaben nach Kategorie, im laufenden Monat inklusive dessen, was noch zu erwarten ist. Die Box zeigt auch die **Wohnkosten als Anteil am Einkommen** (Faustregel: bis 30 %). Unter **Was zählt als Bedarf?** stellst du jede Fixkosten-Gruppe und Kategorie auf Bedarf oder Wunsch. Auf der Seite **Jahr** zeigt dieselbe Box das bisherige Jahr. Im laufenden Monat siehst du **bisher** und **erwartet**; die Prognose nutzt deinen üblichen Ausgabenmix und lässt einmalige große Käufe (etwa eine Jahreskarte) weg.
- **Fixkosten in Diagrammen**: Die Monatsbalken (Seite Jahr) zeigen die 7 größten Kategorien des Jahres in eigenen Farben plus „Sonstiges“; tipp auf eine Farbe oder fahr darüber für Kategorie, Betrag und Anteil am Monat. **Nach Kategorie** (Monat) und **Kategorien dieses Jahr** (Jahr) enthalten die Fixkosten (dunklerer Teil jedes Balkens) mit Ringdiagramm; nimm das Häkchen bei **Mit Fixkosten** weg, um nur Alltagsausgaben zu sehen.
- **Sparmöglichkeiten** (Übersicht) werden jedes Mal aus Plan und Einträgen neu berechnet: mehrere Fixkosten derselben Art (zwei Handyverträge, drei Streamingdienste, zwei Fitnessstudios), Preiserhöhungen, jedes Streaming- oder App-Abo, Jahreskosten, die sich in den nächsten 45 Tagen verlängern, Bank- und Kartengebühren, derselbe kleine Kauf 5-mal oder öfter in 30 Tagen, Lieferdienste, Kategorien deutlich über deinem Schnitt und Kartenzahlungen, die regelmäßig wirken. Wohnen, Versicherungen und Spenden werden nie vorgeschlagen. **Behalten** blendet einen Vorschlag aus.
- **Details per Tippen oder Darüberfahren**: Diagramme, die Ausgaben, Einkommen oder Geldflüsse aufteilen, zeigen Details beim Tippen (iPhone, iPad, Surface) oder Darüberfahren (Mac, PC): Tag, Kategorie oder Monat mit Betrag und Anteil. Details erscheinen auf dem Diagramm selbst, nie auf einer Liste daneben, die die Zahlen schon zeigt; auf iPhone und iPad nur beim Tippen, nicht beim Scrollen. Auch die Ringe zeigen Details; nur das Geldfluss-Diagramm, das jede Zahl ausschreibt, nicht. Bei 50/35/15 hat der laufende Monat zwei Balken: **Bisher** (Ausgaben bis heute als Anteil am Monatseinkommen) und **Erwartet für den Monat**; liegen die Ausgaben voraussichtlich über dem Einkommen, wird der Balken passend skaliert und ein Hinweis sagt, um wie viel.
- **Automatisches Backup auf dem Mac** (Einstellungen → Backup & Export → Automatisches Backup auf dem Mac): Mit Sync speichert eine monatliche Kurzbefehle-Automation auf dem Mac deine **verschlüsselte** Sync-Datei in einen Ordner und ersetzt die vorige Kopie (eine Datei, kein Stapel). Das Fenster zeigt die Adresse zum Kopieren und die Schritte: App Kurzbefehle → neuer Kurzbefehl mit **Inhalte von URL abrufen** (die Adresse) und **Datei sichern** (Speicherort erfragen aus, Unterpfad `Ledgerline/ledgerline-backup.json`, Überschreiben, falls vorhanden an) → einmal ausführen → Tab **Automation** → **Tageszeit**, **Monatlich**, Kurzbefehl wählen; **Vor dem Ausführen fragen** aus lassen (Standard), damit er von selbst läuft, und **Mitteilen** einschalten für einen monatlichen Hinweis. Wiederherstellen: **Aus Backup wiederherstellen**, Datei wählen, Sync-Passphrase eingeben. Ohne Passphrase lässt sich die Datei nicht öffnen, weder von dir noch von anderen. GitHub bewahrt außerdem jede frühere Version der Sync-Datei auf.
- **Sicherheit**: Deine Sync-Datei wird auf deinem Gerät verschlüsselt (AES-256, Schlüssel aus deiner Passphrase). Auf dem Gerät schützt die Sperre des Geräts die Daten. Die beiden Lesewerkzeuge für Screenshots und PDFs werden vor dem Start mit ihren veröffentlichten Fingerabdrücken geprüft, und eine Sicherheitsregel in `index.html` erlaubt der App nur Verbindungen zu GitHub, CoinGecko, dem EZB-Kursdienst und den Servern der Lesewerkzeuge. Schalte die Zwei-Faktor-Anmeldung für dein GitHub-Konto ein.
- **Links in der App**: Wo ein Text sagt, wohin es geht („Einstellungen → Dauerplan“, „Vermögen → Ersparnisse“), tippst du darauf und springst direkt zu dieser Box, die kurz hervorgehoben wird. In einem Hilfe-Fenster öffnet „Anleitung“ die passende Stelle dieser Anleitung.
- **Monatsausblick**: „Noch zu erwartende Alltagsausgaben“ ist eine Prognose für die restlichen Tage (etwa 29 € pro Tag × 23 verbleibende Tage), nicht das bisher Ausgegebene. „Voraussichtlich in die Ersparnisse“ und die erwartete Sparquote bauen darauf auf. Einmalige große Käufe (mindestens 100 € und mindestens fünfmal so viel wie dein üblicher Kauf, etwa eine Jahreskarte) zählen einmal, werden aber nicht auf die restlichen Tage fortgeschrieben. „Investiert“ zeigt, was bisher investiert wurde; noch anstehende Pläne stehen darunter.
- **Wohin das Geld floss / Vermögen im Zeitverlauf**: Zeitraum 1M, 3M, 6M, 1J oder Alle. Die Zusammenfassung zählt erst ab Beginn deiner Aufzeichnung; davor (gestrichelte Linie) ist es eine Schätzung aus deinen heutigen Positionen zu früheren Kursen.
- **Boxen**: Auf den Titel tippen klappt eine Box ein; **Boxen anordnen** unten auf jeder Seite verschiebt sie mit den Pfeilen ↑ ↓; mit Maus oder Trackpad kannst du auch am Griff ⠿ ziehen (auf iPhone und iPad gibt es nur die Pfeile, weil Ziehen in Safari dort nicht zuverlässig klappt). Beides wird pro Gerät gespeichert.

## 7. Bargeld und Konten

Ledgerline behandelt alle Konten als eine Summe. Das Budget des laufenden Monats wird davon zurückgehalten; der Rest zählt als Ersparnisse.

- Summe korrigieren: **Vermögen → Ersparnisse → Saldo aktualisieren**, optional mit jedem Konto einzeln. Beim ersten Konto bleibt deine bisherige Summe als Zeile „Meine bisherigen Konten“ erhalten, damit nichts verloren geht; teile sie auf, wann immer du willst.
- **Konten bleiben aktuell**: Geld, das du den Ersparnissen hinzufügst oder entnimmst (Zinsen, aus Ersparnissen Bezahltes, Tilgungen, Verkäufe), wird dem Konto mit derselben Währung zugerechnet. Gibt es noch keins in dieser Währung, wird eins angelegt (etwa „CAD-Konto“), damit „Je Währung“ es in dieser Währung zeigt. **Saldo aktualisieren** öffnet sich deshalb mit dem aktuellen Stand jedes Kontos, und Summe, Ersparnisse und **Je Währung** stimmen immer überein. Korrigiere dort ein Konto, dann ist das sein neuer Ausgangspunkt.
- **Neues Sparkonto**: einfach als weitere Zeile hinzufügen. Überweisungen zwischen eigenen Konten sind nie Ausgaben; der Import überspringt sie.
- Zinsen kommen als **Einnahme → Ersparnisse** hinein; der Import erledigt das bei Zinszeilen automatisch.

## Währungen

Alles wird in deiner **Heimatwährung** angezeigt (die Einrichtung fragt danach; ändern unter **Einstellungen → Budget → Währung**). Wenn du in mehreren Währungen lebst, verdienst oder investierst, setz darunter das Häkchen **Ich nutze mehr als eine Währung**. Dann:

- **Einträge**: Neben dem Betrag auf Heute und im Eintragsdialog gibt es eine Währungsauswahl. Ein Kauf über 12,00 £ wird als 12,00 £ gespeichert und zum Kurs des Tages umgerechnet; der Originalbetrag bleibt in der Liste sichtbar.
- **Plan**: Jedes Einkommen, jede Fixkosten-Position und jeder Sparplan kann eine eigene Währung haben (ein Gehalt in CHF, Miete in GBP). Das Monatsbudget nutzt den Kurs am Zahltag, bis dahin den heutigen.
- **Konten**: Unter **Saldo aktualisieren** bekommt jedes Konto eine Währung; die Summe wird umgerechnet.
- **Positionen**: Jede Position hat eine Kurswährung, aus der Kursdatei (ein US-Fonds in USD) oder im Dialog gewählt. Der Wert wird zum heutigen Kurs umgerechnet, der Verlauf zum Kurs jedes Tages.
- **Schulden**: Beim Anlegen die Währung wählen. Die Karte zeigt Beträge in dieser Währung plus die umgerechnete Summe; Tilgungen werden zum Tageskurs umgerechnet.
- **Vermögen**: Das Vermögen wird zu aktuellen EZB-Kursen in deine Heimatwährung umgerechnet; darunter steht, sobald du mehr als eine Währung hältst, **jede Währung für sich**, nicht umgerechnet (Positionen in ihrer Kurswährung, Konten, Schulden). Das Diagramm **Währungen** unter Anlageklassen zeigt dasselbe Geld nach Währung aufgeteilt.
- **Heimatwährung ändern** rechnet Einträge zum Kurs ihres Tages um; Plan, Positionen, Konten und Schulden behalten ihre Währung und werden automatisch umgerechnet.
- **Wechselkurse** sind die offiziellen täglichen EZB-Referenzkurse (etwa 30 Währungen, darunter USD, GBP, CHF, CAD und SGD), dazu VAE-Dirham, Saudi- und Katar-Riyal, Omanischer Rial sowie Bahrain- und Jordanischer Dinar über ihre offizielle feste Bindung an den US-Dollar, geladen von frankfurter.app und auf dem Gerät gespeichert, sodass die App offline mit den letzten Kursen funktioniert. **Aktualisieren** bei der Währungseinstellung lädt sie neu.

Mit nur einer Währung ändert sich nichts: Jede Zahl ist genau wie vorher.

## 8. Schulden

- **Schulden → Schuld hinzufügen**: Restbetrag, Zinssatz (0 bei zinsfrei) und optional Zieldatum.
- **Tilgungsplan**: „Mit fester Monatsrate tilgen“ aktivieren, Betrag und Tag setzen. Die Rate wird Teil der Fixkosten und nach Zinsen automatisch abgezogen.
- Sondertilgungen: **Tilgung erfassen** auf der Seite Schulden, aus Ersparnissen oder aus dem Monatsbudget.

## 9. Sync zwischen Geräten

Sync hält deine Geräte über eine verschlüsselte Datei in **deinem eigenen kostenlosen GitHub-Konto** auf demselben Stand. Ohne Sync funktioniert alles auf einem Gerät; mit Sync zeigen Handy und Laptop dieselben Daten. Du richtest es einmal ein, in etwa 10 Minuten.

**A. GitHub-Konto anlegen** (überspringen, wenn du eins hast)

1. Geh auf **github.com/signup**, gib E-Mail, Passwort und Benutzernamen ein und folge den Schritten.
2. Bestätige deine E-Mail-Adresse mit dem Code oder Link, den GitHub schickt.

**B. Token erstellen** (der Schlüssel, mit dem Ledgerline deine Sync-Datei erreicht)

1. Angemeldet bei GitHub öffnest du **github.com/settings/tokens/new**. Falls GitHub nach der Art fragt, wähle **Tokens (classic)**.
2. **Note**: „Ledgerline“ eingeben. **Expiration**: **No expiration** wählen.
3. In der Liste der Berechtigungen **nur gist** anhaken. Sonst nichts.
4. Unten auf **Generate token** klicken. Kopiere das Token (beginnt mit `ghp_`) und speichere es im Passwortmanager: GitHub zeigt es nur einmal.

**C. Geräte verbinden**

- **Erstes Gerät**: In Ledgerline **Einstellungen → Sync zwischen Geräten**: Token einfügen, eine Passphrase wählen (mindestens 8 Zeichen; im Passwortmanager speichern, sie lässt sich nicht wiederherstellen), **Sync-ID** leer lassen und **Sync-Datei erstellen** klicken. Die **Sync-ID** erscheint dann im selben Feld mit einer **Kopieren**-Taste und bleibt dort sichtbar; sie ist auch der Code am Ende der Adresse der Sync-Datei auf gist.github.com.
- **Jedes weitere Gerät**: dasselbe Token, **diese** Sync-ID und dieselbe Passphrase, dann **Verbinden**. Auf einem neuen Gerät führt „Ich nutze Ledgerline schon auf einem anderen Gerät“ in der Einrichtung direkt dorthin.
- Alle Geräte müssen **dieselbe Sync-ID** zeigen. Weicht eine ab, dort **Dieses Gerät trennen** und mit der richtigen ID verbinden; die Daten werden zusammengeführt.
- Jede Person nutzt ihr eigenes Konto und Token; gib deins nie weiter.

## 10. App-Sperre

**Einstellungen → App-Sperre**: Face ID / Touch ID mit PIN als Ersatz, auf jedem Gerät separat. Die App sperrt sich nach 2 Minuten im Hintergrund.

## 11. Fehlerbehebung

- **Kurse wirken alt**: siehe Abschnitt 4. Ein roter Lauf von **Update prices** unter Actions zeigt den Grund; meist behebt sich das beim nächsten Lauf.
- **App nach dem Hochladen nicht aktualisiert**: Prüfen, ob die Datei genau `index.html` heißt, auf den grünen Haken bei **pages build and deployment** warten, dann neu laden. Bleiben Bereitstellungen auf „Queued“, githubstatus.com prüfen.
- **„Sync-Problem, siehe Einstellungen“**: **Einstellungen → Sync zwischen Geräten** nennt den genauen Grund. „Slow down“ ist GitHubs Limit und verschwindet von selbst; „Refused access“ heißt, dem Token fehlt die gist-Berechtigung.
- **Apple-Pay-Zahlungen kommen nicht an**: siehe Abschnitt 2.
- **Nach einem Import stimmt etwas nicht**: den Eintrag auf der Seite Monat öffnen und bearbeiten oder löschen.
- **Demodaten** (**Einstellungen → Backup & Export → Mit Demodaten ansehen**): überschreiben nie deine Daten. Sie fügen Beispiel-Einträge von Januar bis heute hinzu, als Demo markiert, und werden wie jeder Eintrag auf deine anderen Geräte synchronisiert. Solange sie da sind, fließen sie in Budget, Sparquote und Diagramme ein. **Demodaten entfernen** an derselben Stelle löscht genau diese Einträge und stellt Startmonat, Kontosumme und Meilensteine wieder her (für ein paar Sekunden erscheint **Rückgängig**). Ganz ohne Auswirkung auf deine Daten probierst du sie in einem separaten Browser aus (etwa einem Safari-Tab statt der App auf dem Home-Bildschirm), ohne Sync zu verbinden.
- **Alle Daten in diesem Browser löschen** (Einstellungen → Backup & Export) betrifft nur den Browser bzw. die installierte App, in der du es antippst; andere Browser, andere Geräte, deine Sync-Datei und Backups bleiben, wie sie sind.
- **Ein Gerät neu aufsetzen**: zuerst ein Backup unter **Einstellungen → Backup & Export** sichern, später mit **Aus Backup wiederherstellen** einspielen.

## 12. Für einen KI-Assistenten oder Entwickler

Sicherheitsregel: Das Content-Security-Policy-`<meta>` in `1_head.html` listet jeden externen Dienst, den die App laden oder kontaktieren darf; braucht eine Funktion einen neuen Dienst, trag ihn dort ein. Die Lesewerkzeuge werden mit Integritäts-Fingerabdrücken geladen (`LIB_SRI` in `4c_ui.js`); ein Werkzeug-Update bedeutet neue Version und neuen Fingerabdruck (sha384 der exakten npm-Datei).

Detail-Hinweise (`data-tip`): nur auf Diagrammformen, nie auf Legenden- oder Listenzeilen, die die Zahlen schon zeigen.

Boxen: Jede Box auf einer Seite muss verschiebbar sein. Die Verschiebe-Bedienelemente kommen ganz am Ende von `render()` dazu, nach allen `AFTER_RENDER`-Funktionen, damit auch nachträglich eingefügte Boxen dabei sind; prüf vor jeder Version den Anordnen-Modus auf jeder Seite (`tests/move_t.py`).

Schreibstil für jeden Text der App: kurz und einfach, ein Gedanke pro Satz, nichts wiederholen, was der Bildschirm schon zeigt; Wegbeschreibungen zu einer anderen Stelle der App werden als „Seite → Box“ geschrieben, damit sie zu Links werden.

Lies diesen Abschnitt, bevor du etwas änderst. Der Eigentümer ist kein Programmierer: Gib vollständige Dateien zurück, die sich so hochladen lassen, und erkläre GitHub-Schritte Klick für Klick.

### Vorgaben

- Die App ist eine einzige, eigenständige `index.html`: reines JavaScript, kein Framework, kein Build-Schritt beim Ausliefern, kein Paketmanager. Das bleibt so.
- Externer Code wird nur bei Bedarf von cdn.jsdelivr.net geladen, mit Integritäts-Fingerabdrücken: PDF.js für PDF-Text und Tesseract.js für die Texterkennung in Screenshots. Alles andere steckt in der Datei.
- Netzwerkzugriffe gibt es nur zur GitHub-API (verschlüsselter Gist-Sync), zu den EZB-Wechselkursen über frankfurter.app, zu `prices.json` und `compositions.json` aus demselben Repository (zuerst raw.githubusercontent.com, dann dieselbe Adresse), zu CoinGecko für Krypto und zum CDN. Keine Analyse-Dienste, keine anderen Server.
- Persönliche Daten bleiben auf dem Gerät. Importe werden lokal gelesen.
- **Das Repository ist öffentlich. Schreib nie persönliche Daten in den Code** (keine Namen, Beträge, Positionen oder Anteile in Startdaten, Voreinstellungen oder Beispielen). `seedPlan`, `seedHoldings` und `seedDebts` sind absichtlich leer; ein neues Gerät wird per Sync oder Backup befüllt.
- Die Oberfläche ist zweisprachig (Englisch und Deutsch), jeder Text muss in beiden Sprachen da sein. **Daten werden immer als Tag.Monat.Jahr angezeigt** (05.10.2026, im Englischen 05/10/2026), über `fmtDate`, `fmtDateTime` und die Datumsfelder. Nie Monat/Tag.

### Aufbau von index.html

Die Datei ist eine Folge von Blöcken in dieser Reihenfolge. Spätere Blöcke dürfen frühere nutzen; der Start-Block muss der letzte bleiben.

1. `<head>` und `<style>`: Design-Variablen (hell und dunkel), Layout, Komponenten, Druckstile für die PDF-Zusammenfassung.
2. Kern: Konstanten und Speicherschlüssel, Formatierung (Geld in ganzen Cent, `fmt`, `fmtDate`), Symbole, Kategorien und Startdaten, `defaultState` und `migrate`, die Budget-Berechnung (`computeMonth`, `aggregate`, Wochentagsmodell, Wahrscheinlichkeits-Simulation), Bargeld (`cashSavings`, Geld-Ausblick), Vermögen (`wealth`, `wealthSeries`, Kurse über `Prices`), Schulden (`debtLedger`, `debtStatus`, `debtPlansFor`), Prognose (Monte Carlo), Streuung, Diagramme (`sankeySVG`, `flowNodes` und weitere), Sync (`Sync`, AES-GCM mit PBKDF2-Schlüssel) und App-Sperre (`Lock`, WebAuthn und PIN).
3. Oberfläche: `render()`, eine `view…()`-Funktion pro Seite, Dialoge, die `ACTIONS`-Tabelle (jede Schaltfläche hat `data-act="name"`), Eingabe-Bindung, einklappbare Boxen (`decoratePanels`).
4. Import: `IMP` (eigene Leser pro Dokumentart, dazu `IMP.genericPdf` als Notlösung für unbekannte Banken: Trade Republic, Sparkasse, flatex, Coinbase), Einordnung in `buildProposals` (Überträge, Fixkosten- und Plan-Abgleich, Erstattungen, Doppelte, Kategorien) und der Prüf-Dialog. Doppelte findet `align()`: eine reihenfolgetreue Eins-zu-eins-Zuordnung von Einträgen mit gleichem Betrag und ähnlichem Namen innerhalb von 2 Tagen (und 15 Minuten, wenn beide eine Uhrzeit haben); Einträge aus derselben Datei werden nie gepaart. Ersetz das nicht durch eine einfache Prüfung „gleicher Betrag innerhalb weniger Tage“: Sie würde wiederholte Käufe zusammenlegen.
5. PDF-Zusammenfassung: Abschnitte und Druck auf eine Seite.
6. Übersicht: Sparquote und Ziel, typischer Monat, Kategorie-Trends und Limits, Sparmöglichkeiten, Vermögensänderung, das Mehr-Menü.
   Extras (nach den Datumsfeldern und der Anleitung): der Apple-Pay-Eingang (`Inbox`: liest und löscht Kommentare der Form `ledgerline|Betrag|Händler` am Sync-Gist und schickt sie durch die normale Import-Prüfung), die „?“-Hilfe (`HELP`, ein Text pro Box-Titel, dazu `HELP_BY_VIEW` für Boxen mit eigenem Titel; jede neue Box braucht einen Eintrag), Suche und Gruppen in den Einstellungen, `Undo`, Hinweise und Meilenstein-Feiern. Sie hängen sich über `window.AFTER_RENDER` ein, eine Liste von Funktionen, die nach jedem Zeichnen läuft.
7. Anordnen-Modus: Reihenfolge der Boxen (`applyLayout`).
8. Datumsfelder: ersetzen die eingebauten Datumseingaben durch Tag.Monat.Jahr-Felder.
9. Anleitung (`MANUAL_MD` und `MANUAL_DE`), Extras (siehe oben), der Einrichtungs-Assistent (`openWizard`), der einmal auf einem Gerät ohne Daten oder Sync öffnet, und Deutsch (`DE`, `DE_BLOCK`, `DE_PAT`, `HELP_DE`). Die Oberfläche ist auf Englisch geschrieben; mit Deutsch tauscht ein Übersetzungsdurchgang jeden gezeichneten Text aus: ganze formatierte Absätze (`DE_BLOCK`), einzelne Texte (`DE`), dann Sätze mit Zahlen (`DE_PAT`, reguläre Ausdrücke). Neuere Texte nutzen `L2('Englisch', 'Deutsch')` direkt. Auch Bestätigungs- und Eingabefenster des Browsers (`confirm`, `prompt`, `alert`) werden übersetzt. **Jeder neue oder geänderte englische Text braucht eine deutsche Entsprechung**; die Wörterbücher liegen in `i18n/` in den Arbeitsdateien.
10. Start: startet Sync, Sperre und das erste Zeichnen. Er muss das letzte Skript bleiben.

### Datenmodell

Gespeichert im localStorage unter `ledgerline:data:v2` (Oberflächenzustand unter `ledgerline:ui:v2`, eingeklappte Boxen und Anordnung unter eigenen Schlüsseln). Aufbau:

- `schema`: Versionsnummer. Erhöh sie in `defaultState` und ergänze einen Schritt in `migrate()`, sobald sich der gespeicherte Aufbau ändert; alte Daten müssen weiter funktionieren.
- `settings`: der Dauerplan (`recurring.income`, `bills`, `annual`, `savings`), `categories` (optional mit `limit`, `bucket` Bedarf/Wunsch; Fixkosten nutzen dieselben Kategorien), `cash` (`amount`, `date`, `mode: 'accounts'`), `cashAccounts`, `savingsGoals`, `goalInBudget`, `assetClasses`, `projection`, Sync- und Kurs-Einstellungen.
- `months`: `{ "JJJJ-MM": Plan }`, eine Kopie des Plans pro Monat, damit Änderungen an einem Monat andere nicht betreffen.
- `transactions`: `{ id: { name, amount, date, type, category, … } }`. `type` ist `out` (Ausgabe), `in` (Einnahme), `invest` (mit `accountId` und `source` Budget, Bonus oder Ersparnisse), `debt` (mit `debtId`) oder `sell` (mit Anteilen, Brutto, Steuer und Gebühren).
- `holdings`: `{ id: { name, isin, symbol, kind, assetClass, broker, base: { shares, date, at }, manualPrice, coingeckoId } }`. Die Anteile sind `base` plus Sparplan-Ausführungen und Buchungen nach `base.date`; tatsächlich gekaufte Anteile aus Importen stehen in `settings.planActual`.
- `debts`: `{ id: { name, original, rate, plan: { on, amount, day, start }, base: { balance, date }, target } }`.

Währungen (Block `4m_fx`): Jeder Betrag wird in der Heimatwährung gespeichert (`settings.currency`); ein Eintrag in anderer Währung behält zusätzlich `cur` und `orig` (Originalbetrag in Cent). Plan-Einträge, Positionen, Konten und Schulden können `cur` tragen und werden beim Lesen umgerechnet (`fxPlan`, `quoteOf`/`priceOn`, `debtTxAmount`, `totalDebt`). Kurse: `FX.rate(cur, iso)` (auf EUR-Basis, letzter veröffentlichter Tag bis zum Datum), `fxConv(cents, from, to, iso)`. Ohne fremde Währung gibt die Umrechnung ihren Wert unverändert zurück; das muss so bleiben. `fetch_prices.py` speichert die Währung jedes Kurses (Londoner Pence in Pfund umgerechnet).

Regeln: Beträge sind ganze Cent; Daten werden als ISO `JJJJ-MM-TT` gespeichert; jedes Objekt hat `updatedAt`; Löschen setzt `deleted: true` (nötig für den Sync, der pro Objekt zusammenführt, die letzte Änderung gewinnt). Speicherschlüssel nie umbenennen.

### Kurs-Abruf

GitHub Actions führt werktags alle 2 Stunden `fetch_prices.py` aus und monatlich sowie bei manuellem Start `fetch_compositions.py`, dann werden `prices.json` (Kurse plus etwa 400 Tage Tagesschlusskurse) und `compositions.json` gespeichert. Die App zeigt den Zeitstempel jeder Datei. Für einen neuen Fonds trag ihn in `tickers.json` ein.

### Eine Änderung testen

1. Im Repository-Ordner `python3 -m http.server 8765` starten und http://localhost:8765/ öffnen.
2. **Einstellungen → Backup & Export → Mit Beispieldaten ansehen** füllt zehn Monate mit Einträgen, damit jedes Diagramm Inhalt hat.
3. Prüf jede Seite und jedes Fenster in beiden Sprachen auf allen aktuellen iPhone-Größen vom iPhone SE (320 px) über iPhone 15/16/17 und Pro (393–402 px) bis Plus und Pro Max (430–440 px) (`tests/phones_t.py`), auf iPad mini, iPad/Air, Pro 11 und 13 Zoll, hoch, quer und im geteilten Bildschirm (`tests/ipads_t.py`), auf jeder Mac-Größe vom kleinen Fenster bis zum 27-Zoll-Bildschirm und auf allen Microsoft-Surface-Modellen, quer und hoch (`tests/desktops_t.py`); sieh dir auch einen Screenshot auf einem großen Bildschirm an, weil die automatischen Prüfungen leeren Platz nicht beurteilen, und das in hellem und dunklem Modus. Prüf, dass keine Seite seitlich scrollt, kein Datum Monat/Tag zeigt, lange Wörter nur an einer Silbe getrennt werden (mit Bindestrich, nie abgeschnitten, keine winzige Schrift, um etwas passend zu machen) und dass jeder neue oder geänderte Text in beiden Sprachen da ist: Im Deutschen darf kein englisches Wort stehen, im Englischen kein deutsches (`tests/de_words_t.py` prüft jedes sichtbare Wort mit einem Wörterbuch).
4. Prüf, dass das Geldfluss-Diagramm aufgeht: Alles, was in „Einnahmen“ fließt, fließt auch wieder hinaus.
5. Prüf, dass ein bestehendes Backup weiter lädt (Migration).

### Eine Änderung übergeben

Gib die vollständige, aktualisierte `index.html` zurück, dazu jede andere geänderte Datei, mit Anleitung zum Hochladen. **Jede neue Version bekommt oben in `CHANGELOG` einen Eintrag** (einmal als „Neu“ angezeigt). **Wichtige neue Funktionen aktualisieren auch die Tour** (`TOUR_STEPS`, Englisch und Deutsch) und, wo nötig, die Einrichtungshilfe (`SETUP_HELP_EN`, `SETUP_HELP_DE`); kleine Korrekturen nicht. **Zu jeder Änderung gehört eine aktualisierte Anleitung**: `MANUAL.md` und `MANUAL.de.md` gemeinsam ändern und `APP_VERSION` (in den Einstellungen angezeigt) erhöhen; das Build-Skript setzt die Versionszeile beider Anleitungen. Funktionen, auf die sich der Eigentümer verlässt, müssen weiter funktionieren: Import, Apple-Pay-Eingang, Sync, App-Sperre, das Sparziel im Budget, Tag.Monat.Jahr-Daten sowie eingeklappte und angeordnete Boxen.
