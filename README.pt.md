# AI Anti-Duplicate

[English](README.md) · [Русский](README.ru.md) · [中文](README.zh.md) · [Español](README.es.md) · [हिन्दी](README.hi.md) · **Português** · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [العربية](README.ar.md) · [Bahasa Indonesia](README.id.md) · [Türkçe](README.tr.md)

Ferramenta gratuita e de código aberto que encontra fotos duplicadas pelo **conteúdo da imagem**, e não por tamanho, data ou hash. Usa IA, por isso reconhece a mesma foto mesmo reduzida, recomprimida, levemente cortada ou girada.

> 🛡️ **Seguro por projeto:** o programa apenas *copia* arquivos. Nunca apaga, move nem altera suas fotos originais.

![](docs/screenshots/main.png)

## Como usar
1. Escolha a pasta com suas fotos (todas as subpastas são incluídas).
2. Escolha a pasta onde as fotos únicas serão salvas.
3. Escolha a regra para duplicatas: a mais recente, o maior arquivo, a maior resolução ou escolher manualmente em cada grupo.
4. Clique em «Encontrar duplicatas e salvar». Fotos sem duplicatas são copiadas como estão e, de cada grupo de duplicatas, apenas a(s) que você escolher.

## Download (não é preciso instalar o Python)
Baixe o arquivo do seu sistema na página de [Releases](https://github.com/nikweel/ai-anti-duplicate/releases/latest):

| Sistema | Arquivo | Como executar |
|---|---|---|
| **Windows** | `…-Setup.exe` | Clique duas vezes e siga o instalador. |
| **Linux** | `….AppImage` / `….deb` | AppImage: clique direito → Propriedades → Permitir executar como programa, depois clique duas vezes; ou `.deb`: clique duas vezes → Instalar. |
| **macOS** | `….dmg` | Abra o `.dmg` e arraste o app para Aplicativos. |

Na primeira execução você escolhe o modelo de reconhecimento em Configurações e o programa o baixa uma única vez (é preciso internet). Depois funciona totalmente offline.

## Avisos do sistema na primeira execução (é normal)
O programa é gratuito e não tem assinatura de código (certificados são pagos), por isso o sistema pode avisar. O código é aberto e você pode conferir o download com o `SHA256SUMS.txt` da release.

- **Windows:** «O Windows protegeu o seu PC» → **Mais informações → Executar assim mesmo**.
- **macOS:** abra **Ajustes do Sistema → Privacidade e Segurança**, role até o fim e clique em **Abrir Mesmo Assim** ao lado do app.
- **Linux:** sem avisos.

## Recursos
- Comparação de fotos por conteúdo com IA (girar, reduzir ou recomprimir não atrapalha)
- Três modelos: leve, médio e pesado; com aceleração pela placa de vídeo
- Revisão manual: marque várias fotos para salvar e amplie passando o cursor
- Nomes na pasta de destino: originais ou por data (EXIF, timestamp), sem nunca sobrescrever
- Inclui todas as subpastas
- 12 idiomas, tema escuro e claro

## Autor

Licença [MIT](LICENSE): gratuito para qualquer uso, inclusive comercial.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
