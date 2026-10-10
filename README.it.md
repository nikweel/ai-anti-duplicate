# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · **Italiano** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** è un'app gratuita e open source che trova le **foto** duplicate (JPG, PNG, WebP + RAW) in base a **ciò che mostra l'immagine**, non a dimensione, data o hash. Usa l'IA, quindi riconosce lo stesso scatto anche se ridotto, ricompresso, ritagliato un po' o ruotato. Serve solo per raccolte di foto, non per documenti, video o altri file.

> 🛡️ **Sicuro per progetto:** il programma *copia* soltanto i file. Non cancella, non sposta e non modifica mai gli originali.

![](docs/screenshots/main.png)

## Come si usa
1. Scegli la cartella con le tue foto (le sottocartelle sono incluse).
2. Scegli la cartella in cui salvare le foto uniche.
3. Scegli la regola per i duplicati: il più recente, il file più grande, la risoluzione più alta o la scelta manuale per ogni gruppo.
4. Premi «Trova i duplicati e salva». Le foto senza duplicati vengono copiate così come sono; per ogni gruppo di duplicati solo quella (o quelle) che hai scelto.

## Download (non serve installare Python)
Scarica il file per il tuo sistema dalla pagina [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Sistema | File | Come avviarlo |
|---|---|---|
| **Windows** | `…-Setup.exe` | Doppio clic e segui l'installazione guidata. |
| **Linux** | `….AppImage` / `….deb` | AppImage: clic destro → Proprietà → Consenti l'esecuzione come programma, poi doppio clic; oppure `.deb`: doppio clic → Installa. |
| **macOS** | `….dmg` | Apri il `.dmg` e trascina l'app in Applicazioni. |

Al primo avvio scegli il modello di riconoscimento nelle Impostazioni e il programma lo scarica una sola volta (serve internet). Poi funziona del tutto offline.

## Avvisi del sistema al primo avvio (è normale)
Il programma è gratuito e non è firmato con un certificato (sono a pagamento), perciò il sistema può avvisarti. Il codice è aperto e puoi verificare il download con `SHA256SUMS.txt` della release.

- **Windows:** «Windows ha protetto il PC» → **Ulteriori informazioni → Esegui comunque**.
- **macOS:** apri **Impostazioni di Sistema → Privacy e sicurezza**, scorri in basso e premi **Apri comunque** accanto all'app.
- **Linux:** nessun avviso.

## Funzioni
- Confronto del contenuto delle foto con l'IA (rotazione, riduzione o ricompressione non contano)
- Tre modelli: leggero, medio e pesante; accelerazione con la scheda grafica
- Controllo manuale: spunta più foto da salvare e ingrandiscile passandoci sopra
- Nomi nella cartella di destinazione: originali o per data (EXIF, timestamp), senza mai sovrascrivere
- Include tutte le sottocartelle
- 30 lingue, tema scuro e chiaro

## Autore

Licenza [MIT](LICENSE): gratis per qualsiasi uso, anche commerciale.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
