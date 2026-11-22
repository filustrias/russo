// Áudios do Pimsleur Russian 1 no Google Drive (pasta "Russian1_UXX_Lesson.mp3").
// Para tocar no site, os arquivos precisam estar compartilhados como
// "Qualquer pessoa com o link".
const ids: Record<number, string> = {
  1: '1C14_iksPhjV7naAl7SsrXq8VK8kF_yzJ',
  2: '1kUV8eBAtaEUxPOqTMXeDOQnokysB6lD9',
  3: '14g0M4-OVf203lVlk7lxSv1Pn7f_JfXAd',
  4: '1BLm0UqviOv1iNzZsw8Vzk1fMAkQZj6Fj',
  5: '17MQ5zjBVtW1xm9u0g3MNMPKNQxnp7kjY',
  6: '1XWV3g2-02IfxL1kSDdO48XWN58gXad5w',
  7: '11TuNToCsR0DW_xU26BQsjxiaTO8Dqrer',
  8: '1P8-okhriNN9KfPD6xDR0OhZuoHxSZvl7',
  9: '1FdRKin8QsOpA2_apSpt_F2dfdi9N22Ll',
  10: '1_uUOptUmkwj5jvcdlEpVGse8RopjGruZ',
  11: '1Nh4OgeK9MmYhwGuyvtHu2gm3XBsFnQ1W',
  12: '19l-SufsK6GDldkYxwGmAZyMsbnjImI55',
  13: '1AarRSx0YxOPH1CLgUaX8lS4-RCrfUfLF',
  14: '1I0rIqe-I9ClPgZp3AXOSGLmqnCYKHvQk',
  15: '1BoJH76Me47gkYA-39G3C96tAauqWTer9',
  16: '1gQGIfvGjgonu_RcaQJgAx60rKbNZoDxW',
  17: '1R5PDcyb5lZW6GMzs8XemegDErVFJCDvX',
  18: '1Smes9KbHojxAtacI3ZDfmUVVR0Q0LNcT',
  19: '1zXZvv1832nAp5VxF0VY9HV0SUt7Ihg6p',
  20: '1F5zOxaNeS0sx6RC46nKU9VJhyQLv-ZbA',
  21: '1u5kD_ZkYK2HtQkGg3S45CjPX1ZtueegO',
  22: '1P95Ql8A_Ic0FDg8EHrdVD0tas66rqDVe',
  23: '16IGt7iI1bn9aKBGFP72zUyl8ZUUyRnes',
  24: '1JE9U7sDFeDxZs8Jeh9zBp2bpzbUKU3y4',
  25: '1h-YpBSlwHSIBcuXYcmRPoxV1vWThZHo2',
  26: '1pMvBdC8Zvcg4mPQlH94Dqtr-dUfsyZX0',
  27: '156bMr75hNMvKuqoNnpE6rWL3phIfxX94',
  28: '1oiQBbLeagXxqJ_s7YIaOlGKRPb8g9jeH',
  29: '1p09Cnk6aYuQVrgRqMdwZIkqILQ-g79dN',
  30: '10CXDYz3iytGLMMREKVawl_ryv97C5QQT'
}

export function audioPimsleur(unidade: number) {
  const id = ids[unidade]
  if (!id) return null
  return {
    url: `https://drive.usercontent.google.com/download?id=${id}&export=download`,
    drive: `https://drive.google.com/file/d/${id}/view`
  }
}
