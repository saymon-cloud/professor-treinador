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

FONTE_TEMA1 = "Tema 1 Introducao ao estudo da neuroanatofisiologia.pdf"
FONTE_TEMA2 = "Tema 2 Sistema nervoso central.pdf"

QUESTOES = [
    dict(
        n=1,
        pergunta="O Sistema Nervoso Central e composto por:",
        opcoes={
            "A": "Nervos e ganglios.",
            "B": "Encefalo e medula espinal.",
            "C": "Receptores e efetores.",
            "D": "Sistema simpatico e parassimpatico.",
            "E": "Axonios e dendritos.",
        },
        marcada="B",
        correta="B",
        texto_correta="Encefalo e medula espinal",
        justificativa=(
            "O SNC e formado exclusivamente pelo encefalo (cerebro, cerebelo e "
            "tronco encefalico) e pela medula espinal; nervos, ganglios e "
            "receptores pertencem ao sistema nervoso periferico."
        ),
        fonte=FONTE_TEMA2, pagina="2",
    ),
    dict(
        n=2,
        pergunta="Qual das alternativas abaixo representa uma estrutura que faz parte do diencefalo?",
        opcoes={
            "A": "Mesencefalo.",
            "B": "Ponte.",
            "C": "Bulbo.",
            "D": "Hipotalamo.",
            "E": "Cerebelo.",
        },
        marcada="D",
        correta="D",
        texto_correta="Hipotalamo",
        justificativa=(
            "O diencefalo e formado por talamo, hipotalamo, epitalamo e "
            "subtalamo. Mesencefalo, ponte e bulbo pertencem ao tronco "
            "encefalico, e o cerebelo e uma estrutura a parte."
        ),
        fonte=FONTE_TEMA2, pagina="22",
    ),
    dict(
        n=3,
        pergunta="Os dendritos do neuronio possuem como principal funcao:",
        opcoes={
            "A": "Produzir mielina.",
            "B": "Gerar neurotransmissores.",
            "C": "Receber estimulos nervosos.",
            "D": "Formar a bainha neural.",
            "E": "Produzir liquido cefalorraquidiano.",
        },
        marcada="C",
        correta="C",
        texto_correta="Receber estimulos nervosos",
        justificativa=(
            "Os dendritos sao prolongamentos curtos e ramificados "
            "especializados em captar estimulos de outros neuronios e "
            "conduzi-los ate o corpo celular."
        ),
        fonte=FONTE_TEMA1, pagina="4",
    ),
    dict(
        n=4,
        pergunta=(
            "Qual estrutura do sistema nervoso tem a funcao de acelerar a "
            "passagem do impulso nervoso e, alem disso, funciona como um "
            "isolante termico ao redor do axonio?"
        ),
        opcoes={
            "A": "Dendritos.",
            "B": "Axonio.",
            "C": "Corpo Celular.",
            "D": "Bainha de mielina.",
            "E": "Nenhuma das alternativas.",
        },
        marcada="D",
        correta="D",
        texto_correta="Bainha de mielina",
        justificativa=(
            "A bainha de mielina reveste o axonio, isolando-o e permitindo a "
            "conducao saltatoria do impulso nervoso, o que acelera sua "
            "propagacao."
        ),
        fonte=FONTE_TEMA1, pagina="6",
    ),
    dict(
        n=5,
        pergunta="Qual das seguintes opcoes descreve corretamente a funcao dos neuronios?",
        opcoes={
            "A": "Armazenam informacoes em formato digital.",
            "B": "Regulam a pressao arterial e os batimentos cardiacos.",
            "C": "Conduzem sinais eletricos e transmitem informacoes no sistema nervoso.",
            "D": "Produzem hormonios que controlam o metabolismo.",
            "E": "Realizam a filtracao do sangue nos rins.",
        },
        marcada="C",
        correta="C",
        texto_correta="Conduzem sinais eletricos e transmitem informacoes no sistema nervoso",
        justificativa=(
            "Neuronios sao celulas excitaveis especializadas em gerar e "
            "conduzir potenciais de acao, transmitindo informacao entre "
            "regioes do sistema nervoso e do corpo."
        ),
        fonte=FONTE_TEMA1, pagina="3",
    ),
    dict(
        n=6,
        pergunta=(
            "Os neuronios sao celulas especializadas na transmissao de "
            "impulsos nervosos. De acordo com sua funcao, eles podem ser "
            "classificados como:"
        ),
        opcoes={
            "A": "Motores, gliais e ependimarios.",
            "B": "Sensoriais, motores e interneuronios.",
            "C": "Aferentes, eferentes e mioelinicos.",
            "D": "Gliais, sensitivos e autonomicos.",
            "E": "Axonais, dendriticos e somaticos.",
        },
        marcada="B",
        correta="B",
        texto_correta="Sensoriais, motores e interneuronios",
        justificativa=(
            "Classificacao funcional classica: sensoriais/aferentes (captam "
            "estimulos), motores/eferentes (geram respostas) e "
            "interneuronios (associativos, conectam os dois grupos)."
        ),
        fonte=FONTE_TEMA1, pagina="7",
    ),
    dict(
        n=7,
        pergunta=(
            "O SNC humano e composto por dois orgaos principais protegidos "
            "por estruturas osseas. Assinale a alternativa que apresenta "
            "corretamente os orgaos que formam o SNC e a estrutura que "
            "protege o canal vertebral."
        ),
        opcoes={
            "A": "Cerebro e cerebelo; meninges.",
            "B": "Encefalo e medula espinhal; coluna vertebral.",
            "C": "Encefalo e nervos cranianos; cranio.",
            "D": "Cerebro e ganglios nervosos; costelas.",
            "E": "Medula espinal e nervos espinhais; vertebras.",
        },
        marcada="B",
        correta="B",
        texto_correta="Encefalo e medula espinhal; coluna vertebral",
        justificativa=(
            "O encefalo e protegido pelo cranio e a medula espinal pela "
            "coluna vertebral (canal vertebral formado pelas vertebras)."
        ),
        fonte=FONTE_TEMA2, pagina="2",
    ),
    dict(
        n=8,
        pergunta="Sobre as celulas da glia (neuroglia), e correto afirmar que:",
        opcoes={
            "A": "Sao responsaveis diretas por gerar e propagar o potencial de acao.",
            "B": "Nao desempenham qualquer funcao relevante no tecido nervoso.",
            "C": "Dao suporte, nutricao, sustentacao e protecao aos neuronios, alem de participarem da formacao da mielina.",
            "D": "Existem apenas no sistema nervoso periferico.",
            "E": "Substituem os neuronios na transmissao sinaptica.",
        },
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
        fonte=FONTE_TEMA1, pagina="5",
    ),
    dict(
        n=9,
        pergunta=(
            "Na figura do tronco encefalico, a regiao sombreada na BASE da "
            "figura (a parte mais inferior, logo acima da medula espinal) "
            "recebe o nome de:"
        ),
        opcoes={
            "A": "Ponte.",
            "B": "Mesencefalo.",
            "C": "Cerebelo.",
            "D": "Bulbo.",
            "E": "Hipotalamo.",
        },
        marcada="D",
        correta="D",
        texto_correta="Bulbo",
        justificativa=(
            "O tronco encefalico e formado, de cima para baixo, por "
            "mesencefalo, ponte e bulbo (medula oblonga). O bulbo e a porcao "
            "mais caudal, situada na base da figura, que se continua "
            "diretamente com a medula espinal."
        ),
        fonte=FONTE_TEMA2, pagina="16",
    ),
    dict(
        n=10,
        pergunta=(
            "Na vista lateral do encefalo, com o cerebelo identificado pelo "
            "numero 5, os numeros 1, 2, 3 e 4 correspondem, respectivamente, "
            "aos lobos do cortex cerebral:"
        ),
        opcoes={
            "A": "1-Frontal; 2-Occipital; 3-Limbico; 4-Espinhal.",
            "B": "1-Frontal; 2-Parietal; 3-Temporal; 4-Occipital.",
            "C": "1-Temporal; 2-Occipital; 3-Basal; 4-Espinhal.",
            "D": "1-Medular; 2-Temporal; 3-Limbico; 4-Frontal.",
            "E": "1-Parietal; 2-Medular; 3-Occipital; 4-Bulbar.",
        },
        marcada="B",
        correta="B",
        texto_correta="1-Frontal; 2-Parietal; 3-Temporal; 4-Occipital",
        justificativa=(
            "Disposicao anteroposterior classica dos lobos cerebrais: "
            "1 = lobo frontal (mais anterior), 2 = lobo parietal (posterior "
            "ao sulco central), 3 = lobo temporal (regiao inferior), "
            "4 = lobo occipital (regiao mais posterior)."
        ),
        fonte=FONTE_TEMA2, pagina="27",
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
