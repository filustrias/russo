# Prompt: novo caderno de estudos com o framework do "Caderno de russo"

> Como usar: abra o Claude Code na pasta vazia do novo projeto, preencha os campos entre `{{ }}` abaixo e cole tudo a partir de "## Tarefa".

---

## Tarefa

Crie neste diretório um caderno de estudos de **{{LÍNGUA}}** em VitePress, com o mesmo framework, visual e convenções do meu "Caderno de russo". O projeto de referência é público: https://github.com/filustrias/russo (branch `main`; o site publicado é https://filustrias.github.io/russo/).

Dados do novo projeto:

- Título do site: **{{TÍTULO}}** (por exemplo, "Caderno de árabe")
- Autor: **{{AUTOR}}**
- Repositório: **{{URL_DO_REPOSITÓRIO}}** (ex.: `https://github.com/filustrias/arabe2.git`)
- Caminho do site no GitHub Pages: `/{{NOME_DO_REPO}}/`
- Nome da coluna de transliteração: **{{NOME_DA_TRANSLITERAÇÃO}}** (no russo é "Latinizado"; no árabe egípcio poderia ser "Franco")
- Curso das lições: **{{CURSO}}** (ex.: "Pimsleur") e prefixo dos arquivos: **{{PREFIXO}}** (ex.: `pimsleur_arabe`)
- Pasta dos áudios no Google Drive (se houver): {{URL_DA_PASTA_DO_DRIVE}}
- Imagem de abertura: {{ARQUIVO_DA_IMAGEM}}, com a legenda/crédito: {{LEGENDA}}

Antes de começar, clone o repositório de referência numa pasta temporária fora deste projeto e leia `docs/.vitepress/` inteiro. Reaproveite o código de lá em vez de reescrever do zero, adaptando o que for específico do russo. Depois apague a cópia temporária.

## Pilha e publicação

- **VitePress 1.6.x** (versão estável, não a 2.0 alfa), Node, `"type": "module"`.
- Conteúdo em `docs/`; imagens em `docs/imagens/`; tema em `docs/.vitepress/theme/`.
- `base: '/{{NOME_DO_REPO}}/'`, `cleanUrls: false`, `lang: 'pt-BR'`.
- Fontes instaladas por npm com `@fontsource` (nada de CDN em tempo de execução).
- Publicação no branch **`gh-pages`** com o pacote `gh-pages`, sem GitHub Actions. Assim o GitHub ativa o Pages sozinho e não é preciso mexer nas configurações do repositório. Scripts do `package.json`:
  - `dev`: `vitepress dev docs`
  - `build`: `vitepress build docs`
  - `preview`: `vitepress preview docs`
  - `publicar`: `vitepress build docs && gh-pages --dist docs/.vitepress/dist --dotfiles --message "Publica o site"`
- `.gitignore`: `node_modules/`, `docs/.vitepress/dist/`, `docs/.vitepress/cache/`.

## Arquivos do tema (copiar do projeto de referência e adaptar)

| Arquivo | Papel |
|:--|:--|
| `config.mts` | Navegação, barra lateral, busca local, textos da interface em português. As lições entram por uma constante `totalLicoes` que gera o menu (`Lição 01`, `Lição 02`…). Script no `head` aplica a fonte e o tamanho escolhidos antes da página aparecer. |
| `theme/index.ts` | Estende o tema padrão, importa as fontes e o CSS, registra o componente `Lat` e preenche os slots `home-hero-image` (Capa), `doc-before` (BarraAula) e `nav-bar-content-after` (Leitura). |
| `theme/estilo.css` | Toda a identidade visual (ver abaixo). |
| `theme/latinizado-markdown.ts` | Plugin markdown-it: numa tabela cuja coluna se chama "{{NOME_DA_TRANSLITERAÇÃO}}", envolve cada célula dessa coluna em `<Lat>`. Ajuste o nome da coluna procurado. |
| `theme/Lat.vue` | Botão que deixa o texto encoberto (listras) até o clique. Usa `aria-expanded` como string. |
| `theme/latinizado.ts` | Registro compartilhado dos trechos encobertos da página aberta (`shallowReactive(Set)`), para o botão "Mostrar todo". |
| `theme/LatTodos.vue` | Botão "Mostrar/Ocultar todo o {{NOME_DA_TRANSLITERAÇÃO}}". |
| `theme/BarraAula.vue` | Barra presa no alto da lição: tocador de áudio + LatTodos. Lê `unidade` do frontmatter. |
| `theme/Tocador.vue` | Tocador próprio: voltar/avançar 15 s, barra de posição, velocidade 0,75×/1×/1,25×, retomada de onde parou (localStorage, com try/catch). Se o MP3 não puder ser lido direto, troca sozinho pelo player do Google Drive (`/preview` em iframe). |
| `theme/audios.ts` | Mapa número da lição → ID do arquivo no Drive; gera as URLs `drive.usercontent.google.com/download?id=…&export=download`, `/view` e `/preview`. |
| `theme/Leitura.vue` | Botão "Aa" na barra do topo: escolha de fonte do texto e tamanho (A−, A, A+), salvos no navegador. |
| `theme/Capa.vue` | Foto de abertura com legenda de crédito, no slot do hero. |

## Visual

- **Alto contraste.** Claro: fundo creme `#fbf8f1`, texto `#121212`, destaque vermelho `#b3121f`. Escuro: fundo `#0b0b0c`, texto `#f5f1e8`, destaque `#ff5c5c` (botões `#d0202e`). Copie as variáveis `--vp-c-*` do `estilo.css` de referência; troque o vermelho se quiser outra cor de destaque, conferindo o contraste nos dois modos.
- Cabeçalho das tabelas invertido (cor do texto como fundo), bordas fortes, `h2` com fio superior de 2px, sombras "deslocadas" (`3px 3px 0` na cor de destaque) em botões, cartões e foto de abertura.
- **Fontes: escolha fontes que tenham o alfabeto de {{LÍNGUA}}.** No russo usei Golos Text (texto, padrão), PT Serif e Inter como opções do painel "Aa", e Unbounded nos títulos. Para outra escrita, troque por famílias do `@fontsource` que cubram esse alfabeto (por exemplo, para árabe: Cairo, Noto Naskh Arabic, IBM Plex Sans Arabic) e mantenha a regra: título com personalidade, texto confortável, três opções no painel.
- Abertura no layout `home` do VitePress: título, subtítulo na língua estudada, frase curta, dois botões e cartões (features) para as seções. A foto fica no slot do hero.

## Detalhes que já deram problema e a solução

1. **Áudio privado no Drive.** O tocador próprio só lê o MP3 se o arquivo estiver compartilhado como "Qualquer pessoa com o link". Com arquivo privado, o evento `error` do `<audio>` troca para o iframe `https://drive.google.com/file/d/ID/preview`, que toca para quem está logado na conta dona dos arquivos (mas sem ±15 s). Nunca mude o compartilhamento dos arquivos sem me perguntar: os áudios podem ter direitos autorais.
2. **Pular no áudio exige `Range`.** Ao testar com áudio falso, o servidor de teste precisa responder `206` com `Content-Range`; sem isso o navegador volta para 0:00.
3. **Barra presa no celular.** Abaixo de 960px a barra principal do VitePress rola junto e só fica a barra "Capítulos" (48px): use `top: 56px` nessa faixa. Abaixo de 640px, `.barra-aula { display: contents }` para só o tocador ficar preso, e o botão do latinizado rolar com o texto.
4. **Hero no celular.** O VitePress põe margens negativas na imagem do hero; zere com `.VPHero .image { margin: 0 0 40px }` abaixo de 960px, senão a foto cobre o título.
5. **`vitepress preview` guarda a lista de arquivos.** Depois de um novo build, reinicie o preview (ou use outra porta), senão o CSS novo dá 404.
6. **Mensagens de commit no Windows.** O PowerShell 5.1 tira as aspas internas das mensagens; grave a mensagem num arquivo temporário e use `git commit -F arquivo`.

## Convenções de conteúdo

- Cada lição: `docs/{{PREFIXO}}_NN.md` (ex.: `pimsleur_russo_03.md`) com frontmatter `unidade: N` (liga o tocador ao áudio) e as seções, nesta ordem:
  1. `# {{CURSO}} — Lição NN`
  2. `## Diálogo`: uma frase de contexto e a tabela `Quem | {{LÍNGUA}} | {{NOME_DA_TRANSLITERAÇÃO}} | Português`.
  3. `## Conceitos`: parágrafos com rótulo em negrito.
  4. `## Vocabulário`: tabela `{{LÍNGUA}} | {{NOME_DA_TRANSLITERAÇÃO}} | Português`.
  5. `## Exercícios`: cinco itens e as respostas em `::: details Respostas`.
  6. `## Versão informal`: tabela no mesmo formato do diálogo e uma nota curta com as gírias.
- **Transliteração sempre encoberta:** na coluna da tabela (automático) e no texto com `<Lat>…</Lat>`.
- **Explicações:** todo termo da língua estudada vem no formato *termo* (<Lat>transliteração</Lat> - português), com o termo em itálico. Exemplo do russo: *Но* (<Lat>no</Lat> - mas): *Немно́го, но не о́чень хорошо́.* (<Lat>nimnóga, no ni ótchen' kharashó.</Lat> - Um pouco, mas não muito bem.)
- **Nunca usar as aspas « »**, em lugar nenhum. Para citar português, use itálico ou aspas retas.
- Transliteração pensada para quem fala português (no russo: *kh*, *sh*, *tch*, *j*, acento agudo na sílaba tônica, vogais átonas reduzidas). Defina comigo as regras de {{LÍNGUA}} antes da primeira lição e mantenha-as em todas.
- Quando o material de origem não disser quem fala cada linha, deduza pela gramática e pelos nomes, use rótulos neutros (A/B, Passante, Garçom) quando não houver pista, e me avise do que foi deduzido.
- Corrija erros evidentes do material de origem (letras de outro alfabeto, frases truncadas, tradução que não bate) e liste as correções na resposta.

## Forma de trabalhar comigo

- **Sempre que eu pedir algo: faça, dê commit, push e publique** (`npm run publicar`), sem perguntar antes.
- Adicione arquivos ao commit pelo nome. Não faça commit de arquivos que eu não pedi para usar (fontes de texto que eu deixo na raiz, imagens soltas), e me diga que ficaram de fora.
- Antes de publicar, rode o build e teste no navegador: suba o `vitepress preview` e use `puppeteer-core` apontando para o Edge (`C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`), instalado numa pasta temporária fora do projeto. Confira em desktop (1366px) e celular (390px): sem rolagem horizontal, latinizado encoberto, botões funcionando, tocador no lugar certo. Tire capturas e olhe.
- Depois de publicar, espere o deploy e confirme as páginas no site real.
- Guarde as convenções acima na memória do projeto, para valerem nas próximas conversas.
- Responda em português, de forma direta, e no fim diga o que foi feito, o que foi verificado e o que precisa da minha decisão.

## Primeira entrega

1. Projeto VitePress montado com o tema completo, a página de abertura com a imagem e o crédito, e uma página de exemplo com uma lição curta (diálogo de 3 linhas) para eu ver o padrão funcionando.
2. Repositório ligado a {{URL_DO_REPOSITÓRIO}}, primeiro commit no `main`, push e publicação no `gh-pages`.
3. Link do site publicado e a lista do que eu preciso decidir (fontes, cor de destaque, regras de transliteração, compartilhamento dos áudios).
