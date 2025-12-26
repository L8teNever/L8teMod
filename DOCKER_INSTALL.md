# Installation via Docker (GHCR)

Dieses Repository ist mit GitHub Container Registry (GHCR) verknüpft. Das bedeutet, du kannst das Image direkt herunterladen, ohne es selbst bauen zu müssen.

## Voraussetzung

Du benötigst eine installierte Docker-Umgebung (Docker Desktop oder Docker Engine + Docker Compose).

## Installation & Start

1. **Datei herunterladen**:
   Lade die Datei `docker-compose.deploy.yml` herunter und benenne sie ggf. in `docker-compose.yml` um (oder nutze sie direkt wie unten beschrieben).
   
2. **Setup**:
   Erstelle eine `.env` Datei im gleichen Verzeichnis mit deiner Konfiguration (siehe `.env.example`).
   Stelle sicher, dass ein Ordner `./data` existiert oder von Docker erstellt werden kann.

3. **Starten**:
   Führe folgenden Befehl aus:

   ```bash
   docker-compose -f docker-compose.deploy.yml up -d
   ```

   Dies wird automatisch das neueste Image (`ghcr.io/l8tenever/l8temod:latest`) herunterladen und starten.

## Manuelles Aktualisieren

Um auf die neueste Version zu aktualisieren:

```bash
docker-compose -f docker-compose.deploy.yml pull
docker-compose -f docker-compose.deploy.yml up -d
```
