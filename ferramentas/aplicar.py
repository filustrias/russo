"""Preenche a pronúncia IPA do caderno a partir do russo acentuado.

Uso: python ferramentas/aplicar.py docs/pimsleur_russo_*.md
- Em tabelas com as colunas "Russo" e "Latinizado", refaz cada célula Latinizado.
- No texto, refaz cada *Русский* (<Lat>...</Lat> - português) a partir do russo em itálico.
Escreva o russo sempre com o acento tônico (´); monossílabos dispensam.
O alfabeto usa a coluna "Exemplo": processar('docs/alfabeto-cirilico.md', 'Exemplo').
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent))
from ipa import converter

LATIM = re.compile(r'[A-Za-z]')


def ipa(ru, onde, avisos):
    limpo = ru.replace('**', '').replace('*', '').strip()
    if LATIM.search(limpo):
        avisos.append(f'{onde}: latim no russo: {limpo!r}')
    av = []
    r = converter(limpo, av)
    for a in av:
        avisos.append(f'{onde}: sem acento: {a}')
    r = r.strip()
    if r.endswith('.') and not r.endswith('…'):
        r = r[:-1].rstrip()
    return '[' + r + ']'


def celulas(linha):
    return [c.strip() for c in linha.strip().strip('|').split('|')]


def processar(caminho, coluna_origem='Russo'):
    avisos = []
    linhas = Path(caminho).read_text(encoding='utf-8').split('\n')
    i = 0
    while i < len(linhas):
        l = linhas[i]
        if l.startswith('|') and i + 1 < len(linhas) and re.match(r'^\|[\s:|-]+\|$', linhas[i + 1]):
            cab = celulas(l)
            if 'Latinizado' in cab and coluna_origem in cab:
                a, b = cab.index(coluna_origem), cab.index('Latinizado')
                j = i + 2
                while j < len(linhas) and linhas[j].startswith('|'):
                    cs = celulas(linhas[j])
                    cs[b] = ipa(cs[a], f'{Path(caminho).name}:{j + 1}', avisos)
                    linhas[j] = '| ' + ' | '.join(cs) + ' |'
                    j += 1
                i = j
                continue
        i += 1
    texto = '\n'.join(linhas)

    def troca(m):
        return f'*{m.group(1)}* (<Lat>{ipa(m.group(1), Path(caminho).name, avisos)}</Lat>'

    texto = re.sub(r'\*([^*\n]+?)\*\s*\(<Lat>(.*?)</Lat>', troca, texto)
    sobra = [m for m in re.findall(r'<Lat>(.*?)</Lat>', texto) if not m.startswith('[')]
    for s in sobra:
        avisos.append(f'{Path(caminho).name}: <Lat> sem russo em itálico: {s!r}')
    Path(caminho).write_text(texto, encoding='utf-8')
    return avisos


if __name__ == '__main__':
    todos = []
    for c in sys.argv[1:]:
        todos += processar(c)
    for a in todos:
        print(a)
    print('avisos:', len(todos))
