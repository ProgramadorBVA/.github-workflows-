#!/usr/bin/env python3
"""
Revisa los feeds RSS de canales de YouTube y avisa por Telegram
cuando hay un video nuevo.
"""

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

CHANNELS_FILE = "channels.json"
SEEN_FILE = "seen_videos.json"

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_feed(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Falta TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en las variables de entorno.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def main():
    channels = load_json(CHANNELS_FILE, [])
    seen = load_json(SEEN_FILE, {})

    if not channels:
        print("No hay canales configurados en channels.json")
        return

    for channel in channels:
        channel_id = channel["channel_id"]
        display_name = channel.get("name", channel_id)

        try:
            raw = fetch_feed(channel_id)
        except Exception as e:
            print(f"Error obteniendo feed de {display_name}: {e}")
            continue

        try:
            root = ET.fromstring(raw)
        except Exception as e:
            print(f"Error parseando feed de {display_name}: {e}")
            continue

        entries = root.findall("atom:entry", NS)
        if not entries:
            continue

        seen_ids = set(seen.get(channel_id, []))
        new_seen_ids = list(seen_ids)
        is_first_run = channel_id not in seen

        # Los entries vienen del más nuevo al más viejo
        for entry in reversed(entries):
            video_id_el = entry.find("yt:videoId", NS)
            title_el = entry.find("atom:title", NS)
            link_el = entry.find("atom:link", NS)

            if video_id_el is None or title_el is None or link_el is None:
                continue

            video_id = video_id_el.text
            title = title_el.text
            link = link_el.attrib.get("href", "")

            if video_id in seen_ids:
                continue

            new_seen_ids.append(video_id)

            # En la primera corrida para un canal, solo guardamos lo existente
            # sin mandar notificaciones (para no bombardearte con videos viejos)
            if is_first_run:
                continue

            message = f"🎙️ <b>{display_name}</b> subió un video nuevo:\n\n{title}\n\n{link}"
            print(f"Notificando: {display_name} - {title}")
            send_telegram_message(message)

        seen[channel_id] = new_seen_ids

    save_json(SEEN_FILE, seen)


if __name__ == "__main__":
    main()
