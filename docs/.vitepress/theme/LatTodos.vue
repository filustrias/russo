<script setup lang="ts">
import { latinizado } from './latinizado'
</script>

<template>
  <button
    v-if="latinizado.total.value > 0"
    type="button"
    class="lat-todos"
    @click="latinizado.mostrarTodos(!latinizado.todosVisiveis.value)"
  >
    {{ latinizado.todosVisiveis.value ? 'Ocultar todo o latinizado' : 'Mostrar todo o latinizado' }}
  </button>
</template>
