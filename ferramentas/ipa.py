"""Russo acentuado (com U+0301 na vogal tônica) -> IPA, no estilo do Wiktionary,
sem a ligadura das africadas (ts, tɕ), que as fontes web não trazem."""
import re
import unicodedata

AC = '́'
GR = '̀'  # tônica automática (monossílabo sem acento)
VOG = 'аеёиоуыэюя'
SUAVIZA = 'еёиюяь'
CONS = {
    'б': 'b', 'в': 'v', 'г': 'ɡ', 'д': 'd', 'ж': 'ʐ', 'з': 'z', 'й': 'j', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'ф': 'f',
    'х': 'x', 'ц': 'ts', 'ч': 'tɕ', 'ш': 'ʂ', 'щ': 'ɕː',
}
SEMPRE_DURA = set('жшц')
SEMPRE_MOLE = set('чщй')
SONORA = {'b': 'p', 'v': 'f', 'ɡ': 'k', 'd': 't', 'z': 's', 'ʐ': 'ʂ', 'ɣ': 'x', 'dz': 'ts', 'dʑ': 'tɕ', 'ʑː': 'ɕː'}
SURDA = {v: k for k, v in SONORA.items()}
SURDA['x'] = 'ɣ'

PROCLITICOS = {'без', 'в', 'во', 'до', 'для', 'за', 'из', 'изо', 'к', 'ко', 'на', 'над', 'о', 'об', 'обо',
               'от', 'по', 'под', 'при', 'про', 'с', 'со', 'у', 'не', 'ни'}
ENCLITICOS = {'же', 'ж', 'ли', 'ль', 'бы', 'б'}
SUFIXOS_HIFEN = {'то', 'нибудь', 'либо', 'ка', 'таки'}
SEM_OGO = {'много', 'немного', 'строго', 'дорого', 'долго', 'недолго', 'ого', 'убого', 'нестрого', 'намного'}


def sem_acento(s):
    return s.replace(AC, '').replace(GR, '')


def ortografia(p):
    """Ajustes de grafia para a pronúncia, preservando o acento."""
    b = sem_acento(p)
    A = '[' + AC + GR + ']?'

    def sub(pad, rep, s):
        # o padrão é escrito sem acento; aceita acento depois de cada letra
        rx = ''.join(re.escape(c) + A if c.isalpha() else c for c in pad)
        return re.sub(rx, rep, s)

    if b in ('что', 'чтобы', 'чтоб'):
        p = 'ш' + p[1:]
    if b in ('конечно', 'скучно', 'нарочно'):
        p = p.replace('чн', 'шн')
    if b.startswith('пожалуйст'):
        p = re.sub('луйст', 'луст', p)
    if b.startswith('сегодня'):
        p = p.replace('г', 'в', 1)
    if re.search('[ое]го$', b) and b not in SEM_OGO and len([c for c in b if c in VOG]) > 1:
        i = p.rfind('г')
        p = p[:i] + 'в' + p[i + 1:]
    if b == 'его':
        p = p.replace('г', 'в')
    p = re.sub('ть?ся$', 'ца', p)
    if b == 'сейчас':
        p = p.replace('сей', 'си')
    p = p.replace('стьд', 'зьд')
    for pad, rep in [('вств', 'ств'), ('стн', 'сн'), ('здн', 'зн'), ('солнц', 'сонц'), ('сч', 'щ'), ('зч', 'щ'),
                     ('жч', 'щ'), ('дц', 'ц'), ('тц', 'ц'), ('гк', 'хк'), ('гч', 'хч'), ('сш', 'шш'), ('зш', 'шш'),
                     ('сж', 'жж'), ('зж', 'жж')]:
        p = sub(pad, rep, p)
    p = re.sub('[тд]с(?!я)', 'ц', p)
    return p


class Seg:
    def __init__(self, kind, ph='', soft=False, stress=False, letter='', ctx='', final=False):
        self.kind, self.ph, self.soft, self.stress = kind, ph, soft, stress
        self.letter, self.ctx, self.final = letter, ctx, final


def palavra_fon(texto):
    """texto: palavra fonológica, partes separadas por '|'. Devolve lista de Seg (C, V, B=fronteira)."""
    segs = []
    s = texto
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '|':
            segs.append(Seg('B'))
            i += 1
            continue
        if c in CONS:
            nxt = s[i + 1] if i + 1 < n else ''
            soft = (c in SEMPRE_MOLE) or (c not in SEMPRE_DURA and nxt != '' and nxt in SUAVIZA)
            segs.append(Seg('C', CONS[c], soft, letter=c))
            i += 1
            continue
        if c in 'ьъ':
            nxt = s[i + 1] if i + 1 < n else ''
            if nxt != '' and nxt in 'еёюяи':
                segs.append(Seg('C', 'j', True, letter='J'))
            i += 1
            continue
        if c in VOG:
            marca = s[i + 1] if i + 1 < n else ''
            stress = marca in (AC, GR) and marca != '' or c == 'ё'
            auto = marca == GR
            prev = segs[-1] if segs else None
            if prev is None or prev.kind == 'V' or (prev.kind == 'B'):
                # início, depois de vogal ou de fronteira
                antes = None
                for sg in reversed(segs):
                    if sg.kind != 'B':
                        antes = sg
                        break
                if c in 'еёюя':
                    segs.append(Seg('C', 'j', True, letter='J'))
                    ctx = 'mole'
                elif c == 'и' and prev is not None and prev.kind == 'B' and antes is not None and antes.kind == 'C' and not antes.soft:
                    ctx = 'dura'
                else:
                    ctx = 'inicio' if prev is None or (prev.kind == 'B' and antes is None) else ('vogal' if (antes and antes.kind == 'V') else ('dura' if antes and not antes.soft else 'mole'))
            elif prev.kind == 'C':
                if prev.letter in SEMPRE_DURA:
                    ctx = 'chiante'
                elif prev.soft:
                    ctx = 'mole'
                else:
                    ctx = 'dura'
            else:
                ctx = 'dura'
            v = Seg('V', '', stress=stress, letter=c, ctx=ctx)
            v.auto = auto
            segs.append(v)
            i += 1
            continue
        if c in (AC, GR):
            i += 1
            continue
        if c == '-':
            segs.append(Seg('B'))
            i += 1
            continue
        raise ValueError(f'letra inesperada {c!r} em {texto!r}')
    return segs


def vogais(segs):
    vs = [k for k, sg in enumerate(segs) if sg.kind == 'V']
    tonicas = [k for k in vs if segs[k].stress]
    t = tonicas[0] if tonicas else None
    if len(tonicas) > 1:
        # mais de uma tônica (palavras compostas): todas valem
        pass
    # vogal final absoluta
    ultimo = max([k for k, sg in enumerate(segs) if sg.kind != 'B'], default=-1)
    for idx, k in enumerate(vs):
        sg = segs[k]
        L, ctx = sg.letter, sg.ctx
        nxt = next((x for x in segs[k + 1:] if x.kind != 'B'), None)
        antes_mole = nxt is not None and nxt.kind == 'C' and (nxt.soft or nxt.ph in ('tɕ', 'ɕː', 'j'))
        final = k == ultimo
        if sg.stress:
            if L in 'аяо' and L != 'о' or L == 'а':
                ph = 'æ' if ctx == 'mole' and antes_mole else 'a'
            elif L in 'ё':
                ph = 'ɵ' if ctx == 'mole' else 'o'
            elif L == 'о':
                ph = 'ɵ' if ctx == 'mole' else 'o'
            elif L in 'ую':
                ph = 'ʉ' if ctx == 'mole' and antes_mole else 'u'
            elif L == 'е':
                ph = 'ɛ' if ctx in ('chiante', 'dura') else 'e'
            elif L == 'э':
                ph = 'ɛ'
            elif L == 'и':
                ph = 'ɨ' if ctx in ('chiante', 'dura') else 'i'
            elif L == 'ы':
                ph = 'ɨ'
            if L == 'я' and ctx == 'mole' and antes_mole:
                ph = 'æ'
        else:
            pretonica = t is not None and any(segs[j].stress for j in vs[idx + 1:idx + 2])
            if L in 'уюё' and L != 'ё':
                ph = 'ʊ'
            elif L == 'ы':
                ph = 'ɨ'
            elif ctx in ('mole',):
                if L in 'яа' and final:
                    ph = 'ə'
                else:
                    ph = 'ɪ'
            elif ctx == 'chiante':
                if L in 'ао':
                    ph = 'ɐ' if pretonica else 'ə'
                else:
                    ph = 'ɨ'
            else:  # dura, inicio, vogal
                if L in 'ао':
                    ph = 'ɐ' if (pretonica or ctx in ('inicio', 'vogal')) else 'ə'
                elif L == 'и':
                    ph = 'ɪ' if ctx in ('inicio', 'vogal') else 'ɨ'
                elif L == 'э':
                    ph = 'ɪ' if ctx in ('inicio', 'vogal') else 'ɨ'
                elif L in 'ея':
                    ph = 'ɪ'
                else:
                    ph = 'ə'
        sg.ph = ph
    return segs


def assimilacoes(segs):
    cs = segs
    for k, sg in enumerate(cs):
        if sg.kind != 'C':
            continue
        nxt = cs[k + 1] if k + 1 < len(cs) else None
        if nxt is None or nxt.kind != 'C':
            continue
        if sg.letter in 'сз' and nxt.soft and nxt.letter in 'тдн':
            sg.soft = True
        if sg.letter == 'н' and nxt.letter in 'чщ':
            sg.soft = True


def ipa_c(sg):
    ph = sg.ph
    if ph == 'l':
        return 'lʲ' if sg.soft else 'ɫ'
    if sg.soft and ph not in ('j', 'tɕ', 'ɕː', 'ʑː', 'dʑ'):
        return ph + 'ʲ'
    return ph


OBSTR = set(SONORA) | set(SURDA)


def vozeamento(itens):
    """itens: Seg e marcadores ('W' fronteira de palavra, 'P' pausa). Da direita para a esquerda."""
    prox, cruzou = 'pausa', False
    for k in range(len(itens) - 1, -1, -1):
        it = itens[k]
        if it == 'P':
            prox, cruzou = 'pausa', False
            continue
        if it == 'W':
            cruzou = True
            continue
        if it.kind == 'B':
            continue
        if it.kind == 'V' or it.ph not in OBSTR:
            prox, cruzou = 'son', False
            continue
        ph = it.ph
        if prox == 'pausa' or cruzou or prox == 'surda':
            ph = SONORA.get(ph, ph)
        elif prox == 'sonora':
            ph = SURDA.get(ph, ph)
        it.ph = ph
        if it.letter == 'в' and ph == 'v':
            prox = 'son'
        else:
            prox = 'sonora' if ph in SONORA else 'surda'
        cruzou = False
    return itens


def ataque_valido(b):
    if len(b) == 1:
        return True
    if b[0] in ('s', 'z', 'ʂ', 'ʐ'):
        return ataque_valido(b[1:]) or len(b) == 2
    if len(b) == 2 and b[0] not in ('m', 'n', 'ɫ', 'l', 'r', 'j') and b[1] in ('r', 'ɫ', 'l', 'v'):
        return True
    return b == ['m', 'n']


def silaba_tonica(saida):
    """saida: lista de (tipo, texto, tônica); tipo C, Cc (й, sempre coda), V ou ' '. Põe ˈ antes do ataque."""
    res = [[tp, tx, ton, ''] for tp, tx, ton in saida]
    son = ('m', 'n', 'ɫ', 'l', 'r')
    sib = ('s', 'z', 'ʂ', 'ʐ')
    for k, item in enumerate(res):
        if item[0] != 'V' or not item[2]:
            continue
        j = k - 1
        cl = []
        while j >= 0 and res[j][0] in ('C', 'Cc'):
            cl.append(j)
            j -= 1
        cl.reverse()
        inicio = j < 0 or res[j][0] == ' '
        if not inicio:
            while cl and res[cl[0]][0] == 'Cc':
                cl = cl[1:]
        if not cl:
            pos = k
        elif inicio or len(cl) == 1:
            pos = cl[0]
        else:
            b = [res[x][1].replace('ʲ', '').replace('ː', '') for x in cl]
            pos = cl[-1]
            for ini in range(len(cl)):
                if ataque_valido(b[ini:]):
                    pos = cl[ini]
                    break
        res[pos][3] = 'ˈ'
    return ''.join(p + tx for tp, tx, ton, p in res)


TOKEN = re.compile(r"[а-яё́]+(?:-[а-яё́]+)*|\s+|[^а-яё́\s]+", re.I)


def converter(frase, avisos=None):
    if avisos is None:
        avisos = []
    texto = unicodedata.normalize('NFD', frase.lower())
    texto = unicodedata.normalize('NFC', texto)  # й e ё voltam a ser letras; o acento fica solto
    texto = texto.replace('й', 'й').replace('ё', 'ё')
    toks = TOKEN.findall(texto)
    # agrupa em palavras fonológicas
    grupos = []  # cada grupo: ('PAL', [partes]) ou ('ESP', txt) ou ('PON', txt)
    for t in toks:
        if re.match(r'[а-яё]', t, re.I):
            partes = t.split('-')
            grupos.append(['PAL', partes])
        elif t.isspace():
            grupos.append(['ESP', t])
        else:
            grupos.append(['PON', t])
    # junta clíticos
    fon = []
    k = 0
    while k < len(grupos):
        g = grupos[k]
        if g[0] != 'PAL':
            fon.append(g)
            k += 1
            continue
        partes = list(g[1])
        # proclítico: palavra inteira na lista e seguida de espaço + palavra
        while sem_acento(partes[-1]) in PROCLITICOS and AC not in partes[-1] and len(partes) == 1 \
                and k + 2 < len(grupos) and grupos[k + 1][0] == 'ESP' and grupos[k + 2][0] == 'PAL':
            partes = partes + ['␣'] + list(grupos[k + 2][1])
            k += 2
        # proclítico dentro do hífen (по-ру́сски)
        fon.append(['PAL', partes])
        k += 1
    # enclíticos: palavra seguinte na lista se liga à anterior
    final = []
    for g in fon:
        if g[0] == 'PAL' and len(g[1]) == 1 and sem_acento(g[1][0]) in ENCLITICOS and len(final) >= 2 \
                and final[-1][0] == 'ESP' and final[-2][0] == 'PAL':
            final.pop()
            final[-1][1] = final[-1][1] + ['␣'] + g[1]
            continue
        final.append(g)
    # converte
    itens = []
    estrutura = []
    for g in final:
        if g[0] == 'ESP':
            itens.append('W')
            estrutura.append(('ESP', ' '))
            continue
        if g[0] == 'PON':
            itens.append('P')
            estrutura.append(('PON', g[1]))
            continue
        partes = g[1]
        # acento: partes sem acento e com uma vogal, que não são clíticos, ganham tônica
        novas = []
        for idx, p in enumerate(partes):
            if p == '␣':
                novas.append(p)
                continue
            b = sem_acento(p)
            nv = len([c for c in b if c in VOG])
            clitico = (b in PROCLITICOS and idx + 1 < len(partes)) or (b in ENCLITICOS and idx > 0) or \
                      (b in SUFIXOS_HIFEN and idx > 0)
            if AC not in p and 'ё' not in p and not clitico:
                if nv == 1:
                    p = re.sub(f'([{VOG}])', lambda m: m.group(1) + '̀', p, count=1)
                elif nv > 1:
                    avisos.append(p)
            novas.append(ortografia(p))
        texto_fon = '|'.join(x for x in novas if x != '␣')
        # marca onde há espaço (␣) vs hífen; tudo vira espaço na saída
        segs = palavra_fon(texto_fon)
        vogais(segs)
        assimilacoes(segs)
        # gêmeas: dentro da parte, consoantes iguais seguidas
        limp = []
        for sg in segs:
            if limp and sg.kind == 'C' and limp[-1].kind == 'C' and limp[-1].ph == sg.ph and sg.ph != 'j':
                limp[-1].gem = True
                limp[-1].soft = sg.soft
                continue
            limp.append(sg)
        segs = limp
        itens.extend(segs)
        estrutura.append(('PAL', segs))
    vozeamento(itens)
    # monta texto
    out = []
    for tp, val in estrutura:
        if tp != 'PAL':
            out.append(val)
            continue
        segs = val
        nv = len([s for s in segs if s.kind == 'V'])
        explicita = any(s.kind == 'V' and s.stress and not getattr(s, 'auto', False) for s in segs)
        saida = []
        for k, sg in enumerate(segs):
            if sg.kind == 'B':
                saida.append((' ', ' ', False))
            elif sg.kind == 'C':
                ph = ipa_c(sg)
                if getattr(sg, 'gem', False):
                    entre_vogais = k > 0 and segs[k - 1].kind == 'V' and k + 1 < len(segs) and segs[k + 1].kind == 'V'
                    tonica_antes = k > 0 and segs[k - 1].stress
                    if entre_vogais and (tonica_antes or sg.ph in ('ʐ', 'ʂ')) and not ph.endswith('ː'):
                        ph = ph + 'ː'
                saida.append(('Cc' if sg.letter == 'й' else 'C', ph, False))
            else:
                marca = sg.stress and nv > 1 and (explicita is False or not getattr(sg, 'auto', False))
                saida.append(('V', sg.ph, marca))
        out.append(silaba_tonica(saida))
    r = ''.join(out)
    r = r.replace('ʐʐ', 'ʐː').replace('ʂʂ', 'ʂː').replace('dʲdʲ', 'dʲː')
    return r


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for f in sys.argv[1:]:
        print(f, '→', converter(f))
