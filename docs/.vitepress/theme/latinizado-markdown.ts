import type MarkdownIt from 'markdown-it'

// Nas tabelas com uma coluna chamada "IPA", envolve cada célula dessa
// coluna no componente <Lat>, que deixa o texto encoberto até o clique.
export function latinizadoNasTabelas(md: MarkdownIt) {
  md.core.ruler.push('latinizado-nas-tabelas', (state) => {
    const tokens = state.tokens
    let coluna = -1
    let celula = -1
    let noCorpo = false

    for (let i = 0; i < tokens.length; i++) {
      const tok = tokens[i]
      switch (tok.type) {
        case 'table_open':
          coluna = -1
          noCorpo = false
          break
        case 'tbody_open':
          noCorpo = true
          break
        case 'tr_open':
          celula = -1
          break
        case 'th_open':
          celula++
          if (tokens[i + 1]?.content.trim().toLowerCase() === 'ipa') coluna = celula
          break
        case 'td_open': {
          celula++
          const conteudo = tokens[i + 1]
          if (noCorpo && celula === coluna && conteudo?.type === 'inline' && conteudo.children) {
            const abre = new state.Token('html_inline', '', 0)
            abre.content = '<Lat>'
            const fecha = new state.Token('html_inline', '', 0)
            fecha.content = '</Lat>'
            conteudo.children.unshift(abre)
            conteudo.children.push(fecha)
          }
          break
        }
      }
    }
  })
}
