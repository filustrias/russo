import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'

import '@fontsource/golos-text/400.css'
import '@fontsource/golos-text/500.css'
import '@fontsource/golos-text/600.css'
import '@fontsource/golos-text/700.css'
import '@fontsource/pt-serif/400.css'
import '@fontsource/pt-serif/400-italic.css'
import '@fontsource/pt-serif/700.css'
import '@fontsource/pt-serif/700-italic.css'
import '@fontsource-variable/inter'
import '@fontsource-variable/inter/wght-italic.css'
import '@fontsource-variable/unbounded'
import '@fontsource/charis-sil/latin-400.css'
import '@fontsource/charis-sil/latin-ext-400.css'
import './estilo.css'

import Lat from './Lat.vue'
import BarraAula from './BarraAula.vue'
import Leitura from './Leitura.vue'
import Capa from './Capa.vue'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'home-hero-image': () => h(Capa),
      'doc-before': () => h(BarraAula),
      'nav-bar-content-after': () => h(Leitura)
    })
  },
  enhanceApp({ app }) {
    app.component('Lat', Lat)
  }
} satisfies Theme
