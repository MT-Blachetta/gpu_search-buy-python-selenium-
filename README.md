# GPU Shopping Bot (Python & Selenium)

Dieses Repository enthält verschiedene Skripte, die die Verfügbarkeit von Grafikkarten in deutschen Online-Shops automatisch prüfen und beim Kauf unterstützen. Die Skripte nutzen Selenium oder HTTP-Anfragen mit BeautifulSoup.

## Aufbau

- **`asusBuy.py`** – überwacht den ASUS-Webshop und startet einen vorbereiteten Checkout über PayPal, sobald eine Karte lieferbar ist.
- **`asusNotify.py`** – wie oben, sendet jedoch nur eine SMS-Benachrichtigung über `clx.xms`.
- **`mediamarkt_selenium.py`** – geht eine Liste von MediaMarkt-Produkten durch und führt den Login zum Kauf vor.
- **`mindfactoryNotify.py`** – durchsucht mindfactory.de nach GPUs und benachrichtigt bei passenden Angeboten per SMS.
- **`mindfactoryBuy.py`** – Variante mit automatischer Kaufvorbereitung bei Mindfactory.
- **`futureX_selenium.py`** – Sammlung von Beispiel-Links für weitere Experimente.

## Voraussetzungen

- Python 3
- Google Chrome und ein kompatibler ChromeDriver im Unterordner `chromedriver/`
- Bibliotheken: `selenium`, `beautifulsoup4`, `requests`, `playsound` sowie optional `clx-xms` für SMS-Versand. Installation z.B. mit:

  ```bash
  pip install selenium beautifulsoup4 requests playsound clx-xms
  ```

## Verwendung

1. **Zugangsdaten anpassen** – In den Skripten sind Beispiel-E-Mails, Passwörter und Telefonnummern hinterlegt. Vor dem Einsatz müssen eigene Daten eingetragen werden.
2. **Produktlinks eintragen** – Dateien wie `mediamarkt_links.txt` enthalten die zu überwachenden URLs.
3. **Skript starten** – Beispiel für den ASUS-Bot:

   ```bash
   python asusBuy.py
   ```

   Der Bot öffnet einen Browser, prüft die Verfügbarkeit und meldet sich an. Beim Erreichen des Bezahlvorgangs ertönt ein Signal und das Skript wartet auf eine Eingabe, damit der Kauf manuell bestätigt werden kann.

4. **Benachrichtigungsmodus** – Für reine Hinweise ohne Kauf können `asusNotify.py` oder `mindfactoryNotify.py` ausgeführt werden.

## Hinweis

Die Skripte dienen ausschließlich zu Lern- und Demonstrationszwecken. Automatisierte Bestellungen können gegen die Nutzungsbedingungen der Händler verstoßen. Verwendung auf eigenes Risiko.
