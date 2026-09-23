# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import write_correction_pdf

OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "correcoes", "neuro"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "SM1_0078500_gabarito.pdf")

TITLE = "Correcao - SM1 Neuroanatomofisiologia (Codigo 0078500, Versao A)"
META = [
    "Disciplina: ARA0332 - NEUROANATOMOFISIOLOGIA | Unid.: Constantino Nery | Turma: 1002",
    "Prof.: Francisca Martins | Turno/Regime: SM1 2026.2",
    "Resultado: 10 de 10 questoes objetivas corretas.",
]

QUESTOES = [
    dict(
        n=1,
        pergunta="O Sistema Nervoso Central e composto por:",
        marcada="B",
        correta="B",
        texto_correta="Encefalo e medula espinal",
        justificativa=(
            "O SNC e formado exclusivamente pelo encefalo (cerebro, cerebelo e "
            "tronco encefalico) e pela medula espinal; nervos, ganglios e "
            "receptores pertencem ao sistema nervoso periferico."
        ),
    ),
    dict(
        n=2,
        pergunta="Qual das alternativas abaixo representa uma estrutura que faz parte do diencefalo?",
        marcada="D",
        correta="D",
        texto_correta="Hipotalamo",
        justificativa=(
            "O diencefalo e formado por talamo, hipotalamo, epitalamo e "
            "subtalamo. Mesencefalo, ponte e bulbo pertencem ao tronco "
            "encefalico, e o cerebelo e uma estrutura a parte."
        ),
    ),
    dict(
        n=3,
        pergunta="Os dendritos do neuronio possuem como principal funcao:",
        marcada="C",
        correta="C",
        texto_correta="Receber estimulos nervosos",
        justificativa=(
            "Os dendritos sao prolongamentos curtos e ramificados "
            "especializados em captar estimulos de outros neuronios e "
            "conduzi-los ate o corpo celular."
        ),
    ),
    dict(
        n=4,
        pergunta=(
            "Qual estrutura do sistema nervoso tem a funcao de acelerar a "
            "passagem do impulso nervoso e, alem disso, funciona como um "
            "isolante termico ao redor do axonio?"
        ),
        marcada="D",
        correta="D",
        texto_correta="Bainha de mielina",
        justificativa=(
            "A bainha de mielina reveste o axonio, isolando-o e permitindo a "
            "conducao saltatoria do impulso nervoso, o que acelera sua "
            "propagacao."
        ),
    ),
    dict(
        n=5,
        pergunta="Qual das seguintes opcoes descreve corretamente a funcao dos neuronios?",
        marcada="C",
        correta="C",
        texto_correta="Conduzem sinais eletricos e transmitem informacoes no sistema nervoso",
        justificativa=(
            "Neuronios sao celulas excitaveis especializadas em gerar e "
            "conduzir potenciais de acao, transmitindo informacao entre "
            "regioes do sistema nervoso e do corpo."
        ),
    ),
    dict(
        n=6,
        pergunta=(
            "Os neuronios sao celulas especializadas na transmissao de "
            "impulsos nervosos. De acordo com sua funcao, eles podem ser "
            "classificados como:"
        ),
        marcada="B",
        correta="B",
        texto_correta="Sensoriais, motores e interneuronios",
        justificativa=(
            "Classificacao funcional classica: sensoriais/aferentes (captam "
            "estimulos), motores/eferentes (geram respostas) e "
            "interneuronios (associativos, conectam os dois grupos)."
        ),
    ),
    dict(
        n=7,
        pergunta=(
            "O SNC humano e composto por dois orgaos principais protegidos "
            "por estruturas osseas. Assinale a alternativa que apresenta "
            "corretamente os orgaos que formam o SNC e a estrutura que "
            "protege o canal vertebral."
        ),
        marcada="B",
        correta="B",
        texto_correta="Encefalo e medula espinhal; coluna vertebral",
        justificativa=(
            "O encefalo e protegido pelo cranio e a medula espinal pela "
            "coluna vertebral (canal vertebral formado pelas vertebras)."
        ),
    ),
    dict(
        n=8,
        pergunta="Sobre as celulas da glia (neuroglia), e correto afirmar que:",
        marcada="C",
        correta="C",
        texto_correta=(
            "Dao suporte, nutricao, sustentacao e protecao aos neuronios, "
            "alem de participarem da formacao da mielina"
        ),
        justificativa=(
            "As celulas da neuroglia (astrocitos, microglia, oligodendrocitos, "
            "ependimarias no SNC; celulas satelites e de Schwann no SNP) nao "
            "geram potenciais de acao, mas sustentam, nutrem e protegem os "
            "neuronios, alem de formarem a bainha de mielina."
        ),
    ),
    dict(
        n=9,
        pergunta=(
            "Na figura do tronco encefalico, a regiao sombreada na BASE da "
            "figura (a parte mais inferior, logo acima da medula espinal) "
            "recebe o nome de:"
        ),
        marcada="D",
        correta="D",
        texto_correta="Bulbo",
        justificativa=(
            "O tronco encefalico e formado, de cima para baixo, por "
            "mesencefalo, ponte e bulbo (medula oblonga). O bulbo e a porcao "
            "mais caudal, situada na base da figura, que se continua "
            "diretamente com a medula espinal."
        ),
    ),
    dict(
        n=10,
        pergunta=(
            "Na vista lateral do encefalo, com o cerebelo identificado pelo "
            "numero 5, os numeros 1, 2, 3 e 4 correspondem, respectivamente, "
            "aos lobos do cortex cerebral:"
        ),
        marcada="B",
        correta="B",
        texto_correta="1-Frontal; 2-Parietal; 3-Temporal; 4-Occipital",
        justificativa=(
            "Disposicao anteroposterior classica dos lobos cerebrais: "
            "1 = lobo frontal (mais anterior), 2 = lobo parietal (posterior "
            "ao sulco central), 3 = lobo temporal (regiao inferior), "
            "4 = lobo occipital (regiao mais posterior)."
        ),
    ),
]


def build():
    sections = []
    for q in QUESTOES:
        ok = q["marcada"] == q["correta"]
        status = "CORRETA" if ok else "INCORRETA"
        heading = f"Questao {q['n']} -- {status}"
        body = [
            (q["pergunta"], 0, False),
            (f"Resposta marcada: {q['marcada']}  |  Resposta correta: {q['correta']}) {q['texto_correta']}", 0, True),
            (q["justificativa"], 10, False),
        ]
        sections.append((heading, body))

    write_correction_pdf(OUT_PATH, TITLE, META, sections)
    print("gerado:", OUT_PATH)


if __name__ == "__main__":
    build()
