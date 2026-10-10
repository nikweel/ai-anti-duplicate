# AI Anti-Duplicate

[English](README.md) · [Русский](README.ru.md) · [中文](README.zh.md) · [Español](README.es.md) · [हिन्दी](README.hi.md) · [Português](README.pt.md) · **Français** · [Deutsch](README.de.md) · [日本語](README.ja.md) · [العربية](README.ar.md) · [Bahasa Indonesia](README.id.md) · [Türkçe](README.tr.md)

Outil gratuit et open source qui trouve les photos en double d'après **ce que montre l'image**, et non d'après la taille, la date ou une empreinte. Il utilise l'IA : il reconnaît donc la même photo même réduite, recompressée, légèrement recadrée ou pivotée.

> 🛡️ **Sûr par conception :** le programme ne fait que *copier* des fichiers. Il ne supprime, ne déplace et ne modifie jamais vos originaux.

![](docs/screenshots/main.png)

## Utilisation
1. Choisissez le dossier contenant vos photos (tous les sous-dossiers sont inclus).
2. Choisissez le dossier où seront enregistrées les photos uniques.
3. Choisissez la règle pour les doublons : la plus récente, le plus gros fichier, la plus haute résolution, ou choix manuel pour chaque groupe.
4. Cliquez sur « Trouver les doublons et enregistrer ». Les photos sans doublon sont copiées telles quelles ; pour chaque groupe de doublons, seule(s) celle(s) que vous avez choisie(s).

## Téléchargement (aucune installation de Python)
Téléchargez le fichier correspondant à votre système sur la page [Releases](https://github.com/nikweel/ai-anti-duplicate/releases/latest) :

| Système | Fichier | Comment lancer |
|---|---|---|
| **Windows** | `…-Setup.exe` | Double-clic, puis suivez l'installateur. |
| **Linux** | `….AppImage` / `….deb` | AppImage : clic droit → Propriétés → Autoriser l'exécution comme programme, puis double-clic ; ou `.deb` : double-clic → Installer. |
| **macOS** | `….dmg` | Ouvrez le `.dmg` et glissez l'app dans Applications. |

Au premier lancement, vous choisissez le modèle de reconnaissance dans les Paramètres et le programme le télécharge une seule fois (internet requis). Ensuite, il fonctionne entièrement hors ligne.

## Avertissements du système au premier lancement (c'est normal)
Le programme est gratuit et n'est pas signé par un certificat (ils sont payants), le système peut donc vous avertir. Le code est ouvert et vous pouvez vérifier le téléchargement avec `SHA256SUMS.txt` de la release.

- **Windows :** « Windows a protégé votre ordinateur » → **Informations complémentaires → Exécuter quand même**.
- **macOS :** ouvrez **Réglages Système → Confidentialité et sécurité**, faites défiler et cliquez sur **Ouvrir quand même** à côté de l'app.
- **Linux :** aucun avertissement.

## Fonctionnalités
- Comparaison du contenu des photos par IA (rotation, réduction ou recompression sans effet)
- Trois modèles : léger, moyen et lourd ; accélération par carte graphique
- Vérification manuelle : cochez plusieurs photos à garder, survolez pour agrandir
- Noms dans le dossier de destination : d'origine ou selon la date (EXIF, horodatage), sans jamais écraser
- Inclut tous les sous-dossiers
- 12 langues, thème sombre et clair

## Auteur

Licence [MIT](LICENSE) : gratuit pour tout usage, y compris commercial.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
