# Einrichtungs-Anleitung für L8teMod

Um den Bot nutzen zu können, benötigst du Zugangsdaten von Twitch und Google (für die KI).

## 1. Twitch App erstellen (Client ID & Secret)

Damit der Bot sich bei Twitch anmelden und Chat-Nachrichten lesen kann, brauchst du eine "Application".

1. Gehe auf die **[Twitch Developer Console](https://dev.twitch.tv/console/apps)**.
2. Melde dich mit deinem Twitch-Account an.
3. Klicke rechts auf **"Register Your Application"**.
4. Fülle das Formular aus:
   - **Name**: Ein eindeutiger Name (z.B. `L8teMod_DeinName`).
   - **OAuth Redirect URLs**: Hier **musst** du die Adresse eintragen, unter der du das Dashboard aufrufst, plus `/callback`.
     - Für lokal: `http://localhost:9999/callback`
     - Wenn du es auf einem Server hast: `http://<DEINE-SERVER-IP>:9999/callback`
   - **Category**: "Chat Bot" auswählen.
   - **Client Type**: "Confidential" ist okay.
   - Klicke auf **"Create"**.
5. Klicke in der Liste auf deine neue App ("Manage").
6. Hier findest du die **Client ID**. Kopiere sie.
7. Klicke bei **Client Secret** auf "New Secret", um eins zu erstellen. Kopiere es sofort (es wird danach nicht mehr angezeigt!).

## 2. Google Gemini API (KI-Funktion)

Für die intelligenten Antworten nutzt der Bot Google Gemini.

1. Gehe zu **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2. Klicke auf **"Create API Key"**.
3. Wähle ein bestehendes Projekt oder "Create API key in new project".
4. Kopiere den Schlüssel, der mit `AIza...` anfängt.

## 3. Konfiguration eintragen

Trage diese Daten nun in deine `.env` Datei oder in Dockge unter "Environment" ein:

- `TWITCH_CLIENT_ID`: Deine ID aus Schritt 1.
- `TWITCH_CLIENT_SECRET`: Dein Secret aus Schritt 1.
- `GEMINI_API_KEY`: Dein Key aus Schritt 2.
- `BOT_NICK`: Der Twitch-Name des Accounts, der posten soll (meist dein eigener oder ein Zweitaccount).
- `CHANNEL_NAME`: Der Name des Kanals, in dem der Bot laufen soll (dein Streamer-Name).
