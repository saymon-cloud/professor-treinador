# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import write_correction_pdf

OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "correcoes", "teorias_cc"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "SM1_0076775_gabarito.pdf")

TITLE = "Correcao - SM1 Teorias Cognitivo-Comportamentais (Codigo 0076775, Versao A)"
META = [
    "Disciplina: ARA0444 - AS TEORIAS COGNITIVO COMPORTAMENTAIS | Unid.: Constantino Nery",
    "Prof.: Natalia de Castro Loureiro | Turma: 1001 | Data: 11/09/2026",
    "Resultado: 5 de 10 questoes objetivas corretas.",
    "Atencao: algumas marcacoes na folha usam simbolos diferentes (asterisco, cruz, barra) e",
    "podem ter sido lidas com incerteza -- se alguma resposta abaixo nao bater com o que voce",
    "realmente marcou, me avise para eu corrigir.",
]

FONTE_PRINCIPIOS = "Principios basicos do behaviorismo.pdf"
FONTE_ANALISE = "Analise aplicada de contingencias.pdf"

QUESTOES = [
    dict(
        n=1,
        pergunta=(
            "De acordo com o Behaviorismo Radical, extinguir um comportamento "
            "significa suspender a consequencia reforcadora, ate que o "
            "comportamento retorne ao nivel operante. Porem, o inicio do "
            "procedimento de extincao provoca alguns 'efeitos' no organismo. "
            "Assinale a alternativa correta em relacao a um efeito:"
        ),
        opcoes={
            "A": "Diminuicao da frequencia de resposta.",
            "B": "Aumento de comportamentos ruins.",
            "C": "Aumento da frequencia da resposta.",
            "D": "Estabilidade na topografia da resposta.",
            "E": "Aumento de comportamentos punitivos.",
        },
        marcada="A",
        correta="C",
        texto_correta="Aumento da frequencia da resposta",
        justificativa=(
            "O material descreve exatamente esse fenomeno (a 'explosao de "
            "extincao'): no exemplo do controle remoto que para de funcionar, "
            "a pessoa aperta os botoes com MAIS forca e frequencia logo no "
            "inicio da extincao, antes de a resposta finalmente diminuir. A "
            "diminuicao (opcao A) e o resultado final do processo, mas o "
            "'efeito' notavel logo no inicio e esse aumento temporario."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="25",
    ),
    dict(
        n=2,
        pergunta=(
            "Leia o trecho da musica 'Cotidiano', de Chico Buarque: 'Seis da "
            "tarde como era de se esperar / Ela pega e me espera no portao'. "
            "De acordo com o condicionamento operante, a musica expressa o "
            "seguinte tipo de contingencia operante em relacao ao "
            "comportamento da mulher:"
        ),
        opcoes={
            "A": "Punicao positiva.",
            "B": "Reforco negativo.",
            "C": "Reforco positivo.",
            "D": "Punicao negativa.",
            "E": "Extincao operante.",
        },
        marcada="C",
        correta="C",
        texto_correta="Reforco positivo",
        justificativa=(
            "O reencontro com o companheiro e uma consequencia agradavel que "
            "e adicionada apos o comportamento de esperar no portao, "
            "mantendo esse comportamento -- a definicao classica de reforco "
            "positivo (adicao de um estimulo agradavel que aumenta a "
            "frequencia do comportamento)."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="18",
    ),
    dict(
        n=3,
        pergunta=(
            "Uma psicologa escolar observa que uma crianca frequentemente "
            "interrompe a aula fazendo brincadeiras. Apos analise funcional, "
            "identifica que os colegas costumam rir sempre que isso "
            "acontece. Com base na analise aplicada de contingencias, a "
            "intervencao mais adequada seria:"
        ),
        opcoes={
            "A": "Aumentar a quantidade de tarefas escolares.",
            "B": "Ignorar sistematicamente o comportamento inadequado e reforcar participacoes adequadas.",
            "C": "Aplicar punicoes cada vez mais severas.",
            "D": "Explicar a crianca por que o comportamento e inadequado.",
            "E": "Retirar a crianca da sala sempre que ela fizer brincadeiras.",
        },
        marcada="B",
        correta="B",
        texto_correta="Ignorar sistematicamente o comportamento inadequado e reforcar participacoes adequadas",
        justificativa=(
            "O comportamento e mantido pela atencao/riso dos colegas "
            "(reforco social). A intervencao correta em analise aplicada do "
            "comportamento combina extincao (remover o reforco do "
            "comportamento-problema) com reforco diferencial de "
            "comportamentos alternativos adequados."
        ),
        fonte=FONTE_ANALISE, pagina="28",
    ),
    dict(
        n=4,
        pergunta=(
            "Um coordenador de curso observou que poucos alunos "
            "participavam das discussoes em sala de aula. Passou a atribuir "
            "pontos extras aos estudantes que contribuissem de forma "
            "relevante. Apos algumas semanas, a frequencia das "
            "participacoes aumentou significativamente. De acordo com os "
            "principios do condicionamento operante, qual conceito explica "
            "melhor esse fenomeno?"
        ),
        opcoes={
            "A": "Condicionamento respondente.",
            "B": "Generalizacao de estimulos.",
            "C": "Reforcamento positivo.",
            "D": "Punicao negativa.",
            "E": "Habituacao.",
        },
        marcada="B",
        correta="C",
        texto_correta="Reforcamento positivo",
        justificativa=(
            "Adicionar uma consequencia agradavel (pontos extras) "
            "contingente ao comportamento (participar), aumentando sua "
            "frequencia, e a definicao direta de reforco positivo. "
            "Generalizacao de estimulos e um conceito diferente -- responder "
            "de forma semelhante a estimulos parecidos, nao entra em jogo "
            "neste cenario."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="18",
    ),
    dict(
        n=5,
        pergunta=(
            "(MOREIRA E MEDEIROS, 2019) De acordo com os conceitos de "
            "reflexo inato, estimulo e resposta, e correto apenas o que se "
            "afirma em:"
        ),
        opcoes={
            "A": "Um estimulo eliciara sempre a mesma resposta e com a mesma magnitude, independentemente de sua intensidade.",
            "B": "Um reflexo pode ser definido como uma reacao voluntaria do individuo a certos estimulos.",
            "C": "A relacao entre estimulo e resposta, que caracteriza um reflexo inato, e exclusiva do repertorio comportamental de animais irracionais (o que exclui o homem).",
            "D": "Estudar para tirar boas notas e um exemplo de reflexo inato.",
            "E": "Um reflexo expressa a relacao entre um estimulo e uma resposta, na qual dizemos que uma resposta e eliciada por um estimulo.",
        },
        marcada="B",
        correta="E",
        texto_correta="Um reflexo expressa a relacao entre um estimulo e uma resposta, na qual dizemos que uma resposta e eliciada por um estimulo",
        justificativa=(
            "O reflexo e por definicao uma resposta INVOLUNTARIA (nao "
            "voluntaria, como diz a opcao B) eliciada por um estimulo. O "
            "material define: 'Reflexos nao sao apenas comportamentos, mas "
            "sim a relacao entre estimulo e resposta' -- exatamente a opcao "
            "E. Alem disso, quanto maior a intensidade do estimulo, maior a "
            "intensidade da resposta (refutando A), reflexos existem tambem "
            "no ser humano (refutando C), e estudar para notas e "
            "comportamento operante aprendido, nao reflexo inato (refutando D)."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="7",
    ),
    dict(
        n=6,
        pergunta=(
            "Observe a imagem que representa uma situacao classica dos "
            "estudos de B. F. Skinner, em que um animal aprende a pressionar "
            "uma alavanca para obter alimento."
        ),
        opcoes={
            "A": "O animal pressiona a alavanca porque possui um desejo inconsciente de encontrar alimento.",
            "B": "O comportamento ocorre devido exclusivamente a fatores hereditarios.",
            "C": "O animal aprendeu a pressionar a alavanca porque essa acao foi seguida por uma consequencia reforcadora (receber alimento).",
            "D": "O comportamento e resultado de um conflito emocional interno.",
            "E": "O animal age apenas por imitacao de outros animais.",
        },
        marcada="C",
        correta="C",
        texto_correta="O animal aprendeu a pressionar a alavanca porque essa acao foi seguida por uma consequencia reforcadora (receber alimento)",
        justificativa=(
            "E a descricao classica do condicionamento operante na Caixa de "
            "Skinner: uma resposta (pressionar a alavanca) seguida de uma "
            "consequencia reforcadora (alimento) aumenta em frequencia."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="16",
    ),
    dict(
        n=7,
        pergunta=(
            "Durante um atendimento psicologico infantil, uma terapeuta "
            "observa que uma crianca apresenta respostas reflexas de "
            "ansiedade sempre que ouve barulhos altos, como buzinas e "
            "sirenes. Considerando a aplicacao dos principios do "
            "condicionamento classico na pratica clinica, qual das "
            "estrategias a seguir pode ser mais eficaz para reduzir essa "
            "resposta reflexa?"
        ),
        opcoes={
            "A": "Exposicao gradual aos sons em um ambiente controlado, associando-os a estimulos positivos para promover a dessensibilizacao.",
            "B": "Aplicacao imediata de reforco positivo sempre que a crianca demonstrar sinais de ansiedade, fortalecendo sua resposta emocional.",
            "C": "Evitacao total de qualquer ambiente onde esses sons possam ocorrer, reduzindo completamente a exposicao ao estimulo aversivo.",
            "D": "Introducao de estimulos ainda mais intensos para acelerar a adaptacao da crianca e extinguir sua resposta reflexa rapidamente.",
            "E": "Uso de tecnicas de reforco negativo, removendo o som dos ambientes sempre que a crianca demonstrar sinais de ansiedade.",
        },
        marcada="A",
        correta="A",
        texto_correta="Exposicao gradual aos sons em um ambiente controlado, associando-os a estimulos positivos para promover a dessensibilizacao",
        justificativa=(
            "A dessensibilizacao sistematica (exposicao gradual pareada com "
            "estimulos positivos) e a tecnica classica derivada do "
            "condicionamento respondente para reduzir respostas de ansiedade "
            "condicionadas."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="20",
    ),
    dict(
        n=8,
        pergunta=(
            "O behaviorismo surgiu como uma tentativa de tornar a Psicologia "
            "uma ciencia objetiva. Watson defendia o foco no comportamento "
            "observavel. Thorndike contribuiu com a Lei do Efeito. Skinner "
            "desenvolveu o condicionamento operante. Assinale a alternativa "
            "correta:"
        ),
        opcoes={
            "A": "Watson defendia que a introspeccao era o metodo mais confiavel para estudar o comportamento humano.",
            "B": "Thorndike demonstrou, por meio da Lei do Efeito, que comportamentos seguidos de consequencias positivas tendem a se repetir.",
            "C": "Skinner rejeitava o uso de reforcos, afirmando que apenas reflexos automaticos poderiam ser estudados cientificamente.",
            "D": "O behaviorismo considera que os processos mentais subjetivos sao mais importantes que o comportamento observavel.",
            "E": "O behaviorismo radical de Skinner negava a possibilidade de modelar comportamentos complexos, limitando-se a respostas simples.",
        },
        marcada="B",
        correta="B",
        texto_correta="Thorndike demonstrou, por meio da Lei do Efeito, que comportamentos seguidos de consequencias positivas tendem a se repetir",
        justificativa=(
            "A Lei do Efeito de Thorndike estabelece exatamente isso: "
            "respostas seguidas de consequencias satisfatorias tendem a se "
            "repetir; as demais alternativas contradizem os proprios "
            "fundamentos do behaviorismo."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="5",
    ),
    dict(
        n=9,
        pergunta=(
            "Os reflexos podem ser classificados em inatos e aprendidos. Com "
            "base nesses conceitos, assinale a alternativa correta:"
        ),
        opcoes={
            "A": "O reflexo inato depende de experiencias previas para se manifestar, como no caso da salivacao condicionada ao som do sino.",
            "B": "O reflexo aprendido ocorre sem necessidade de associacao entre estimulos, sendo sempre automatico e herdado geneticamente.",
            "C": "O reflexo patelar e um exemplo de reflexo aprendido, pois so se desenvolve apos repetidas experiencias de treinamento.",
            "D": "O condicionamento classico de Pavlov demonstra como um estimulo inicialmente neutro pode se tornar condicionado e eliciar uma resposta aprendida.",
            "E": "A succao realizada pelo bebe ao encontrar o mamilo da mae e um exemplo de reflexo aprendido, pois depende da repeticao da experiencia.",
        },
        marcada="A",
        correta="D",
        texto_correta="O condicionamento classico de Pavlov demonstra como um estimulo inicialmente neutro pode se tornar condicionado e eliciar uma resposta aprendida",
        justificativa=(
            "O material define: 'estimulo condicionado e aquele que "
            "previamente era neutro e que passa a eliciar uma resposta "
            "condicionada' -- exatamente a opcao D. As demais alternativas "
            "trocam inato por aprendido: a salivacao condicionada ao sino "
            "(A) e um reflexo APRENDIDO, nao inato; o reflexo patelar (C) e "
            "a succao do bebe (E) sao reflexos INATOS, nao aprendidos."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="9",
    ),
    dict(
        n=10,
        pergunta=(
            "Em um programa de intervencao para adolescentes, um psicologo "
            "utiliza estrategias baseadas no condicionamento operante. "
            "Analise as proposicoes como VERDADEIRAS ou FALSAS e assinale a "
            "sequencia correta: "
            "(1) O comportamento e influenciado pelas consequencias que "
            "ocorrem apos sua emissao. "
            "(2) O reforco positivo consiste na remocao de um estimulo "
            "agradavel para aumentar a frequencia do comportamento. "
            "(3) No reforco negativo, um estimulo aversivo e removido para "
            "aumentar a probabilidade do comportamento desejado. "
            "(4) A punicao positiva reduz um comportamento indesejado ao "
            "introduzir um estimulo aversivo apos sua ocorrencia. "
            "(5) A extincao ocorre quando um comportamento deixa de ser "
            "seguido por reforco, levando a sua diminuicao ao longo do tempo."
        ),
        opcoes={
            "A": "V - F - V - V - F",
            "B": "V - V - F - F - V",
            "C": "V - F - V - V - V",
            "D": "F - V - V - F - V",
            "E": "V - V - V - V - V",
        },
        marcada="D",
        correta="C",
        texto_correta="V - F - V - V - V",
        justificativa=(
            "(1) Verdadeiro -- principio basico do condicionamento operante. "
            "(2) Falso -- reforco positivo e a ADICAO de um estimulo "
            "agradavel, nao a remocao (a remocao de um estimulo agradavel "
            "para reduzir comportamento e punicao negativa). (3) Verdadeiro "
            "-- definicao correta de reforco negativo. (4) Verdadeiro -- "
            "definicao correta de punicao positiva. (5) Verdadeiro -- "
            "definicao correta de extincao."
        ),
        fonte=FONTE_PRINCIPIOS, pagina="18, 22 e 26",
    ),
]


def build():
    sections = []
    for q in QUESTOES:
        ok = q["marcada"] == q["correta"]
        status = "CORRETA" if ok else "INCORRETA"
        heading = f"Questao {q['n']} -- {status}"
        body = [(q["pergunta"], 0, False)]
        for letra, texto in q["opcoes"].items():
            marca = []
            if letra == q["marcada"]:
                marca.append("marcada")
            if letra == q["correta"]:
                marca.append("correta")
            sufixo = f"  [{', '.join(marca)}]" if marca else ""
            body.append((f"{letra}) {texto}{sufixo}", 10, letra == q["correta"]))
        body.append((f"Resposta marcada: {q['marcada']}  |  Resposta correta: {q['correta']}", 0, True))
        body.append((q["justificativa"], 10, False))
        body.append((f"Fonte: {q['fonte']}, p. {q['pagina']}", 10, False))
        sections.append((heading, body))

    write_correction_pdf(OUT_PATH, TITLE, META, sections)
    print("gerado:", OUT_PATH)


if __name__ == "__main__":
    build()
