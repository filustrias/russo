import { defineConfig } from 'vitepress'
import { latinizadoNasTabelas } from './theme/latinizado-markdown'

// Lições do Pimsleur já escritas: basta aumentar este número ao criar a próxima.
const totalLicoes = 10
const licoes = Array.from({ length: totalLicoes }, (_, i) => {
  const n = String(i + 1).padStart(2, '0')
  return { text: `Lição ${n}`, link: `/pimsleur_russo_${n}` }
})

export default defineConfig({
  lang: 'pt-BR',
  title: 'Caderno de russo',
  description: 'Notas de aprendizado da língua russa.',
  base: '/russo/',
  cleanUrls: false,

  head: [
    // Aplica a fonte e o tamanho escolhidos antes da página aparecer, para não piscar.
    ['script', {}, `try{var d=document.documentElement,f=localStorage.getItem('leitura-fonte'),t=localStorage.getItem('leitura-tamanho');if(f)d.dataset.fonte=f;if(t)d.dataset.tamanho=t}catch(e){}`]
  ],

  markdown: {
    config: (md) => md.use(latinizadoNasTabelas)
  },

  themeConfig: {
    nav: [
      { text: 'Alfabeto', link: '/alfabeto-cirilico' },
      { text: 'Pimsleur', items: licoes }
    ],

    sidebar: [
      {
        text: 'Começo',
        items: [
          { text: 'Início', link: '/' },
          { text: 'O alfabeto cirílico', link: '/alfabeto-cirilico' }
        ]
      },
      { text: 'Pimsleur', items: licoes }
    ],

    socialLinks: [{ icon: 'github', link: 'https://github.com/filustrias/russo' }],

    editLink: {
      pattern: 'https://github.com/filustrias/russo/edit/main/docs/:path',
      text: 'Editar esta página no GitHub'
    },

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: 'Buscar', buttonAriaLabel: 'Buscar' },
          modal: {
            displayDetails: 'Mostrar detalhes',
            resetButtonTitle: 'Limpar a busca',
            backButtonTitle: 'Fechar a busca',
            noResultsText: 'Nada encontrado para',
            footer: { selectText: 'abrir', navigateText: 'navegar', closeText: 'fechar' }
          }
        }
      }
    },

    outline: { level: [2, 3], label: 'Nesta página' },
    docFooter: { prev: 'Anterior', next: 'Próxima' },
    darkModeSwitchLabel: 'Aparência',
    lightModeSwitchTitle: 'Mudar para o modo claro',
    darkModeSwitchTitle: 'Mudar para o modo escuro',
    sidebarMenuLabel: 'Capítulos',
    returnToTopLabel: 'Voltar ao topo',
    langMenuLabel: 'Idioma',
    notFound: {
      title: 'Página não encontrada',
      quote: 'Этой страницы нет. Esta página não existe.',
      linkText: 'Voltar ao início'
    }
  }
})
