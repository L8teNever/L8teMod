# Installation via Dockge / Docker

Dieses Repository ist so konfiguriert, dass Images auf Docker Hub gepusht werden.

## Installation

Nutze folgenden Code in **Dockge** oder einer `docker-compose.yml`:

```yaml
version: '3.8'

services:
  twitch_bot:
    image: <DEIN_DOCKERHUB_USERNAME>/l8temod:latest
    container_name: l8temod_bot
    restart: always
    volumes:
      - ./data:/app/data
    ports:
      - "9999:5000"
    environment:
      - TWITCH_CLIENT_ID=
      - TWITCH_CLIENT_SECRET=
      - GEMINI_API_KEY=
      - BOT_NICK=L8teBot
      - CHANNEL_NAME=
```

1. Ersetze `<DEIN_DOCKERHUB_USERNAME>` mit deinem Docker Hub Benutzernamen.
2. Trage deine Environment-Variablen ein.
3. Der Service ist dann unter `http://<DEINE-IP>:9999` erreichbar.
