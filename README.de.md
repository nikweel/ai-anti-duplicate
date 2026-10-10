# AI Anti-Duplicate

[English](README.md) · [Русский](README.ru.md) · [中文](README.zh.md) · [Español](README.es.md) · [हिन्दी](README.hi.md) · [Português](README.pt.md) · [Français](README.fr.md) · **Deutsch** · [日本語](README.ja.md) · [العربية](README.ar.md) · [Bahasa Indonesia](README.id.md) · [Türkçe](README.tr.md)

Kostenloses Open-Source-Werkzeug, das doppelte Fotos anhand ihres **Bildinhalts** findet — nicht nach Dateigröße, Datum oder Hash. Dank KI erkennt es dasselbe Foto auch dann, wenn es verkleinert, neu komprimiert, leicht beschnitten oder gedreht wurde.

> 🛡️ **Sicher durch Design:** Das Programm *kopiert* nur Dateien. Es löscht, verschiebt oder verändert Ihre Originale niemals.

![](docs/screenshots/main.png)

## So geht's
1. Wählen Sie den Ordner mit Ihren Fotos (alle Unterordner werden einbezogen).
2. Wählen Sie den Ordner, in dem die einzigartigen Fotos gespeichert werden.
3. Wählen Sie die Regel für Duplikate: neueste, größte Datei, höchste Auflösung oder manuell für jede Gruppe.
4. Klicken Sie auf „Duplikate finden und speichern“. Fotos ohne Duplikate werden unverändert kopiert, aus jeder Duplikatgruppe nur die von Ihnen gewählte(n).

## Download (kein Python nötig)
Laden Sie die Datei für Ihr System von der Seite [Releases](https://github.com/nikweel/ai-anti-duplicate/releases/latest) herunter:

| System | Datei | Starten |
|---|---|---|
| **Windows** | `…-Setup.exe` | Doppelklick und dem Installationsassistenten folgen. |
| **Linux** | `….AppImage` / `….deb` | AppImage: Rechtsklick → Eigenschaften → Als Programm ausführen erlauben, dann Doppelklick; oder `.deb`: Doppelklick → Installieren. |
| **macOS** | `….dmg` | `.dmg` öffnen und die App in „Programme“ ziehen. |

Beim ersten Start wählen Sie in den Einstellungen das Erkennungsmodell; das Programm lädt es einmalig herunter (Internet nötig). Danach läuft alles offline.

## Systemwarnungen beim ersten Start (völlig normal)
Das Programm ist kostenlos und nicht mit einem Zertifikat signiert (Zertifikate kosten Geld), deshalb kann das System warnen. Der Code ist offen; den Download können Sie mit `SHA256SUMS.txt` aus dem Release prüfen.

- **Windows:** „Der Computer wurde durch Windows geschützt“ → **Weitere Informationen → Trotzdem ausführen**.
- **macOS:** **Systemeinstellungen → Datenschutz & Sicherheit** öffnen, nach unten scrollen und neben der App auf **Trotzdem öffnen** klicken.
- **Linux:** keine Warnungen.

## Funktionen
- KI-Vergleich des Foto-Inhalts (Drehen, Verkleinern, Neukomprimieren stört nicht)
- Drei Modelle: leicht, mittel und schwer; Beschleunigung per Grafikkarte
- Manuelle Prüfung: mehrere Fotos zum Speichern anhaken, per Mauszeiger vergrößern
- Dateinamen im Zielordner: original oder nach Datum (EXIF, Zeitstempel), nie überschreiben
- Alle Unterordner einbezogen
- 12 Sprachen, dunkles und helles Design

## Autor

[MIT](LICENSE)-Lizenz: kostenlos für jede Nutzung, auch kommerziell.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
