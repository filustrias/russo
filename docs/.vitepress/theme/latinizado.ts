import { computed, shallowReactive, type Ref } from 'vue'

// Todos os trechos latinizados da página aberta, para o botão "Mostrar todo".
const trechos = shallowReactive(new Set<Ref<boolean>>())

export const latinizado = {
  registrar(visivel: Ref<boolean>) {
    trechos.add(visivel)
  },
  remover(visivel: Ref<boolean>) {
    trechos.delete(visivel)
  },
  total: computed(() => trechos.size),
  todosVisiveis: computed(() => [...trechos].every((v) => v.value)),
  mostrarTodos(visivel: boolean) {
    trechos.forEach((v) => (v.value = visivel))
  }
}
