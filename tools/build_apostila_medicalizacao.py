# -*- coding: utf-8 -*-
"""
Apostila de leitura — Grupo 3 (Medicalização e patologização da infância)
Trabalho Avaliativo de Psicologia do Desenvolvimento Humano, 1º Semestre.

Sintetiza 18 fontes da pasta "Fundamentação Teórica" em um texto único,
organizado conforme o roteiro oficial do trabalho (Desenvolvimento do
trabalho, itens 1-6), com citação de fonte e página sempre que necessário.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from pdfgen import PdfBuilder

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "materiais", "desenvolvimento",
    "Apostila_Medicalizacao_Patologizacao_Infancia_Grupo3.pdf"
)

pdf = PdfBuilder()
pdf.title("Medicalização e Patologização da Infância")
pdf.meta("Apostila de leitura — Grupo 3 (Kaio, Ester, Antônia, Flávia) | Infância")
pdf.meta("Psicologia do Desenvolvimento Humano — 1º Semestre | Trabalho Avaliativo, 13/10")
pdf.spacer(14)

SOURCES_NOTE = (
    "Esta apostila sintetiza 18 fontes reunidas na pasta de Fundamentação Teórica do grupo. "
    "Toda afirmação relevante traz, entre parênteses, a indicação (Fonte: nome do PDF, p. X). "
    "A lista completa de referências está ao final. O objetivo do texto, conforme pede o roteiro "
    "do trabalho, não é descrever 'o que é' a medicalização, mas analisar por que ela acontece, "
    "que condições sociais e relacionais a sustentam, e que efeitos produz no desenvolvimento humano."
)

sections = []


def sec(heading, paragraphs):
    sections.append((heading, paragraphs))


# ---------------------------------------------------------------------------
sec("0. Como usar esta apostila", [
    (SOURCES_NOTE, 0, False),
])

# ---------------------------------------------------------------------------
sec("1. Apresentação da problemática", [
    ("O que é medicalização e patologização da infância", 0, True),
    (
        "Medicalização é o processo pelo qual questões da vida social — complexas, multifatoriais, "
        "marcadas pela cultura e pelo tempo histórico — são reduzidas a uma racionalidade que "
        "vincula a dificuldade de adaptação a normas sociais a determinismos orgânicos, que se "
        "expressariam no adoecimento do indivíduo (Fonte: CFP_CartilhaMedicalizacao_web-16.06.15.pdf, p. 11). "
        "Patologizar, por sua vez, é tratar como doença, transtorno ou distúrbio de cunho pessoal ou "
        "familiar aquilo que é, na origem, uma questão de política pública, de cultura ou de "
        "organização social (Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, p. 3, citando Souza, 2016). "
        "Os dois processos costumam andar juntos: medicalizar um fenômeno teve, tradicionalmente, "
        "o sentido de reduzir problemas sócio-políticos a questões individuais, e essa redução tem "
        "por consequência patologizá-lo (Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, p. 2, citando Guarido, 2011).",
        0, False,
    ),
    (
        "Uma imagem resume bem a inversão de lógica que caracteriza o fenômeno: em vez de se "
        "fabricarem remédios para doenças já existentes, fabricam-se doenças para remédios, com "
        "vistas ao aquecimento de um mercado farmacêutico (Fonte: CFP_CartilhaMedicalizacao_web-16.06.15.pdf, p. 12).",
        0, False,
    ),
    ("Como se manifesta hoje", 0, True),
    (
        "No contexto escolar brasileiro, a manifestação mais visível é o encaminhamento maciço de "
        "crianças com dificuldades de aprendizagem ou de comportamento para diagnóstico e tratamento "
        "médico-psiquiátrico: nunca antes as escolas encaminharam tantos estudantes com queixa "
        "escolar para serviços de saúde (Fonte: 01_Dialogos_Medicalizacao.pdf, p. 3). Dificuldades no "
        "processo de ensinar e aprender, que poderiam ser resolvidas com intervenção pedagógica, "
        "passam a ser caracterizadas como transtornos neurológicos que exigem intervenção médica e "
        "medicamentosa (Fonte: 01_Dialogos_Medicalizacao.pdf, p. 3).",
        0, False,
    ),
    (
        "Os números tornam essa manifestação concreta. O Brasil tornou-se o segundo maior mercado "
        "mundial de metilfenidato (Ritalina®, Concerta®), com cerca de 2.000.000 de caixas vendidas "
        "em 2010 (Fonte: Resoluo177Conanda.pdf, p. 1) — alta de 775% no consumo entre 2003 e 2012, "
        "segundo o Instituto de Medicina Social da UERJ (Fonte: Resoluo177Conanda.pdf, p. 2). Em uma "
        "década, as vendas saltaram de 70 mil para dois milhões de caixas por ano, tornando o país o "
        "segundo maior consumidor dessa droga no mundo, atrás apenas dos Estados Unidos "
        "(Fonte: Caderno_AF.pdf, p. 5). Em paralelo, o DSM — manual diagnóstico da psiquiatria "
        "norte-americana — passou de 106 categorias de transtorno em 1952 para cerca de 300 em 2013 "
        "(Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, p. 3) e para aproximadamente 500 na "
        "edição revisada de 2023 (Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO "
        "DIAGNÓSTICA PSIQUIÁTRICA EM DISCUSSÃO.pdf, p. 2-3, 11).",
        0, False,
    ),
    ("Por que é relevante para a fase da infância", 0, True),
    (
        "A infância é o alvo privilegiado desse processo porque é justamente o período em que o "
        "desenvolvimento humano é mais plástico, mais dependente da mediação de adultos e "
        "instituições, e mais sujeito à avaliação permanente por parte da escola e da família. É "
        "também o momento em que a criança menos pode recusar, questionar ou renegociar um "
        "diagnóstico que lhe é atribuído por adultos — pais, professores, médicos — que falam por "
        "ela. Como mostra a Resolução nº 177/2015 do CONANDA, a infância tem direito à proteção "
        "integral e a não ser submetida à excessiva medicalização, definida como \"a redução "
        "inadequada de questões de aprendizagem, comportamento e disciplina a patologias\" "
        "(Fonte: Resoluo177Conanda.pdf, p. 2, Art. 1º, parágrafo único) — o próprio fato de haver uma "
        "resolução federal específica sobre o tema evidencia a magnitude do problema na infância "
        "brasileira contemporânea.",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("2. Glossário — significados das palavras do tema", [
    ("Medicalização", 0, True),
    (
        "Processo que transforma, artificialmente, questões não médicas (sociais, políticas, "
        "pedagógicas, afetivas) em problemas médicos (Fonte: Caderno_AF.pdf, p. 13, Manifesto do "
        "Fórum sobre Medicalização da Educação e da Sociedade). O termo foi proposto por Irving "
        "Zola em 1972 para descrever o aumento da jurisdição da profissão médica sobre novos "
        "domínios da vida (Fonte: 07_Medicalizacao_Infancias_Cuidados_Medicamentos.pdf, p. 452).",
        0, False,
    ),
    ("Patologização", 0, True),
    (
        "Ato de atribuir a um fenômeno o estatuto de doença/transtorno. Enquanto a medicalização é "
        "o processo mais amplo de levar uma questão para o campo médico, a patologização é seu "
        "efeito mais direto: tornar patológico (fora da norma, carente de tratamento) algo que antes "
        "era lido como parte da diversidade humana ou como produto de condições sociais "
        "(Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, p. 2).",
        0, False,
    ),
    ("Biopoder e biopolítica (Michel Foucault)", 0, True),
    (
        "Biopoder é a tecnologia de poder que incide sobre o corpo individual, disciplinando-o, "
        "tornando-o dócil e produtivo; biopolítica é a tecnologia que incide sobre o \"corpo-espécie\" "
        "— a população —, regulando natalidade, mortalidade, saúde e longevidade "
        "(Fonte: 01_Dialogos_Medicalizacao.pdf, p. 5; Fonte: 15_Foucault_Illich_Biopolitica.pdf, p. 100). "
        "\"Uma sociedade normalizadora é o efeito histórico de uma tecnologia de poder centrada na "
        "vida\" (Foucault, citado em Fonte: 15_Foucault_Illich_Biopolitica.pdf, p. 100-101).",
        0, False,
    ),
    ("Iatrogênese (Ivan Illich)", 0, True),
    (
        "Dano ou doença causada pela própria ação médica. Illich distingue três níveis: iatrogênese "
        "clínica (efeitos adversos diretos do tratamento), social (a medicalização da vida como "
        "efeito social) e cultural/estrutural (perda da capacidade autônoma das pessoas de lidar "
        "com a dor, a doença e a morte sem mediação de especialistas) "
        "(Fonte: Ivan Illich da expropriação à desmedicalização da saúde.pdf, p. 1188; "
        "Fonte: 13_Bases_Teoricas_Medicalizacao_Tese_USP.pdf, p. 61-64).",
        0, False,
    ),
    ("TDAH, dislexia e Transtornos Funcionais Específicos (TFE)", 0, True),
    (
        "O TDAH é descrito pela psiquiatria organicista como \"transtorno neurobiológico, de causas "
        "genéticas... caracterizado por sintomas de desatenção, inquietude e impulsividade\" "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 745). A literatura crítica contesta essa "
        "definição: os critérios diagnósticos (\"perde as coisas\", \"é distraído\", \"se remexe na "
        "carteira\") decorrem de aprendizagens sociais e podem mudar conforme o contexto — a mesma "
        "criança pode se agitar na aula de um professor e ficar atenta na de outro "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 748). TFE é a categoria guarda-chuva que "
        "reúne dislexia, disortografia, discalculia e TDAH como supostas \"disfunções neurológicas\" "
        "do aprender (Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 745).",
        0, False,
    ),
    ("Queixa escolar e fracasso escolar", 0, True),
    (
        "Fracasso escolar é uma expressão institucionalizada que opera produzindo saber: antes, o "
        "aluno fracassado era aquele com \"desinteresse\" ou \"falta de educação\"; hoje é o aluno "
        "com alguma disfunção cerebral presumida (Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, "
        "p. 3, citando Luengo, 2010). Considerar que a causa da queixa escolar está no psiquismo ou no "
        "intelecto da criança exime o sistema escolar de qualquer participação na produção dessa "
        "dificuldade (Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, p. 2, citando Souza, 2007).",
        0, False,
    ),
    ("Desmedicalização e despatologização", 0, True),
    (
        "Movimento, acadêmico e social, de resistência à medicalização — presente em hashtags, "
        "fóruns e publicações científicas (Fonte: 05_Mapeando_Controversias.pdf, p. 5) — que propõe "
        "devolver ao campo social, pedagógico e cultural problemas hoje tratados como biológicos. "
        "Illich propunha a \"desprofissionalização\" da medicina como caminho para a desmedicalização "
        "(Fonte: 13_Bases_Teoricas_Medicalizacao_Tese_USP.pdf, p. 69, 72-73).",
        0, False,
    ),
    ("Discurso competente e normal/patológico", 0, True),
    (
        "Discurso competente é o discurso de quem detém saber institucionalmente reconhecido "
        "(o médico, o professor), que adquire o direito de falar e agir pelo outro, destituindo-o de "
        "sua condição de sujeito (Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 758, citando "
        "Chauí, 2014). Para Georges Canguilhem, um traço humano não é normal por ser frequente — "
        "é frequente por ser normal, ou seja, normativo dentro de um determinado modo de vida "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 747).",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("3. Principais autores e referências teóricas", [
    ("Michel Foucault", 0, True),
    (
        "Nunca usou a palavra \"medicalização\", mas descreveu, desde o fim do século XVIII, a "
        "constituição de uma medicina de higienização e disciplinarização dos corpos "
        "(Fonte: 01_Dialogos_Medicalizacao.pdf, p. 5). Em \"Os anormais\", mostra como a psiquiatria se "
        "tornou uma \"medicina do não-patológico\", abrangendo condutas desviantes para além da "
        "loucura clássica (Fonte: 08_Movimentos_Medicalizacao_Vida.pdf, p. 21), e como a família "
        "burguesa foi tornada \"penetrável\" ao poder médico: \"faz-se que ela fique penetrável por "
        "toda uma técnica de poder, de que a medicina e os médicos são transmissores junto às "
        "famílias\" (Fonte: 08_Movimentos_Medicalizacao_Vida.pdf, p. 23, citando Foucault, 2010, p. 222).",
        0, False,
    ),
    ("Ivan Illich", 0, True),
    (
        "Crítico radical da sociedade industrial; via a medicina institucionalizada como uma "
        "\"elite\" que ameaça a saúde ao colonizar a vida e monopolizar o conhecimento sobre o corpo "
        "(Fonte: Ivan Illich da expropriação à desmedicalização da saúde.pdf, p. 1187). Para ele, a "
        "melhoria histórica da expectativa de vida se deveu a condições de nutrição e moradia, não à "
        "ação médica — e a medicina de ponta gerou, em troca, a própria doença iatrogênica "
        "(Fonte: Ivan Illich da expropriação à desmedicalização da saúde.pdf, p. 1189-1190). Morreu em "
        "2002 recusando tratamento médico, por coerência com suas próprias ideias "
        "(Fonte: Ivan Illich da expropriação à desmedicalização da saúde.pdf, p. 1188-1189).",
        0, False,
    ),
    ("Peter Conrad e Irving Zola", 0, True),
    (
        "Conrad mostra que a medicalização não é um imperialismo médico unidirecional: há uma "
        "interação social complexa, com múltiplos atores (indústria farmacêutica, associações de "
        "pais, legisladores), em que o próprio medicalizado é ativo "
        "(Fonte: 01_Dialogos_Medicalizacao.pdf, p. 6). Seu estudo de caso sobre a hipercinesia infantil "
        "(precursora do TDAH) mostra quatro consequências da medicalização de um comportamento: "
        "controle do especialista, controle social médico, individualização de um problema social e "
        "despolitização do desvio (Fonte: 13_Bases_Teoricas_Medicalizacao_Tese_USP.pdf, p. 75-85). "
        "Zola, por sua vez, descreve a medicina como novo \"repositório da verdade\", substituindo a "
        "religião e a lei na regulação social dos comportamentos "
        "(Fonte: 01_Dialogos_Medicalizacao.pdf, p. 6).",
        0, False,
    ),
    ("Maria Helena Souza Patto", 0, True),
    (
        "Referência clássica da crítica brasileira à patologização do fracasso escolar associada a "
        "classe social. Mostrou que a ausência, nas classes populares, de hábitos e práticas das "
        "classes dominantes foi historicamente lida como \"atraso cultural\", deslocando-se depois "
        "para uma leitura organicista: \"a inadequação da escola decorre muito mais de sua má "
        "qualidade... do que da suposição de que os alunos pobres não têm habilidades que, na "
        "realidade, muitas vezes possuem\" (Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, "
        "p. 2, citando Patto, 1990, p. 340).",
        0, False,
    ),
    ("Cecília Collares e Maria Aparecida Moysés", 0, True),
    (
        "Autoras centrais da crítica brasileira à base orgânica atribuída a distúrbios de "
        "aprendizagem. Síntese de sua tese: \"É crescente o deslocamento de problemas inerentes à "
        "vida para o campo médico, com a transformação de questões coletivas, de ordem social e "
        "política, em questões individuais, biológicas... Isentam-se de responsabilidades todas as "
        "instâncias de poder, em cujas entranhas são gerados e perpetuados tais problemas\" "
        "(Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, p. 3, citando Moysés e Collares, 2015, p. 80).",
        0, False,
    ),
    ("Lev Vigotski (psicologia histórico-cultural)", 0, True),
    (
        "Base teórica central para situar a crítica dentro da própria Psicologia do Desenvolvimento: "
        "distingue Funções Psíquicas Elementares (de base biológica) de Funções Psíquicas "
        "Superiores — atenção voluntária, memória lógica, pensamento verbal —, que são "
        "desenvolvidas culturalmente, na relação com o outro e com os instrumentos criados "
        "histórica e socialmente (Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 6). Para Vigotski, "
        "\"toda a aprendizagem só é possível na medida em que se baseia no próprio interesse da "
        "criança\" (Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 752) — um contraponto direto à "
        "ideia de que a desatenção é, por definição, um déficit neurológico fixo.",
        0, False,
    ),
    ("Outros autores que aparecem nas fontes", 0, True),
    (
        "Jacques Donzelot e Philippe Ariès (construção histórica da infância e da família "
        "medicalizada); Sandra Caponi e Luciana Caliman (biodiagnósticos, \"cidadanias biológicas\", "
        "crítica ao DSM-5 e à psiquiatria do desenvolvimento); Marisa Meira (a medicalização oculta "
        "condicionantes sociais, culturais, políticos e afetivos); Allen Frances, ex-coordenador do "
        "próprio DSM-IV, hoje crítico interno do sistema que ajudou a construir: \"Transformamos "
        "problemas cotidianos em transtornos mentais\" (Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, "
        "p. 6); e D. W. Winnicott, cuja teoria do cuidado (holding, \"mãe suficientemente boa\") permite "
        "pensar o sofrimento infantil como efeito de falhas ambientais, não de disfunção cerebral "
        "(Fonte: 07_Medicalizacao_Infancias_Cuidados_Medicamentos.pdf, p. 454).",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("4. Relação com o desenvolvimento humano", [
    (
        "O roteiro pede que o grupo explique quais processos e características do desenvolvimento "
        "estão envolvidos na problemática. A psicologia histórico-cultural de Vigotski oferece a "
        "chave teórica mais direta: o desenvolvimento infantil não é a simples maturação de um "
        "substrato biológico fixo, mas um processo em que funções psíquicas superiores — atenção "
        "voluntária, linguagem, memória lógica — só se formam na relação social, mediadas por "
        "adultos e por instrumentos culturais (Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 6). "
        "Quando um comportamento infantil é lido diretamente como sintoma neurológico, sem "
        "investigar o contexto de interação em que ele ocorre, essa mediação social — motor do "
        "próprio desenvolvimento — é apagada da análise.",
        0, False,
    ),
    (
        "O caso de \"Susi\", documentado em entrevistas e pareceres escolares desde os 2 anos de "
        "idade, ilustra isso de forma concreta: diagnosticada com TDAH aos 6 anos e medicada desde "
        "então, a menina só avançou na leitura e na escrita no 3º ano, com uma professora mais "
        "acolhedora — ainda sob medicação. A melhora foi atribuída pelas próprias pesquisadoras a "
        "fatores afetivo-volitivos da relação pedagógica, e não ao diagnóstico ou ao remédio "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 757). Isso evidencia que a qualidade do "
        "vínculo entre adulto e criança — elemento central de qualquer teoria do desenvolvimento "
        "centrada na interação social — tem peso explicativo maior do que a suposta disfunção "
        "biológica isolada.",
        0, False,
    ),
    (
        "Historicamente, a infância como fase do desenvolvimento também foi construída de modo "
        "distinto da atual: antes do século XVIII, a criança era vista como um \"pequeno adulto\" "
        "(Fonte: 08_Movimentos_Medicalizacao_Vida.pdf, p. 22, citando Ariès, 1978). A psiquiatrização da "
        "infância, posteriormente, nasceu não da \"loucura\" infantil, mas da categoria de \"idiotia\" "
        "— lida à época não como doença, mas como \"uma variação do processo de desenvolvimento, "
        "um estado que pertence à infância\" (Fonte: 08_Movimentos_Medicalizacao_Vida.pdf, p. 24, "
        "citando Lobo, 2008, p. 372). Essa origem histórica mostra que a fronteira entre \"desvio do "
        "desenvolvimento\" e \"doença\" é uma construção social e institucional, não um dado "
        "biológico estável.",
        0, False,
    ),
    (
        "Do ponto de vista afetivo, a perspectiva winnicottiana permite pensar o sofrimento infantil "
        "como efeito de rupturas no cuidado (holding) oferecido pelo ambiente, e não como disfunção "
        "localizada no cérebro da criança: \"quando a criança é medicalizada, o cuidador não promove "
        "um enigma que permite o vir-a-ser infantil\" (Fonte: 07_Medicalizacao_Infancias_Cuidados_"
        "Medicamentos.pdf, p. 454, citando Figueiredo, 2009). O brincar, atividade central do "
        "desenvolvimento infantil para Vigotski e para a psicanálise, também é afetado: a medicação "
        "estimulante \"entorpece e indisponibiliza o sujeito para a interação\", substituindo uma "
        "forma espontânea de elaboração de conflitos por uma solução química "
        "(Fonte: 05_Mapeando_Controversias.pdf, p. 10-11).",
        0, False,
    ),
    (
        "Por fim, há uma dimensão social e histórica mais ampla: mudanças na estrutura familiar "
        "contemporânea — entrada maciça das mulheres no mercado de trabalho sem redistribuição "
        "equivalente do cuidado, inserção muito precoce das crianças em creches — produziriam "
        "\"novas modalidades de subjetivação e de transtornos psíquicos\" "
        "(Fonte: 07_Medicalizacao_Infancias_Cuidados_Medicamentos.pdf, p. 455, citando Birman, 2007). "
        "Entender a problemática exige, portanto, articular processos psicológicos individuais "
        "(vínculo, linguagem, brincar) a transformações sociais, culturais e econômicas mais amplas "
        "— exatamente o que a pergunta norteadora do trabalho pede que o grupo investigue.",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("5. Fundamentação teórica aprofundada", [
    ("A fragilidade científica do DSM", 0, True),
    (
        "Um pilar da fundamentação teórica da crítica é mostrar que o DSM não é um instrumento "
        "neutro de diagnóstico, mas um produto histórico e político. Um levantamento bibliográfico "
        "entre 2014 e 2016 encontrou 128 publicações favoráveis ao manual contra 122 publicações "
        "desfavoráveis — uma controvérsia equilibrada, não um consenso científico "
        "(Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, p. 6). Cerca de 70% da força-tarefa que "
        "compôs o DSM-5 relatou ter relações financeiras com a indústria farmacêutica "
        "(Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf, p. 6, citando Cosgrove & Krimsky, 2012). O psiquiatra Joseph Biederman, "
        "responsável por boa parte da expansão do diagnóstico de bipolaridade infantil nos EUA "
        "(aumento de mais de 40 vezes em poucas décadas), era financiado pela Johnson & Johnson, "
        "fabricante do antipsicótico Risperdal (Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A "
        "CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM DISCUSSÃO.pdf, p. 6).",
        0, False,
    ),
    (
        "Mesmo os estudos de neuroimagem citados para sustentar uma base biológica do TDAH têm "
        "problemas metodológicos sérios: ao reanalisar o estudo mais citado da área (Castellanos et "
        "al., 2002), pesquisadores mostraram que os grupos comparados (medicados, não medicados e "
        "controle) não eram equivalentes em idade, e que a própria medicação estimulante — usada "
        "havia anos pelo grupo \"medicado\" — pode alterar a estrutura cerebral observada, "
        "invertendo a relação de causa e efeito (Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, "
        "p. 746-747). O próprio DSM-5-TR reconhece hoje uma metanálise que não encontrou diferença "
        "de volume cerebral entre crianças com TDAH e controles "
        "(Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf, p. 10). As próprias estimativas de prevalência de TDAH no Brasil variam de "
        "0,9% a 26,8%, segundo o Boletim de Farmacoepidemiologia da Anvisa "
        "(Fonte: Resoluo177Conanda.pdf, p. 2) — uma discrepância incompatível com um transtorno de "
        "base biológica bem definida.",
        0, False,
    ),
    ("A dimensão econômica: a indústria farmacêutica como ator estrutural", 0, True),
    (
        "A indústria farmacêutica é a segunda em faturamento no mundo, atrás apenas da indústria "
        "bélica (Fonte: Caderno_AF.pdf, p. 5). Nos Estados Unidos, o mercado de psicoestimulantes "
        "pulou de 1,7 bilhão para 9 bilhões de dólares em uma década, acompanhando o salto nos "
        "diagnósticos de TDAH de 600 mil para 3,5 milhões a partir de 1990 "
        "(Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf, p. 9). No Brasil, um levantamento junto a municípios paulistas mostrou "
        "aumento de cerca de 1.284% na compra/dispensação de metilfenidato entre 2005 e 2011 "
        "(Fonte: Caderno_AF.pdf, p. 7-8). Entender esses números como fundamentação teórica, e não "
        "apenas como curiosidade estatística, é o que permite ao grupo sustentar a tese foucaultiana "
        "e illichiana de que a medicina contemporânea está estruturalmente associada a interesses "
        "econômicos que extrapolam o cuidado clínico individual (Fonte: 13_Bases_Teoricas_"
        "Medicalizacao_Tese_USP.pdf, p. 109-110, citando Foucault, 1976, p. 193).",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("6. Análise crítica: por que o problema se produz e se mantém", [
    (
        "O roteiro exige evitar explicações individualizantes. As fontes convergem em identificar "
        "pelo menos cinco fatores estruturais, não individuais, que produzem e sustentam a "
        "medicalização da infância:",
        0, False,
    ),
    ("1) A escola terceiriza seus próprios problemas pedagógicos", 0, True),
    (
        "Ao atribuir uma dificuldade de aprendizagem a um transtorno neurológico, a escola isenta "
        "de responsabilidade \"todas as outras instâncias implicadas\", retornando à culpabilização "
        "do estudante (Fonte: 01_Dialogos_Medicalizacao.pdf, p. 3). Um estudo com três Conselhos "
        "Tutelares do Paraná mostrou que são as próprias escolas — e não as famílias — que acionam "
        "esse órgão de proteção para agilizar consultas com neurologistas e psiquiatras, "
        "transformando-o em \"mais um instrumento no processo medicalizante\" "
        "(Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 1, 9-10). Uma conselheira entrevistada "
        "resume o mecanismo: \"se for olhar pelas queixas das escolas, acho que a maioria das "
        "crianças 'taria' medicada, porque sempre é do mau comportamento\" (Fonte: 04_Medicalizacao_"
        "Fracasso_Escolar.pdf, p. 10).",
        0, False,
    ),
    ("2) Classe social e racismo estrutural moldam quem é patologizado", 0, True),
    (
        "A patologização de hoje tem raiz direta na patologização de classe de décadas passadas: "
        "culturas populares foram primeiro lidas como \"inferiores\", depois como produtoras de "
        "crianças com \"atraso\", até a explicação migrar para o terreno biológico "
        "(Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, p. 2). Famílias pobres são "
        "frequentemente rotuladas de \"negligentes\" quando não conseguem manter a rotina de "
        "medicação exigida pela escola e pelo serviço de saúde — um rótulo que pode, na verdade, "
        "funcionar como mecanismo de controle da infância pobre historicamente marginalizada, e não "
        "como proteção genuína (Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 11-12).",
        0, False,
    ),
    ("3) Conflito de interesse econômico na produção do próprio saber diagnóstico", 0, True),
    (
        "Como já apontado na fundamentação teórica, boa parte das pesquisas que sustentam bases "
        "biológicas para o TDAH é financiada pelos laboratórios que fabricam os medicamentos "
        "correspondentes — \"isso significa que são cerceadas por conflitos de interesses\" "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 746, nota 3). Esse não é um problema "
        "de má-fé individual de um médico, mas um desenho estrutural de financiamento da ciência.",
        0, False,
    ),
    ("4) Precarização da escola pública e da formação docente", 0, True),
    (
        "A precariedade das escolas públicas brasileiras — má formação e remuneração dos "
        "professores, falta de recursos materiais e humanos, contradições nos programas do MEC "
        "(Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 12) — é nomeada explicitamente como fator "
        "estrutural de produção do fracasso escolar que depois é lido, de forma invertida, como "
        "problema do aluno. Não se trata de culpar individualmente o professor: evidencia-se, "
        "antes, que a sociedade não valoriza formação profissional embasada em fundamentos críticos "
        "mais aprofundados (Fonte: 04_Medicalizacao_Fracasso_Escolar.pdf, p. 11, citando Silva & "
        "Leonardo, 2012).",
        0, False,
    ),
    ("5) Uma cultura mais ampla de performance e de individualização neoliberal", 0, True),
    (
        "Em uma cultura em que \"a obsessão de ganhar, de vencer, ser alguém\" se tornou norma de "
        "conduta de massa (Fonte: 07_Medicalizacao_Infancias_Cuidados_Medicamentos.pdf, p. 455, "
        "citando Ehrenberg, 2010), e em que problemas sociais são sistematicamente lidos como "
        "falhas individuais — a \"psicologização da vida\" (Fonte: 13_Bases_Teoricas_Medicalizacao_"
        "Tese_USP.pdf, p. 128) —, o diagnóstico biomédico funciona também como alívio moral: ele "
        "\"oferece uma explicação e produz um sentido que alivia o fardo moral ao qual somos "
        "submetidos numa sociedade altamente individualizante\" (Fonte: 08_Movimentos_Medicalizacao_"
        "Vida.pdf, p. 29, citando Caliman).",
        0, False,
    ),
    (
        "É importante registrar uma ressalva presente nas próprias fontes acadêmicas, para que a "
        "análise crítica não se torne, ela mesma, simplificadora: isso não significa negar que "
        "crianças de fato sofrem, nem que algumas requerem apoio clínico. O que está em questão é a "
        "construção de um transtorno concebido à margem das práticas sociais que o produzem "
        "(Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 760).",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("7. Possibilidades de intervenção e enfrentamento", [
    ("No âmbito da família e da escola", 0, True),
    (
        "A cartilha do Conselho Federal de Psicologia recomenda que profissionais de educação não "
        "atribuam a dificuldade só ao aluno, mas trabalhem de forma coletiva (equipe gestora + "
        "professores), com projetos pedagógicos participativos e diversificação de estratégias de "
        "ensino (Fonte: CFP_CartilhaMedicalizacao_web-16.06.15.pdf, p. 24-28). Para profissionais de "
        "saúde, recomenda-se não ler o laudo escolar antes de formar impressão própria, investigar "
        "o contexto familiar e social antes de encaminhar, e evitar fechar diagnóstico de "
        "\"distúrbio orgânico\" sem compreender esse contexto (Fonte: CFP_CartilhaMedicalizacao_web-"
        "16.06.15.pdf, p. 28-39).",
        0, False,
    ),
    ("No âmbito das políticas públicas e da legislação", 0, True),
    (
        "O Brasil já conta com base normativa explícita contra a excessiva medicalização infantil. "
        "A Resolução nº 177/2015 do CONANDA determina que a criança tem direito a \"alternativas "
        "não medicalizantes\" que envolvam família, profissionais e comunidade, e exige abordagem "
        "multiprofissional e intersetorial das questões de aprendizagem e comportamento "
        "(Fonte: Resoluo177Conanda.pdf, p. 2, Art. 2º-3º). Em 2018, o Ministério Público Federal "
        "recomendou formalmente que o Ministério da Saúde e as secretarias estaduais e municipais "
        "se abstivessem de regulamentar um dispositivo do Estatuto da Criança e do Adolescente que "
        "exigiria triagem obrigatória de \"risco psíquico\" em todas as crianças de 0 a 18 meses — "
        "recomendação feita após o próprio Conselho Federal de Psicologia alertar para o \"conceito "
        "equívoco de risco psíquico\" embutido na norma (Fonte: recomendação.pdf, p. 2, 9). O MPF "
        "citou estudos internacionais (Reino Unido, Austrália, Estados Unidos) que desaconselham a "
        "triagem universal de risco psíquico em bebês por falta de evidência científica suficiente "
        "(Fonte: recomendação.pdf, p. 5-6).",
        0, False,
    ),
    ("No âmbito da atuação da Psicologia", 0, True),
    (
        "A especificidade da contribuição da Psicologia na Educação está na mediação entre os "
        "aspectos que constituem a vida humana e os processos educacionais, garantindo a "
        "apropriação dos saberes acumulados historicamente — e não na aplicação de um \"olhar "
        "clínico\" individual sobre a criança (Fonte: Caderno_AF.pdf, p. 10). Entre as propostas "
        "concretas documentadas nas fontes estão: avaliação psicológica como processo de "
        "compreensão das relações escolares, e não apenas da criança isolada "
        "(Fonte: 02_Medicalizacao_Patologizacao_Educacao.pdf, p. 7); Planos Educacionais "
        "Individualizados construídos com professores, pais, psicólogos e, quando possível, a "
        "própria criança (Fonte: 14_Escola_Sofrimento_Critica_DSM.pdf, p. 93-94); e intervenções de "
        "psicologia escolar que criam espaço de fala para professores, pais e estudantes, revelando "
        "a complexidade das relações escolares em vez de localizar o problema em um único sujeito "
        "(Fonte: 01_Dialogos_Medicalizacao.pdf, p. 11).",
        0, False,
    ),
    ("Resgate do brincar e da experiência", 0, True),
    (
        "No plano mais cotidiano, o resgate do brincar como forma legítima de elaboração de "
        "conflitos — \"forma natural de comunicar, de recuperar o papel ativo, de se refazer e de "
        "formar seu eu\" (Fonte: 05_Mapeando_Controversias.pdf, p. 11) — e de uma relação pedagógica "
        "centrada na experiência (\"o que nos passa, o que nos acontece, o que nos toca\", "
        "Fonte: 03_Infancia_Patologizacao_Nao_Aprendizagem.pdf, p. 7, citando Larrosa) aparecem como "
        "alternativas concretas, de baixo custo e sem efeitos colaterais, à resposta medicamentosa.",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("8. Assuntos quentes — controvérsias atuais sobre o tema", [
    (
        "Lei nº 13.438/2017 e a triagem obrigatória de \"risco psíquico\" em bebês de 0 a 18 meses: "
        "incluída no Estatuto da Criança e do Adolescente, a norma segue sem regulamentação por "
        "recomendação expressa do Ministério Público Federal desde 2018, após o CFP alertar para o "
        "risco de ações iatrogênicas — falsos diagnósticos, excesso de intervenção e medicalização "
        "precoce (Fonte: recomendação.pdf, p. 7, 9). É um caso raro em que a oposição à medicalização "
        "chegou ao nível de uma recomendação formal do Ministério Público contra a regulamentação "
        "de uma lei federal já aprovada.",
        0, False,
    ),
    (
        "Conflitos de interesse na elaboração do DSM-5: a revelação de que cerca de 70% dos "
        "membros da força-tarefa do manual tinham vínculo financeiro com a indústria farmacêutica "
        "(Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf, p. 6) alimenta um debate público e acadêmico contínuo sobre a legitimidade "
        "científica dos critérios diagnósticos usados em todo o mundo, inclusive no Brasil.",
        0, False,
    ),
    (
        "A crise da saúde mental infantil nos Estados Unidos como alerta: segundo o ex-diretor do "
        "National Institute of Mental Health, os EUA registraram aumento de 30% nos suicídios entre "
        "1990 e hoje (enquanto o mundo teve redução de 38%), gastaram mais de 200 bilhões de "
        "dólares por ano com saúde mental, e ficaram em 32º lugar entre 38 países ricos em "
        "bem-estar mental infantil, segundo a UNICEF (Fonte: DSM E TRANSTORNOS ASSOCIADOS À "
        "INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM DISCUSSÃO.pdf, p. 11) — um dado usado "
        "por pesquisadores como evidência de que o aumento de diagnósticos e de prescrição "
        "medicamentosa não necessariamente traduz melhora efetiva na saúde mental da população "
        "infantil.",
        0, False,
    ),
    (
        "Movimentos de despatologização nas redes sociais e campanhas institucionais: desde o "
        "Manifesto do Fórum sobre Medicalização da Educação e da Sociedade (mais de 2.300 "
        "assinaturas, Fonte: Caderno_AF.pdf, p. 16) até hashtags contemporâneas de desmedicalização "
        "(Fonte: 05_Mapeando_Controversias.pdf, p. 5), o tema segue mobilizando atores da sociedade "
        "civil, universidades e conselhos profissionais — mostrando que não se trata de um debate "
        "encerrado, mas de uma controvérsia ativa.",
        0, False,
    ),
    (
        "Judicialização e projetos de lei sobre dislexia e TDAH: um levantamento identificou 18 "
        "proposições legislativas entre 2003 e 2011, em diferentes esferas (Câmara Federal, Senado, "
        "Assembleia Legislativa de SP, Câmara Municipal de SP), tratando de dislexia e TDAH "
        "(Fonte: Caderno_AF.pdf, p. 8) — evidência de que a medicalização também avança por via "
        "legislativa, não apenas clínica ou escolar.",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("9. Síntese e resposta à pergunta norteadora", [
    (
        "Pergunta norteadora do trabalho: \"O que essa problemática revela sobre as condições em "
        "que o desenvolvimento humano acontece na sociedade contemporânea?\"",
        0, True,
    ),
    (
        "A medicalização e a patologização da infância revelam, antes de tudo, que o desenvolvimento "
        "humano contemporâneo acontece sob vigilância permanente: a criança de hoje é "
        "continuamente observada, comparada a normas estatísticas e institucionais, e tem seu "
        "comportamento interpretado por adultos que raramente são chamados a examinar sua própria "
        "parte na produção daquilo que classificam como \"problema\" (Fonte: 09_Medicalizacao_"
        "Educacao_Implicacoes.pdf, p. 756, sobre a escola como \"aparelho de exame ininterrupto\", "
        "citando Foucault). Isso mostra que o desenvolvimento infantil, longe de ser um processo "
        "privado e estritamente biológico, acontece dentro de instituições — escola, família, saúde "
        "— que carregam interesses, limitações e históricos próprios, e que frequentemente "
        "resolvem suas próprias insuficiências transferindo o problema para dentro do corpo da "
        "criança.",
        0, False,
    ),
    (
        "Revela também que esse desenvolvimento acontece dentro de uma economia concreta: a "
        "segunda maior indústria do mundo em faturamento tem interesse direto em que mais crianças "
        "sejam diagnosticadas e medicadas (Fonte: Caderno_AF.pdf, p. 5), e boa parte do conhecimento "
        "científico que sustenta esses diagnósticos é produzida sob conflito de interesse "
        "(Fonte: DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf, p. 6). O desenvolvimento humano, nesse sentido, não é hoje regulado apenas "
        "por pais, professores e profissionais de saúde agindo de boa-fé — é também, "
        "estruturalmente, um mercado.",
        0, False,
    ),
    (
        "Por fim, a problemática revela uma sociedade que tende a tratar a diferença — de ritmo, de "
        "comportamento, de origem social — como desvio a ser corrigido, em vez de como parte "
        "esperada da diversidade do desenvolvimento humano. A alternativa que as próprias fontes "
        "apontam não é negar que crianças sofrem ou negam o papel da saúde, mas devolver à análise "
        "a complexidade social, histórica, cultural e institucional que o diagnóstico biomédico "
        "isolado tende a apagar (Fonte: 09_Medicalizacao_Educacao_Implicacoes.pdf, p. 760) — e, com "
        "isso, devolver à criança o estatuto de sujeito em desenvolvimento dentro de uma rede de "
        "relações, e não de paciente a ser ajustado por um transtorno.",
        0, False,
    ),
])

# ---------------------------------------------------------------------------
sec("10. Referências (fontes utilizadas nesta apostila)", [
    (
        "ATUMANE, A. M. A. Michel Foucault e Ivan Illich: análise crítica à medicalização da vida e "
        "do corpo. [SYN]THESIS, v. 12, n. 1, p. 98-107, 2019. "
        "(15_Foucault_Illich_Biopolitica.pdf)",
        0, False,
    ),
    (
        "AZEVEDO, L. J. C. de. Medicalização das infâncias: entre os cuidados e os medicamentos. "
        "Psicologia USP, v. 29, n. 3, p. 451-458, 2018. "
        "(07_Medicalizacao_Infancias_Cuidados_Medicamentos.pdf)",
        0, False,
    ),
    (
        "BARBOSA, M. de B.; LEITE, C. D. P. Infância e patologização: contornos sobre a questão da "
        "não aprendizagem. Psicologia Escolar e Educacional, v. 24, e220707, 2020. "
        "(03_Infancia_Patologizacao_Nao_Aprendizagem.pdf)",
        0, False,
    ),
    (
        "BARBOSA, S. A. Mapeando as controvérsias que envolvem o processo de medicalização da "
        "infância. Psicologia & Sociedade, v. 31, e213211, 2019. (05_Mapeando_Controversias.pdf)",
        0, False,
    ),
    (
        "BELTRAME, R. L.; GESSER, M.; SOUZA, S. V. de. Diálogos sobre medicalização da infância e "
        "educação: uma revisão de literatura. Psicologia em Estudo, v. 24, e42566, 2019. "
        "(01_Dialogos_Medicalizacao.pdf)",
        0, False,
    ),
    (
        "CONSELHO FEDERAL DE PSICOLOGIA / Fórum sobre Medicalização da Educação e da Sociedade. "
        "Recomendações de práticas não medicalizantes para profissionais e serviços de educação e "
        "saúde. São Paulo, 2015. (CFP_CartilhaMedicalizacao_web-16.06.15.pdf)",
        0, False,
    ),
    (
        "CONSELHO FEDERAL DE PSICOLOGIA. Subsídios para a Campanha Não à Medicalização da Vida. "
        "XV Plenário, Gestão 2011-2013. (Caderno_AF.pdf)",
        0, False,
    ),
    (
        "CONSELHO NACIONAL DOS DIREITOS DA CRIANÇA E DO ADOLESCENTE (CONANDA). Resolução nº 177, "
        "de 11 de dezembro de 2015. (Resoluo177Conanda.pdf)",
        0, False,
    ),
    (
        "FIGUEIRA, P. L.; CALIMAN, L. V. Considerações sobre os movimentos de medicalização da "
        "vida. Psicologia Clínica, v. 26, n. 2, p. 17-32, 2014. (08_Movimentos_Medicalizacao_Vida.pdf)",
        0, False,
    ),
    (
        "MINAKAWA, M. M. Bases teóricas dos processos de medicalização: um olhar sobre as forças "
        "motrizes. Dissertação (Mestrado em Saúde Pública) — USP, 2016. "
        "(13_Bases_Teoricas_Medicalizacao_Tese_USP.pdf)",
        0, False,
    ),
    (
        "MINISTÉRIO PÚBLICO FEDERAL — PRDF. Recomendação GAB-LLO/PRDF nº 01/2018. Brasília, "
        "10 jan. 2018. (recomendação.pdf)",
        0, False,
    ),
    (
        "PERUZZOLO, M. C.; VIARO, R. V. DSM e transtornos associados à infância: a classificação "
        "diagnóstica psiquiátrica em discussão. 2024. "
        "(DSM E TRANSTORNOS ASSOCIADOS À INFÂNCIA A CLASSIFICAÇÃO DIAGNÓSTICA PSIQUIÁTRICA EM "
        "DISCUSSÃO.pdf)",
        0, False,
    ),
    (
        "SCARIN, A. C. C. F.; SOUZA, M. P. R. de. Medicalização e patologização da educação: "
        "desafios à Psicologia Escolar e Educacional. Psicologia Escolar e Educacional, v. 24, "
        "e214158, 2020. (02_Medicalizacao_Patologizacao_Educacao.pdf)",
        0, False,
    ),
    (
        "SCHOENBERGER, F.; CHAMPAGNATTE, D. M. de O. Escola e sofrimento psíquico infantil: "
        "crítica ao DSM e caminhos para uma prática pedagógica inclusiva. p. 80-97. "
        "(14_Escola_Sofrimento_Critica_DSM.pdf)",
        0, False,
    ),
    (
        "SIGNOR, R. de C. F.; BERBERIAN, A. P.; SANTANA, A. P. A medicalização da educação: "
        "implicações para a constituição do sujeito/aprendiz. Educação e Pesquisa, v. 43, n. 3, "
        "p. 743-763, 2017. (09_Medicalizacao_Educacao_Implicacoes.pdf)",
        0, False,
    ),
    (
        "TABET, L. P. et al. Ivan Illich: da expropriação à desmedicalização da saúde. Saúde em "
        "Debate, v. 41, n. 115, p. 1187-1198, 2017. "
        "(Ivan Illich da expropriação à desmedicalização da saúde.pdf)",
        0, False,
    ),
    (
        "TAVERNA, C. S. R. [Resenha] Medicalização de Crianças e Adolescentes. Revista da ABRAPEE, "
        "v. 15, n. 1, p. 169-171, 2011. (06_Medicalizacao_Criancas_Adolescentes.pdf)",
        0, False,
    ),
    (
        "WERLANG, E. M.; PEREIRA, D. P.; BETT, G. de C. Medicalização da infância, fracasso escolar "
        "e Conselho Tutelar: uma análise histórico-cultural. Psicologia em Estudo, v. 29, e55625, "
        "2024. (04_Medicalizacao_Fracasso_Escolar.pdf)",
        0, False,
    ),
    (
        "Roteiro do Trabalho Avaliativo — Psicologia do Desenvolvimento Humano (documento-base da "
        "disciplina). (Roteiro_Trabalho_Psicologia_Desenvolvimento_Humano_45_alunos.pdf)",
        0, False,
    ),
])


for heading, paragraphs in sections:
    pdf.heading(heading)
    for text, indent, bold in paragraphs:
        pdf.body(text, indent=indent, bold=bold)
    pdf.spacer(8)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
data = pdf.build()
with open(OUT_PATH, "wb") as f:
    f.write(data)

print("Gerado:", OUT_PATH)
print("Tamanho:", len(data), "bytes")
