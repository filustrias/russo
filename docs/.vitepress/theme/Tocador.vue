<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
import { audioPimsleur } from './audios'

const props = defineProps<{ unidade: number }>()
const arquivo = computed(() => audioPimsleur(props.unidade))

const audio = ref<HTMLAudioElement>()
const tocando = ref(false)
const esperando = ref(false)
const atual = ref(0)
const duracao = ref(0)
const erro = ref(false)
const velocidades = [0.75, 1, 1.25]
const velocidade = ref(1)

// Guarda onde a pessoa parou em cada lição, para continuar depois.
const chave = computed(() => `audio-posicao-${props.unidade}`)
let ultimaGravada = 0

function ler(): number {
  try {
    return Number(localStorage.getItem(chave.value)) || 0
  } catch {
    return 0
  }
}
function gravar(segundos: number) {
  try {
    localStorage.setItem(chave.value, String(Math.floor(segundos)))
  } catch {}
}

function formatar(s: number) {
  if (!isFinite(s) || s <= 0) return s === 0 ? '0:00' : '--:--'
  const m = Math.floor(s / 60)
  const r = Math.floor(s % 60)
  return `${m}:${String(r).padStart(2, '0')}`
}

function alternar() {
  const a = audio.value
  if (!a) return
  if (a.paused) a.play().catch(() => {})
  else a.pause()
}

function pular(segundos: number) {
  const a = audio.value
  if (!a) return
  const fim = isFinite(a.duration) ? a.duration : Infinity
  a.currentTime = Math.min(Math.max(a.currentTime + segundos, 0), fim)
  atual.value = a.currentTime
}

function buscar(e: Event) {
  const a = audio.value
  if (!a) return
  a.currentTime = Number((e.target as HTMLInputElement).value)
  atual.value = a.currentTime
}

function mudarVelocidade() {
  const i = velocidades.indexOf(velocidade.value)
  velocidade.value = velocidades[(i + 1) % velocidades.length]
  if (audio.value) audio.value.playbackRate = velocidade.value
}

function aoCarregar() {
  const a = audio.value
  if (!a) return
  duracao.value = a.duration
  const salvo = ler()
  if (salvo > 5 && salvo < a.duration - 5) {
    a.currentTime = salvo
    atual.value = salvo
  }
}

function aoAvancar() {
  const a = audio.value
  if (!a) return
  atual.value = a.currentTime
  if (Math.abs(a.currentTime - ultimaGravada) >= 5) {
    ultimaGravada = a.currentTime
    gravar(a.currentTime)
  }
}

function aoTerminar() {
  tocando.value = false
  gravar(0)
}

const rotuloVelocidade = computed(() => String(velocidade.value).replace('.', ',') + '×')

onUnmounted(() => {
  const a = audio.value
  if (a && !a.paused) {
    gravar(a.currentTime)
    a.pause()
  }
})
</script>

<template>
  <div v-if="arquivo" class="tocador" :class="{ 'tocador-com-erro': erro }">
    <audio
      ref="audio"
      :src="arquivo.url"
      preload="metadata"
      @loadedmetadata="aoCarregar"
      @durationchange="duracao = audio?.duration ?? 0"
      @timeupdate="aoAvancar"
      @play="tocando = true"
      @pause="tocando = false"
      @waiting="esperando = true"
      @playing="esperando = false"
      @canplay="esperando = false"
      @ended="aoTerminar"
      @error="erro = true"
    ></audio>

    <template v-if="!erro">
      <button type="button" class="tocador-pular" aria-label="Voltar 15 segundos" title="Voltar 15 segundos" @click="pular(-15)">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z" /></svg>
        <span>15</span>
      </button>
      <button
        type="button"
        class="tocador-play"
        :class="{ 'tocador-esperando': esperando && tocando }"
        :aria-label="tocando ? 'Pausar' : 'Tocar'"
        :title="tocando ? 'Pausar' : 'Tocar'"
        @click="alternar"
      >
        <svg v-if="!tocando" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" /></svg>
        <svg v-else viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" /></svg>
      </button>
      <button type="button" class="tocador-pular" aria-label="Avançar 15 segundos" title="Avançar 15 segundos" @click="pular(15)">
        <span>15</span>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z" /></svg>
      </button>
      <input
        class="tocador-barra"
        type="range"
        min="0"
        :max="duracao || 0"
        step="1"
        :value="atual"
        aria-label="Posição do áudio"
        :aria-valuetext="formatar(atual)"
        @input="buscar"
      />
      <span class="tocador-tempo">{{ formatar(atual) }} / {{ formatar(duracao) }}</span>
      <button type="button" class="tocador-velocidade" title="Velocidade" aria-label="Mudar a velocidade" @click="mudarVelocidade">
        {{ rotuloVelocidade }}
      </button>
    </template>

    <p v-else class="tocador-erro">
      Não consegui carregar o áudio desta lição.
      <a :href="arquivo.drive" target="_blank" rel="noopener">Abrir no Google Drive</a>
    </p>
  </div>
</template>
