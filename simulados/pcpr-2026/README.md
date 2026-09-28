# Simulado PC-PR 2026 — Agente de Polícia Judiciária (padrão FGV)

Simulado com 100 questões inéditas de múltipla escolha (A–E) e nível de dificuldade 4 de 5, montado conforme o prompt `prompt_simulado_pcpr_outra_ia.md`.

| Arquivo | Conteúdo |
|---|---|
| [`caderno_de_questoes.md`](caderno_de_questoes.md) | **Parte A**: as 100 questões e uma folha de respostas, sem nenhuma marcação da correta |
| [`gabarito_comentado.md`](gabarito_comentado.md) | **Parte B**: gabarito e comentários. ⚠️ Revela as respostas; só abra depois de fazer a prova |
| `fonte/` | Arquivos-fonte e o script `build.py`, que gera e valida os dois arquivos acima. ⚠️ Também contêm as respostas |

A ordem e a quantidade das matérias seguem o prompt (25 LP, 5 RLM, 5 Paraná, 25 Informática, 10 Forenses, 5 Contabilidade, 5 Estatística, 5 Legislação, 3 em cada ramo do Direito). Tempo de prova: 4h30.

## Controles contra padrões no gabarito

O script `fonte/build.py` confere as regras abaixo a cada geração:

- **Nenhum bloco de 5 questões seguidas tem A, B, C, D e E exatamente uma vez.** A regra vale para os blocos 1–5, 6–10 etc. e também para qualquer outra sequência de 5 questões consecutivas. Não dá, portanto, para deduzir a quinta resposta a partir das outras quatro. (Toda regra desse tipo dá alguma pista: se você tiver certeza de quatro respostas diferentes entre si, só consegue descartar uma letra para a quinta, bem menos do que o padrão antigo, que entregava a resposta.)
- **Frequência das letras:** A = 21, B = 19, C = 19, D = 21, E = 20, dentro da faixa de 18 a 22 exigida pelo prompt. No máximo 3 letras iguais seguidas.
- **A resposta certa não tende a ser a alternativa mais longa.** Em número de caracteres, a correta é a mais longa em 18 questões e a mais curta em 19, perto dos 20% esperados por acaso. Em média, a correta tem o mesmo tamanho das erradas (razão 0,993). Nas demais questões ela fica no meio, ou empata em tamanho com outras alternativas, como nas numéricas.
- Os casos das questões fora de Língua Portuguesa têm entre 60 e 100 palavras (nível 4). Nenhuma alternativa usa "todas/nenhuma das anteriores" nem remete a outra letra.

## Fidelidade às normas e limites conhecidos

- Os comentários do gabarito citam o dispositivo (artigo, parágrafo, inciso), a súmula ou o precedente que decide cada questão de Direito e de legislação.
- **Legislação Estadual e Institucional (questões 81 a 85):** as cinco questões cobram a Lei Estadual 23.213/2026 (Lei Orgânica da PC-PR, subtema 5.4), com base no texto publicado no Diário Oficial nº 12150, de 22/05/2026. Os temas são hierarquia (art. 9º), Conselho Superior de Polícia (arts. 16 a 18), Corregedoria-Geral (art. 21), criação de unidades policiais (arts. 54 e 55) e avocação de inquérito (arts. 50 e 51). Essas questões receberam letras de gabarito diferentes das que as antigas 81 a 85 tinham.
- **Subtemas não usados por falta de texto confiável.** Pela regra "na dúvida sobre vigência, não use o dispositivo", ficaram de fora a LC estadual 259/2023 (5.2) e a Lei estadual 21.894/2024 (5.5). Também não há questão que dependa de numeração de artigos da Constituição do Paraná nem da Lei 15.358/2026.
- Em Direito Penal, as três questões seguem os blocos do levantamento FGV (Parte Geral, Parte Especial e Legislação Extravagante). O subtema 6.2 (processual) está coberto pelas questões 89 a 91.
- Realidade do Paraná evita dados conjunturais (governo atual, estatísticas recentes) e usa fatos históricos, geográficos e metodológicos estáveis.
- Antes da prova, vale confirmar se houve alteração legislativa recente nos pontos cobrados, em especial Lei Maria da Penha, art. 12-C, e Lei de Interceptação, art. 8º-A.

## Como regenerar

```bash
python3 simulados/pcpr-2026/fonte/build.py          # gera caderno e gabarito e imprime o relatório de controle
python3 simulados/pcpr-2026/fonte/build.py --check  # só valida
```
