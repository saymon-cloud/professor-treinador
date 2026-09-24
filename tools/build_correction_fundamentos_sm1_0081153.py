# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import write_correction_pdf

OUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "correcoes", "fundamentos"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "SM1_0081153_gabarito.pdf")

TITLE = "Correcao - SM1 Fundamentos Hist. e Epistemologicos (Codigo 0081153, Versao A)"
META = [
    "Disciplina: ARA4339 - FUNDAMENTOS HIS. E EPISTEMOLOGICOS DA PSICOLOGIA | Unid.: Constantino Nery",
    "Prof.: Hilda Nogueira dos Santos | Turma: 1001 | Data: 24/09/2026",
    "Resultado: 10 de 10 questoes objetivas corretas.",
]

FONTE_ANTECEDENTES = "ANTECEDENTES HISTORICOS E ESTATUTO CIENTIFICO DA PSICOLOGIA.pdf"
FONTE_PSICANALISE = "PSICANALISE, GESTALT E PSICOLOGIA HUMANISTA.pdf"

QUESTOES = [
    dict(
        n=1,
        pergunta="Para Descartes, as ideias derivadas (adventicias) sao aquelas que:",
        opcoes={
            "A": "Surgem da experiencia e parecem chegar ao pensamento por meio dos sentidos.",
            "B": "Existem na mente independentemente de qualquer experiencia.",
            "C": "Sao necessariamente produzidas pela razao antes da experiencia.",
            "D": "Sao exclusivamente ideias matematicas.",
            "E": "Correspondem apenas as ideias relacionadas a Deus.",
        },
        marcada="A",
        correta="A",
        texto_correta="Surgem da experiencia e parecem chegar ao pensamento por meio dos sentidos",
        justificativa=(
            "As ideias derivadas/adventicias sao as que chegam a mente pela via "
            "sensorial, em oposicao as ideias inatas (presentes na razao, "
            "independente da experiencia)."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="5",
    ),
    dict(
        n=2,
        pergunta="Na filosofia de Rene Descartes, as ideias inatas sao aquelas que:",
        opcoes={
            "A": "Sao adquiridas exclusivamente por meio dos sentidos.",
            "B": "Sao produzidas pela imaginacao a partir de experiencias anteriores.",
            "C": "Estao presentes na razao e nao dependem diretamente da experiencia sensivel.",
            "D": "Sao formadas somente pela observacao dos fenomenos naturais.",
            "E": "Resultam da combinacao de diferentes experiencias sensoriais.",
        },
        marcada="C",
        correta="C",
        texto_correta="Estao presentes na razao e nao dependem diretamente da experiencia sensivel",
        justificativa=(
            "O racionalismo cartesiano postula ideias inatas -- presentes na razao "
            "desde sempre, nao extraidas da experiencia sensivel."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="5",
    ),
    dict(
        n=3,
        pergunta=(
            "Uma pessoa observa uma arvore e forma em sua mente a ideia desse "
            "objeto. De acordo com a classificacao de Descartes, essa ideia pode "
            "ser considerada:"
        ),
        opcoes={
            "A": "Inata, pois todas as ideias sobre objetos ja estao prontas na mente.",
            "B": "Inata, pois resulta exclusivamente da razao.",
            "C": "Inata, pois nao depende da experiencia.",
            "D": "Impossivel, pois os sentidos nao participam da formacao de ideias.",
            "E": "Derivada ou adventicia, pois esta relacionada a experiencia sensivel.",
        },
        marcada="E",
        correta="E",
        texto_correta="Derivada ou adventicia, pois esta relacionada a experiencia sensivel",
        justificativa=(
            "Observar um objeto concreto e formar sua ideia correspondente e o "
            "exemplo classico de ideia derivada/adventicia -- chega a mente pela "
            "via dos sentidos, nao pela razao pura."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="5",
    ),
    dict(
        n=4,
        pergunta=(
            "O desenvolvimento da ciencia moderna esteve relacionado ao chamado "
            "metodo cientifico. De modo geral, esse metodo buscava:"
        ),
        opcoes={
            "A": "Produzir conhecimentos baseados na observacao, na formulacao de hipoteses e na verificacao.",
            "B": "Explicar os fenomenos apenas por meio de tradicoes antigas.",
            "C": "Substituir a razao pela fe como principal forma de conhecimento.",
            "D": "Evitar qualquer tipo de experimentacao.",
            "E": "Considerar que todos os conhecimentos ja haviam sido produzidos na Antiguidade.",
        },
        marcada="A",
        correta="A",
        texto_correta="Produzir conhecimentos baseados na observacao, na formulacao de hipoteses e na verificacao",
        justificativa=(
            "O metodo cientifico moderno (base positivista) exige observacao "
            "empirica rigorosa, formulacao de hipoteses/leis e verificacao "
            "passivel de reproducao por outros pesquisadores."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="16",
    ),
    dict(
        n=5,
        pergunta=(
            "Um marco associado a consolidacao da Psicologia como ciencia ocorreu "
            "quando Wilhelm Wundt criou um laboratorio de investigacao de "
            "processos psicologicos em Leipzig. Esse acontecimento e importante "
            "porque:"
        ),
        opcoes={
            "A": "Representou o inicio dos estudos psicologicos exclusivamente religiosos.",
            "B": "Demonstrou que a Psicologia poderia desenvolver investigacoes experimentais proprias.",
            "C": "Eliminou a influencia da Filosofia sobre todos os estudos psicologicos.",
            "D": "Estabeleceu a Psicanalise como principal escola psicologica.",
            "E": "Definiu o comportamento como unico objeto possivel da Psicologia.",
        },
        marcada="B",
        correta="B",
        texto_correta="Demonstrou que a Psicologia poderia desenvolver investigacoes experimentais proprias",
        justificativa=(
            "O laboratorio de Wundt (1879, Leipzig) e o marco do nascimento da "
            "Psicologia experimental, mostrando ser possivel investigar processos "
            "psicologicos com metodo proprio, nao apenas especulacao filosofica."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="8",
    ),
    dict(
        n=6,
        pergunta=(
            "Durante o seculo XIX, pesquisadores passaram a buscar formas mais "
            "sistematicas de estudar os fenomenos psicologicos. Esse processo foi "
            "importante para a consolidacao da Psicologia como ciencia porque:"
        ),
        opcoes={
            "A": "A Psicologia abandonou completamente os estudos sobre o comportamento humano.",
            "B": "A Psicologia passou a utilizar exclusivamente explicacoes filosoficas.",
            "C": "Os pesquisadores deixaram de realizar observacoes sobre os fenomenos psicologicos.",
            "D": "A Psicologia passou a considerar um conhecimento que refutava a metodologia cientifica corrente.",
            "E": "Os fenomenos psicologicos passaram a ser investigados por meio de metodos cientificos e experimentais.",
        },
        marcada="E",
        correta="E",
        texto_correta="Os fenomenos psicologicos passaram a ser investigados por meio de metodos cientificos e experimentais",
        justificativa=(
            "A consolidacao da Psicologia como ciencia se deu pela adocao de "
            "criterios positivistas de cientificidade -- metodos objetivos, "
            "observaveis e passiveis de verificacao empirica."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="16",
    ),
    dict(
        n=7,
        pergunta=(
            "A Gestalt se dedicou ao estudo da percepcao e da forma como os "
            "individuos organizam os estimulos, pressupondo que a experiencia "
            "perceptiva nao pode ser reduzida a soma dos elementos isolados. "
            "Assinale a alternativa CORRETA:"
        ),
        opcoes={
            "A": "A lei da boa forma, ou pregnancia, explica a tendencia de percebermos elementos que estao proximos uns dos outros como pertencentes a um mesmo grupo.",
            "B": "A lei da proximidade e a principal lei da Gestalt e afirma que o cerebro sempre interpreta as imagens da forma mais simples e equilibrada possivel.",
            "C": "O insight corresponde a compreensao subita de uma situacao ou a percepcao repentina da solucao de um problema.",
            "D": "A lei do fechamento afirma que o olhar tende a seguir uma direcao continua, acompanhando linhas e curvas.",
            "E": "A lei da continuidade explica a tendencia de completarmos mentalmente formas que estao incompletas para percebermos um objeto fechado.",
        },
        marcada="C",
        correta="C",
        texto_correta="O insight corresponde a compreensao subita de uma situacao ou a percepcao repentina da solucao de um problema",
        justificativa=(
            "As demais alternativas trocam as definicoes das leis da Gestalt "
            "entre si. O insight (Kohler, estudos com chimpanzes em Tenerife) e "
            "a reestruturacao subita do campo perceptual que revela a solucao "
            "de um problema, sem tentativa e erro gradual."
        ),
        fonte=FONTE_PSICANALISE, pagina="18",
    ),
    dict(
        n=8,
        pergunta=(
            "Na segunda topica (1923), Freud formulou o aparelho psiquico como "
            "Isso (id), Eu (ego) e Supereu (superego). Qual e o papel principal "
            "do Eu (Ego) nessa formulacao?"
        ),
        opcoes={
            "A": "Atuar como a sede primitiva das pulsoes, buscando sua satisfacao imediata segundo o principio do prazer.",
            "B": "Mediar as exigencias pulsionais do Isso (id), as imposicoes da realidade e as demandas do Supereu (superego).",
            "C": "Estabelecer julgamentos morais e sentimentos de culpa por meio da internalizacao de normas e valores.",
            "D": "Exercer a funcao simbolica de separar de forma definitiva a relacao dual entre mae e bebe.",
            "E": "Buscar a satisfacao imediata dos desejos inconscientes, sem considerar as exigencias da realidade ou as normas internalizadas.",
        },
        marcada="B",
        correta="B",
        texto_correta="Mediar as exigencias pulsionais do Isso (id), as imposicoes da realidade e as demandas do Supereu (superego)",
        justificativa=(
            "O Ego e a instancia mediadora do aparelho psiquico: harmoniza os "
            "impulsos do Id, os julgamentos morais do Superego e as limitacoes "
            "da realidade externa, usando mecanismos de defesa quando necessario."
        ),
        fonte=FONTE_PSICANALISE, pagina="13",
    ),
    dict(
        n=9,
        pergunta=(
            "Identifique as afirmativas abaixo, assinalando 1 para Racionalismo e "
            "2 para Empirismo, e marque a sequencia correta: "
            "(1) Defende que o conhecimento se inicia pela experiencia, pela "
            "observacao e pelas sensacoes que temos do mundo. "
            "(2) A partir da observacao da realidade, e possivel organizar as "
            "informacoes, identificar regularidades e, por meio da abstracao e "
            "da razao, chegar a conhecimentos mais gerais. "
            "(3) Considera que o conhecimento e construido a partir da "
            "experiencia, dos habitos e das relacoes que estabelecemos com o "
            "mundo. "
            "(4) Defende uma distincao entre alma e corpo e considera que "
            "existem estruturas ou ideias que nao dependem da experiencia para "
            "serem conhecidas. "
            "(5) Defende que a razao e o principal meio para alcancar "
            "conhecimentos verdadeiros e universais. "
            "(6) Considera que algumas ideias ou principios fundamentais sao "
            "inatos, nao sendo adquiridos exclusivamente por meio da experiencia."
        ),
        opcoes={
            "A": "2 - 2 - 2 - 1 - 1 - 1",
            "B": "2 - 2 - 1 - 2 - 1 - 1",
            "C": "1 - 2 - 2 - 1 - 1 - 2",
            "D": "2 - 2 - 1 - 1 - 2 - 1",
            "E": "1 - 1 - 1 - 2 - 2 - 2",
        },
        marcada="A",
        correta="A",
        texto_correta="2-2-2-1-1-1",
        justificativa=(
            "As tres primeiras afirmativas descrevem o Empirismo (conhecimento "
            "via experiencia, observacao, habitos); as tres ultimas descrevem o "
            "Racionalismo (dualismo cartesiano, primazia da razao, ideias "
            "inatas) -- sequencia 2-2-2-1-1-1."
        ),
        fonte=FONTE_ANTECEDENTES, pagina="5",
    ),
    dict(
        n=10,
        pergunta=(
            "Joao procura atendimento apos perceber que sabota conquistas "
            "importantes; ao falar do pai exigente, muda de assunto, depois "
            "comeca a chegar atrasado e questiona o tratamento. Pelos "
            "pressupostos da Psicanalise, qual a interpretacao mais adequada?"
        ),
        opcoes={
            "A": "Os comportamentos de Joao podem estar relacionados a conflitos psiquicos inconscientes, enquanto suas mudancas de assunto e atrasos podem representar formas de resistencia diante de conteudos que provocam conflitos.",
            "B": "O comportamento de Joao e resultado exclusivamente da falta de motivacao consciente e pode ser solucionado por meio do estabelecimento de metas e recompensas.",
            "C": "A dificuldade de Joao deve ser compreendida principalmente como uma resposta automatica a estimulos ambientais, sem necessidade de considerar sua historia pessoal.",
            "D": "Como Joao afirma conscientemente desejar o sucesso, nao e possivel considerar a existencia de desejos ou conflitos inconscientes relacionados ao seu comportamento.",
            "E": "Joao desiste de suas conquistas e passa a cometer erros como forma consciente de contrariar as expectativas e exigencias do pai.",
        },
        marcada="A",
        correta="A",
        texto_correta=(
            "Os comportamentos de Joao podem estar relacionados a conflitos "
            "psiquicos inconscientes, enquanto suas mudancas de assunto e "
            "atrasos podem representar formas de resistencia"
        ),
        justificativa=(
            "A resistencia e o fenomeno clinico em que o paciente apresenta "
            "bloqueios, hesitacoes, mudancas de assunto ou atrasos diante de "
            "conteudos que provocam conflito -- e a manifestacao do recalque, "
            "protegendo o Ego da angustia associada as lembrancas dolorosas."
        ),
        fonte=FONTE_PSICANALISE, pagina="6",
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
