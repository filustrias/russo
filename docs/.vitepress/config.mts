import { defineConfig } from 'vitepress'
import { latinizadoNasTabelas } from './theme/latinizado-markdown'

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
      {
        text: 'Pimsleur',
        items: [
          { text: 'Lição 01', link: '/pimsleur_russo_01' },
          { text: 'Lição 02', link: '/pimsleur_russo_02' }
        ]
      }
    ],

    sidebar: [
      {
        text: 'Começo',
        items: [
          { text: 'Início', link: '/' },
          { text: 'O alfabeto cirílico', link: '/alfabeto-cirilico' }
        ]
      },
      {
        text: 'Pimsleur',
        items: [
          { text: 'Lição 01', link: '/pimsleur_russo_01' },
          { text: 'Lição 02', link: '/pimsleur_russo_02' }
        ]
      }
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
