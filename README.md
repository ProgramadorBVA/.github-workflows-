# Notificador de podcasts de YouTube a Telegram

Te avisa apenas un canal de YouTube que sigues sube un video nuevo,
mandándote el nombre y el link directo a Telegram. Gratis y sin límite
de canales.

## Paso 1: Crear el repositorio en GitHub

1. Entra a github.com y crea una cuenta si no tienes.
2. Crea un repositorio nuevo, **público**, con cualquier nombre
   (ej: `mis-podcasts`).
3. Sube estos 4 archivos/carpetas manteniendo la misma estructura:
   - `check_podcasts.py`
   - `channels.json`
   - `seen_videos.json`
   - `.github/workflows/check.yml`

   (Puedes arrastrarlos directo en la web de GitHub con el botón
   "Add file" → "Upload files", asegurándote de que `check.yml` quede
   dentro de la carpeta `.github/workflows/`).

## Paso 2: Agregar tus credenciales de Telegram (seguro, encriptado)

1. En tu repositorio, ve a **Settings** → **Secrets and variables** →
   **Actions**.
2. Click en **New repository secret** y crea dos:
   - Nombre: `TELEGRAM_TOKEN` → Valor: el token que te dio @BotFather
   - Nombre: `TELEGRAM_CHAT_ID` → Valor: tu Chat ID (el que te dio
     @userinfobot)

Estos valores quedan encriptados, nadie puede verlos aunque el
repositorio sea público.

## Paso 3: Agregar los canales que quieres seguir

Edita `channels.json` y pon el nombre que quieras mostrar y el
**Channel ID** real de YouTube (no el @usuario, sino el ID que empieza
con `UC...`).

### Cómo conseguir el Channel ID de un canal:
- Entra al canal de YouTube en el navegador.
- Click derecho → "Ver código fuente de la página" (o Ctrl+U).
- Busca (Ctrl+F) `"channelId"` y copia el valor que empieza con `UC`.

  **O más fácil:** usa una página como
  https://commentpicker.com/youtube-channel-id.php — pegas el link del
  canal y te da el ID directo.

Ejemplo de `channels.json` con canales reales:
```json
[
  { "name": "Podcast Perritos Callejeros", "channel_id": "UC1234567890abcdefghij" },
  { "name": "Otro Podcast", "channel_id": "UCabcdefghij1234567890" }
]
```
Puedes agregar tantos canales como quieras, solo sigue el mismo
formato separado por comas.

## Paso 4: Activarlo

1. Ve a la pestaña **Actions** de tu repositorio.
2. Si GitHub te pregunta si quieres habilitar los workflows, dile que sí.
3. Puedes correrlo manualmente la primera vez: pestaña Actions →
   "Revisar podcasts nuevos" → **Run workflow**.
4. Después de eso, corre solo cada 10 minutos, para siempre, gratis.

## Notas importantes

- La **primera vez** que agregues un canal nuevo, el bot NO te va a
  notificar sus videos existentes (para no bombardearte con videos
  viejos). Solo te avisará de los que suban **después** de agregarlo.
- Si quieres agregar o quitar canales después, solo edita
  `channels.json` directo en GitHub (botón del lápiz para editar) y
  guarda los cambios ("Commit changes").
- Si algo no funciona, revisa la pestaña **Actions** → click en la
  corrida más reciente → ahí ves el log de errores.
