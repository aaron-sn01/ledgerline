# Ledgerline-Anleitung

*Version 2026-10-08 · 56. Diese Anleitung wird mit jeder neuen Version der App aktualisiert; die Versionsnummer unter **Einstellungen → Backup & Export** sollte übereinstimmen.*

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

1. **Ausgaben erfassen** auf der Seite Heute: Name und Betrag eingeben. Ledgerline schlägt eine Kategorie vor; tippe auf eine andere, wenn sie nicht passt. Es lernt aus jeder Korrektur.
2. **Importieren statt tippen**: Tippe auf **Importieren** und wähle Screenshots oder PDF-Auszüge (Trade Republic, Sparkasse, flatex, Coinbase). Prüfe die Liste, entferne Häkchen bei allem, was du nicht willst, und tippe auf **Ausgewählte hinzufügen**.
   - **Trade-Republic-Screenshots**: die Umsatzliste (alles unter „Anstehend“ wird übersprungen, weil es noch nicht passiert ist; die wöchentlichen Saveback- und Aufrundungs-Einträge zählen) oder **eine geöffnete Zahlung** (praktisch für einen einzelnen Kauf; ihre „Vorteile“ bleiben außen vor, weil Trade Republic Saveback und Aufrundungen einmal pro Woche gesammelt zahlt und die Liste diesen Wocheneintrag zeigt).
   - **Sparkasse-Screenshots**: die Umsatzliste oder **eine geöffnete Zahlung** („Umsatzdetails“): Name, Betrag, Buchungsdatum und Verwendungszweck werden gelesen. Ist es eine deiner Fixkosten (etwa die Handyrechnung von Telefonica, also O2), wird sie erkannt und übersprungen, weil der Plan sie schon zählt.
   - **Doppelte Einträge**: Was schon in Ledgerline ist oder in zwei importierten Dateien vorkommt, wird mit einem Hinweis abgewählt. Wiederholte Käufe (mehrere Fahrscheine zu 3,00 €) zählen einzeln: Jeder Eintrag kann nur zu einem anderen passen, Zahlungen aus derselben Datei gelten nie als doppelt, und unterschiedliche Uhrzeiten (Apple Pay) bedeuten unterschiedliche Zahlungen. Ist etwas zu Unrecht abgewählt, setz das Häkchen.
   - **Einfügen statt speichern**: Screenshot machen, auf die Vorschau tippen, dann **Fertig → Kopieren und löschen**. In Ledgerline auf **Importieren → Screenshot einfügen** tippen (falls das iPhone fragt: **Einfügen erlauben**). Klappt die Taste nicht, tippe in das gestrichelte Feld daneben und wähle **Einfügen**. Auf dem Mac funktioniert ⌘V, solange das Importfenster offen ist.
3. **Tage durchblättern**: Die App öffnet immer mit der Übersicht, auch wenn du nach mehr als 10 Minuten zurückkehrst (kürzere Abstecher in eine andere App behalten deine Stelle). Auf der Seite Heute blätterst du mit den Pfeilen neben dem Datum zu früheren oder späteren Tagen. Neue Einträge landen an dem Tag, den du gerade ansiehst.
4. **Monatsrückblick**: öffnet sich nach Monatsende von selbst. Korrigiere dort Anteile und deine Kontosumme.
5. **Apple Pay automatisch**: Richte einmal die Kurzbefehle-Automation ein (**Einstellungen → Apple-Pay-Automation**, Schritte unten). Dann kommt jede Apple-Pay-Zahlung an einem Kartenterminal (iPhone oder Watch an das Lesegerät gehalten) von selbst in Ledgerline an, zum Bestätigen oder direkt eingetragen. Apple Pay online und in Apps gehört nicht dazu.
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

**Apple Pay online und in Apps** löst die Automation nicht aus: iOS bietet sie nur für das Halten von iPhone oder Watch an ein Terminal. Online-Käufe erfasst du per Schnelleintrag, oder der monatliche Auszugsimport erfasst sie.

**Testen**: Bezahle etwas Kleines mit Apple Pay an einem Kassenterminal und öffne Ledgerline. Ein Hinweis zeigt die Zahlung, oder sie ist schon eingetragen. Die Automation von Hand auszuführen funktioniert nicht, weil es ohne echte Zahlung keinen Betrag und keinen Händler gibt.

**Prüfen, was angekommen ist**: **Jetzt nach Zahlungen suchen** in Ledgerline zeigt die Uhrzeit der letzten Prüfung, wie viele Zahlungen warten und was ohne Betrag ankam (mit einem Beispiel). Um nur die Verbindung zu testen, tippe in der Automation auf ▶: Kurzbefehle zeigt dann GitHubs Antwort (ein Textblock mit `"id"` heißt: hat funktioniert; „Bad credentials“ oder „Not Found“ heißen: Token oder Adresse stimmt nicht). Ein Testlauf von Hand kommt ohne Betrag an und erscheint als unlesbar; mit einem Tipp entfernen.

**Wenn nichts ankommt**: Öffne auf dem iPhone **Einstellungen → Apps → Wallet** und schalte **Mobile Daten** ein; prüfe, ob die Automation noch auf **Sofort ausführen** steht; tippe in Ledgerline auf **Jetzt nach Zahlungen suchen**; und wenn du dein GitHub-Token ersetzt, trag das neue auch in der Automation ein. Solange eine Zahlung auf Ledgerline wartet, liegt sie unverschlüsselt (nur Betrag und Händler) in deiner Sync-Datei und wird gelöscht, sobald sie abgeholt ist.

### Banken, die Ledgerline noch nicht kennt

Für Trade Republic, Sparkasse, flatex und Coinbase gibt es eigene Leser. Bei allen anderen Banken versucht Ledgerline sein Bestes: Jede Zeile mit Datum und Betrag wird in der Prüfung vorgeschlagen, markiert mit „Layout noch unbekannt: bitte jede Zeile prüfen“. Prüfe Richtung (ausgegeben oder erhalten), Betrag und Name. Für einen richtigen Leser schickst du einen Beispiel-Screenshot oder ein PDF mit geschwärzten persönlichen Daten an die Person, die die App pflegt; er kommt mit dem nächsten Update, für alle mit dieser Bank.

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
- **Im Voraus gezahltes Einkommen** (etwa ein Stipendium, das am 29. für den Folgemonat gezahlt wird): echten Zahltag eintragen und **Im Voraus gezahlt** anhaken. Es zählt für den Monat, für den es gedacht ist; Ledgerline erwartet es an diesem Tag im Vormonat und legt es ab dem Eingang für den nächsten Monat zurück, statt es als Ersparnis zu zählen. Importe erkennen eine solche Zahlung als geplantes Einkommen des nächsten Monats. Ändert sich der Zeitpunkt später, ändere den Eintrag und übernimm ihn ab diesem Monat.
- **Sparquoten-Ziel**: **Einstellungen → Sparquoten-Ziel**, optional mit Änderung ab einem Monat. Der Schalter darunter legt den Bargeld-Anteil des Ziels vor deinem Ausgabebudget zurück.
- **Kategorien**: **Einstellungen → Kategorien**: hinzufügen, umbenennen, umfärben, löschen; das Betragsfeld ist ein optionales Monatslimit.
- **Sprache, Währung, Zahlenformat**: **Einstellungen → Budget**.
- **Einstellungen finden**: Suchfeld oder Gruppentasten (Plan, Geld, Investments, Geräte, Erweitert).
- **Monatsausblick**: „Voraussichtlich in die Ersparnisse“ und die erwartete Sparquote gehen für den Rest des Monats von deinen üblichen Alltagsausgaben aus. Einmalige große Käufe (mindestens 100 € und mindestens fünfmal so viel wie dein üblicher Kauf, etwa eine Jahreskarte) zählen einmal, werden aber nicht auf die restlichen Tage fortgeschrieben. „Investiert“ zeigt, was bisher investiert wurde; noch anstehende Pläne stehen darunter.
- **Wohin das Geld floss / Vermögen im Zeitverlauf**: Zeitraum 1M, 3M, 6M, 1J oder Alle. Die Zusammenfassung zählt erst ab Beginn deiner Aufzeichnung; davor (gestrichelte Linie) ist es eine Schätzung aus deinen heutigen Positionen zu früheren Kursen.
- **Boxen**: Auf den Titel tippen klappt eine Box ein; **Boxen anordnen** unten auf jeder Seite verschiebt sie. Beides wird pro Gerät gespeichert.

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
- **„Sync problem, see Settings“**: **Einstellungen → Sync zwischen Geräten** nennt den genauen Grund. „Slow down“ ist GitHubs Limit und verschwindet von selbst; „Refused access“ heißt, dem Token fehlt die gist-Berechtigung.
- **Apple-Pay-Zahlungen kommen nicht an**: siehe Abschnitt 2.
- **Nach einem Import stimmt etwas nicht**: den Eintrag auf der Seite Monat öffnen und bearbeiten oder löschen.
- **Demodaten** (**Einstellungen → Backup & Export → Mit Demodaten ansehen**): überschreiben nie deine Daten. Sie fügen Beispiel-Einträge von Januar bis heute hinzu, als Demo markiert, und werden wie jeder Eintrag auf deine anderen Geräte synchronisiert. Solange sie da sind, fließen sie in Budget, Sparquote und Diagramme ein. **Demodaten entfernen** an derselben Stelle löscht genau diese Einträge und stellt Startmonat, Kontosumme und Meilensteine wieder her (für ein paar Sekunden erscheint **Rückgängig**). Ganz ohne Auswirkung auf deine Daten probierst du sie in einem separaten Browser aus (etwa einem Safari-Tab statt der App auf dem Home-Bildschirm), ohne Sync zu verbinden.
- **Alle Daten in diesem Browser löschen** (Einstellungen → Backup & Export) betrifft nur den Browser bzw. die installierte App, in der du es antippst; andere Browser, andere Geräte, deine Sync-Datei und Backups bleiben, wie sie sind.
- **Ein Gerät neu aufsetzen**: zuerst ein Backup unter **Einstellungen → Backup & Export** sichern, später mit **Aus Backup wiederherstellen** einspielen.

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
3. Check every page at desktop width and at phone widths (390 px and 320 px), in light and dark mode. Check that no page scrolls sideways, that no date shows month/day, and that no word is split in the middle (text may only wrap between words or at a hyphen; only codes and addresses may break anywhere).
4. Check that the money-flow diagram balances: everything into "Money in" equals everything out of it.
5. Check that an existing backup still loads (migration).

### Handing back a change

Return the complete updated `index.html`, plus any other changed files, with upload steps. **Every new version adds an entry at the top of `CHANGELOG`** (shown once as "What's new"). **Significant new features also update the tour** (`TOUR_STEPS`, English and German) and, where relevant, the setup help (`SETUP_HELP_EN`, `SETUP_HELP_DE`); small fixes don't. **Every change to the app must come with an updated manual**: edit `MANUAL.md` and the copy embedded in `index.html` (the `MANUAL_MD` constant) together, raise `APP_VERSION` (shown in Settings) and the version line at the top of this manual to the same value. Keep features working that the owner relies on: the importer, the Apple Pay inbox, sync, app lock, the savings-rate goal in the budget, day/month/year dates, and collapsed and arranged boxes.
