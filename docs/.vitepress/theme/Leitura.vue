<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

// Preferências de leitura: fonte do texto e tamanho. Ficam salvas no navegador.
const fontes = [
  { id: 'golos', nome: 'Golos', amostra: 'Привет' },
  { id: 'serif', nome: 'PT Serif', amostra: 'Привет' },
  { id: 'inter', nome: 'Inter', amostra: 'Привет' }
]
const tamanhos = [
  { id: 'p', nome: 'A−', rotulo: 'Texto menor' },
  { id: 'm', nome: 'A', rotulo: 'Texto normal' },
  { id: 'g', nome: 'A+', rotulo: 'Texto maior' }
]

const aberto = ref(false)
const fonte = ref('golos')
const tamanho = ref('m')
const raiz = ref<HTMLElement>()

function guardar(chave: string, valor: string) {
  try {
    localStorage.setItem(chave, valor)
  } catch {}
}

function escolherFonte(id: string) {
  fonte.value = id
  document.documentElement.dataset.fonte = id
  guardar('leitura-fonte', id)
}

function escolherTamanho(id: string) {
  tamanho.value = id
  document.documentElement.dataset.tamanho = id
  guardar('leitura-tamanho', id)
}

function fecharFora(e: Event) {
  if (raiz.value && !raiz.value.contains(e.target as Node)) aberto.value = false
}
function fecharEsc(e: KeyboardEvent) {
  if (e.key === 'Escape') aberto.value = false
}

onMounted(() => {
  fonte.value = document.documentElement.dataset.fonte || 'golos'
  tamanho.value = document.documentElement.dataset.tamanho || 'm'
  document.addEventListener('click', fecharFora)
  document.addEventListener('keydown', fecharEsc)
})
onUnmounted(() => {
  document.removeEventListener('click', fecharFora)
  document.removeEventListener('keydown', fecharEsc)
})
</script>

<template>
  <div ref="raiz" class="leitura">
    <button
      type="button"
      class="leitura-botao"
      :aria-expanded="String(aberto)"
      aria-label="Fonte e tamanho do texto"
      title="Fonte e tamanho do texto"
      @click="aberto = !aberto"
    >
      Aa
    </button>
    <div v-if="aberto" class="leitura-painel" role="group" aria-label="Fonte e tamanho do texto">
      <p class="leitura-titulo">Fonte</p>
      <div class="leitura-opcoes">
        <button
          v-for="f in fontes"
          :key="f.id"
          type="button"
          :class="['leitura-opcao', 'fonte-' + f.id]"
          :aria-pressed="String(fonte === f.id)"
          @click="escolherFonte(f.id)"
        >
          <span class="leitura-amostra">{{ f.amostra }}</span>
          <span class="leitura-nome">{{ f.nome }}</span>
        </button>
      </div>
      <p class="leitura-titulo">Tamanho</p>
      <div class="leitura-opcoes">
        <button
          v-for="t in tamanhos"
          :key="t.id"
          type="button"
          class="leitura-opcao"
          :aria-pressed="String(tamanho === t.id)"
          :aria-label="t.rotulo"
          @click="escolherTamanho(t.id)"
        >
          {{ t.nome }}
        </button>
      </div>
    </div>
  </div>
</template>
