#!/usr/bin/env python3
"""Gera o caderno (Parte A) e o gabarito comentado (Parte B) do simulado
a partir dos arquivos-fonte desta pasta e valida as regras de montagem.

Uso: python3 build.py            (gera os arquivos e imprime o relatório)
     python3 build.py --check    (só valida, sem gravar)

ATENÇÃO: os arquivos-fonte contêm o gabarito.
"""
import glob
import itertools
import os
import re
import statistics
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.dirname(BASE)
LETRAS = "ABCDE"
ESTRUTURA = [
    (1, 25, "Língua Portuguesa"),
    (26, 30, "Raciocínio Lógico-Matemático"),
    (31, 35, "Realidade do Paraná"),
    (36, 60, "Tecnologia (Informática)"),
    (61, 70, "Ciências Forenses"),
    (71, 75, "Contabilidade"),
    (76, 80, "Estatística"),
    (81, 85, "Legislação Estadual e Institucional"),
    (86, 88, "Direito Penal"),
    (89, 91, "Direito Processual Penal"),
    (92, 94, "Direito Constitucional"),
    (95, 97, "Direito Administrativo"),
    (98, 100, "Direitos Humanos"),
]
PROIBIDAS = re.compile(
    r"todas as anteriores|nenhuma das anteriores|alternativa [A-E]\b|letra [A-E]\b"
    r"|opção anterior|opção seguinte|item anterior",
    re.IGNORECASE,
)


def materia_esperada(n):
    for ini, fim, nome in ESTRUTURA:
        if ini <= n <= fim:
            return nome
    raise ValueError(n)


def ler_fontes():
    textos, questoes = {}, {}
    for caminho in sorted(glob.glob(os.path.join(BASE, "*.txt"))):
        atual, secao = None, None
        for bruta in open(caminho, encoding="utf-8"):
            linha = bruta.rstrip("\n")
            if linha.startswith("@@texto "):
                atual = {"tipo": "texto", "id": linha.split()[1], "corpo": []}
                continue
            if linha.startswith("@@q "):
                atual = {"tipo": "q", "n": int(linha.split()[1]), "secoes": {}}
                secao = None
                continue
            if linha == "@@fim":
                if atual["tipo"] == "texto":
                    corpo = atual["corpo"]
                    atual["titulo"] = corpo[0].split(":", 1)[1].strip()
                    atual["corpo"] = "\n".join(corpo[1:]).strip()
                    textos[atual["id"]] = atual
                else:
                    q = atual
                    for k, v in q["secoes"].items():
                        q["secoes"][k] = "\n".join(v).strip()
                    if q["n"] in questoes:
                        raise SystemExit(f"Questão {q['n']} duplicada")
                    questoes[q["n"]] = q
                atual = None
                continue
            if atual is None:
                continue
            if atual["tipo"] == "texto":
                atual["corpo"].append(linha)
            elif linha.startswith(">"):
                secao = linha[1:].strip()
                atual["secoes"][secao] = []
            elif secao is None:
                if linha.strip():
                    chave, valor = linha.split(":", 1)
                    atual[chave.strip()] = valor.strip()
            else:
                atual["secoes"][secao].append(linha)
    return textos, questoes


def validar(textos, questoes):
    erros, avisos = [], []
    if sorted(questoes) != list(range(1, 101)):
        erros.append("As questões precisam ser exatamente 1 a 100.")
    for n, q in sorted(questoes.items()):
        if q.get("materia") != materia_esperada(n):
            erros.append(f"Q{n}: matéria '{q.get('materia')}' fora da estrutura.")
        if q.get("correta") not in LETRAS:
            erros.append(f"Q{n}: letra correta inválida.")
        for L in LETRAS:
            if not q["secoes"].get(L):
                erros.append(f"Q{n}: alternativa {L} ausente.")
        if len(set(q["secoes"].get(L, "") for L in LETRAS)) < 5:
            erros.append(f"Q{n}: alternativas repetidas.")
        coment = q["secoes"].get("comentario", "")
        if f"Correta ({q['correta']})" not in coment:
            erros.append(f"Q{n}: comentário não indica a correta ({q['correta']}).")
        for L in LETRAS:
            if L != q["correta"] and not re.search(rf"^{L}\) ", coment, re.M):
                erros.append(f"Q{n}: comentário sem a alternativa errada {L}.")
        for campo in ["enunciado"] + list(LETRAS):
            if PROIBIDAS.search(q["secoes"].get(campo, "")):
                erros.append(f"Q{n}: expressão proibida em '{campo}'.")
        if "texto" in q and q["texto"] not in textos:
            erros.append(f"Q{n}: texto-base {q['texto']} inexistente.")
    return erros, avisos


def relatorio(questoes):
    seq = "".join(questoes[n]["correta"] for n in range(1, 101))
    linhas = [f"Sequência do gabarito: {seq}"]
    cont = {L: seq.count(L) for L in LETRAS}
    linhas.append("Letras: " + ", ".join(f"{L}={c}" for L, c in cont.items()))
    ok_cont = all(18 <= c <= 22 for c in cont.values())
    janelas = [i + 1 for i in range(96) if len(set(seq[i:i + 5])) == 5]
    blocos = [i + 1 for i in range(0, 100, 5) if len(set(seq[i:i + 5])) == 5]
    maior_seq = max(len(list(g)) for _, g in itertools.groupby(seq))
    linhas.append(f"Cada letra entre 18 e 22: {'OK' if ok_cont else 'FALHOU'}")
    linhas.append(f"Blocos alinhados de 5 (1-5, 6-10...) com A-E uma vez cada: {blocos or 'nenhum'}")
    linhas.append(f"Quaisquer 5 questões consecutivas com A-E uma vez cada: {janelas or 'nenhuma'}")
    linhas.append(f"Maior sequência de letras iguais: {maior_seq}")

    # Tamanho das alternativas: a correta não pode ser sistematicamente a mais longa
    # (nem a mais curta). Empates exatos (ex.: alternativas numéricas) são neutros.
    mais_longa, mais_curta, empates, razoes, posicoes = [], [], [], [], []
    for n in range(1, 101):
        q = questoes[n]
        tam = {L: len(q["secoes"][L]) for L in LETRAS}
        c = tam[q["correta"]]
        outras = [tam[L] for L in LETRAS if L != q["correta"]]
        if c > max(outras):
            mais_longa.append(n)
        elif c < min(outras):
            mais_curta.append(n)
        if c in outras:
            empates.append(n)
        razoes.append(c / statistics.mean(outras))
        posicoes.append(1 + sum(1 for t in outras if t > c))
    linhas.append(f"Correta é estritamente a mais longa em {len(mais_longa)} questões: {mais_longa}")
    linhas.append(f"Correta é estritamente a mais curta em {len(mais_curta)} questões: {mais_curta}")
    linhas.append(f"Correta empatada em tamanho com outra alternativa: {empates}")
    linhas.append(
        "Posição da correta no ranking de tamanho (1 = mais longa): "
        + ", ".join(f"{p}º={posicoes.count(p)}" for p in range(1, 6))
    )
    linhas.append(f"Tamanho médio da correta / média das erradas: {statistics.mean(razoes):.3f}")

    palavras = {}
    for n in range(1, 101):
        q = questoes[n]
        if "texto" in q:
            continue
        enun = re.sub(r"```.*?```", "", q["secoes"]["enunciado"], flags=re.S)
        palavras[n] = len(enun.split())
    fora = {n: p for n, p in palavras.items() if not 60 <= p <= 100 and n > 25}
    linhas.append(f"Enunciados (fora de Português) com menos de 60 ou mais de 100 palavras: {fora or 'nenhum'}")
    return "\n".join(linhas), mais_longa


def paragrafos(texto):
    """Converte o texto-fonte em Markdown, preservando blocos de código e listas."""
    saida, em_codigo = [], False
    for linha in texto.split("\n"):
        if linha.startswith("```"):
            em_codigo = not em_codigo
            saida.append(linha)
            continue
        if em_codigo:
            saida.append(linha)
        elif linha.startswith("• "):
            if saida and saida[-1] and not saida[-1].startswith("- "):
                saida.append("")
            saida.append("- " + linha[2:])
        else:
            if linha and saida and saida[-1].startswith("- "):
                saida.append("")  # encerra a lista antes do texto seguinte
            saida.append(linha)
    return "\n".join(saida)


def caderno(textos, questoes):
    md = [
        "# Simulado PC-PR 2026 — Agente de Polícia Judiciária",
        "",
        "**Parte A — Caderno de questões** · 100 questões inéditas de múltipla escolha (A–E), "
        "uma única correta · padrão FGV · nível 4 de 5 · tempo de prova: **4h30**",
        "",
        "> Instruções: resolva sem consulta e marque as respostas na folha ao final. "
        "Os textos e os casos foram elaborados exclusivamente para este simulado; nomes e situações são fictícios. "
        "O gabarito comentado (Parte B) está no arquivo separado `gabarito_comentado.md` — só abra depois de terminar.",
        "",
        "| Matéria | Questões |",
        "|---|---|",
    ]
    for ini, fim, nome in ESTRUTURA:
        md.append(f"| {nome} | {ini} a {fim} ({fim - ini + 1}) |")
    usos = {}
    for n in range(1, 101):
        t = questoes[n].get("texto")
        if t:
            usos.setdefault(t, []).append(n)
    mostrados = set()
    materia_atual = None
    for n in range(1, 101):
        q = questoes[n]
        if q["materia"] != materia_atual:
            materia_atual = q["materia"]
            ini, fim = next((a, b) for a, b, m in ESTRUTURA if m == materia_atual)
            md += ["", "---", "", f"## {materia_atual} (questões {ini} a {fim})"]
        t = q.get("texto")
        if t and t not in mostrados:
            mostrados.add(t)
            nums = usos[t]
            md += ["", f"### {textos[t]['titulo']}", "", textos[t]["corpo"], "",
                   f"*O texto acima serve de base para as questões {nums[0]} a {nums[-1]}.*"]
        md += ["", f"**Questão {n}** · {q['materia']}", "", paragrafos(q["secoes"]["enunciado"]), ""]
        for L in LETRAS:
            md += [f"**({L})** {q['secoes'][L]}", ""]
    md += ["---", "", "## Folha de respostas", "",
           "| Q | Resp. | Q | Resp. | Q | Resp. | Q | Resp. |",
           "|---|---|---|---|---|---|---|---|"]
    for i in range(1, 26):
        md.append("| " + " | ".join(f"{i + 25 * k} | " for k in range(4)) + " |")
    return "\n".join(md).replace("\n\n\n", "\n\n") + "\n"


def gabarito(questoes):
    md = [
        "# Simulado PC-PR 2026 — Parte B: gabarito comentado",
        "",
        "> ⚠️ **Não abra antes de fazer a prova.** Este arquivo revela as respostas do caderno `caderno_de_questoes.md`.",
        "",
        "## Gabarito rápido",
        "",
        "| Questões | " + " | ".join(str(i) for i in range(1, 11)) + " |",
        "|---|" + "---|" * 10,
    ]
    for d in range(10):
        letras = [questoes[d * 10 + i]["correta"] for i in range(1, 11)]
        md.append(f"| {d * 10 + 1}–{d * 10 + 10} | " + " | ".join(letras) + " |")
    md += ["", "## Comentários"]
    for n in range(1, 101):
        q = questoes[n]
        md += ["", f"### Questão {n} — {q['correta']}", "", f"*{q['materia']} · {q['subtema']}*", ""]
        for linha in q["secoes"]["comentario"].split("\n"):
            if not linha.strip():
                continue
            m = re.match(r"^(Correta \([A-E]\):|[A-E]\))\s*(.*)$", linha)
            md.append(f"- **{m.group(1)}** {m.group(2)}" if m else f"- {linha}")
    return "\n".join(md) + "\n"


def main():
    textos, questoes = ler_fontes()
    erros, avisos = validar(textos, questoes)
    if erros:
        print("\n".join(erros))
        raise SystemExit(1)
    rel, _ = relatorio(questoes)
    print(rel)
    if "--check" in sys.argv:
        return
    with open(os.path.join(SAIDA, "caderno_de_questoes.md"), "w", encoding="utf-8") as f:
        f.write(caderno(textos, questoes))
    with open(os.path.join(SAIDA, "gabarito_comentado.md"), "w", encoding="utf-8") as f:
        f.write(gabarito(questoes))
    print("Arquivos gerados em", SAIDA)


if __name__ == "__main__":
    main()
