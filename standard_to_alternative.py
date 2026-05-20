import re

# =========================
# BLOCO 0
# =========================

MAPA_ACENTOS = str.maketrans({
    "á": "a", "à": "a", "â": "a",
    "é": "e", "è": "e", "ê": "e",
    "í": "i", "ì": "i", "î": "i",
    "ó": "o", "ò": "o", "ô": "o",
    "ú": "u", "ù": "u", "û": "u",
})

def remover_acentos_seletivos(texto):
    return texto.translate(MAPA_ACENTOS)

BLOCO_0 = [
    {
        "nome": "R45",
        "descricao": "preservar a distinção de é antes da retirada de acentos",
        "tipo": "regex",
        "padrao": r"\bé\b",
        "sub": "e'",
    },
    {
        "nome": "R45a",
        "descricao": "preservar a distinção de nós antes da retirada de acentos",
        "tipo": "regex",
        "padrao": r"\bnós\b",
        "sub": "nois",
    },
    {
        "nome": "R0",
        "descricao": "remover agudo, circunflexo e crase; preservar til",
        "tipo": "funcao",
        "funcao": remover_acentos_seletivos,
    },
    {
        "nome": "R14.1",
        "descricao": "nas sequências axi ou oxi, x para qis",
        "tipo": "regex",
        "padrao": r"(\w*)pr([oó])xim(\w+)",
        "sub": r"\1pr\2ssim\3",
    },
    {
        "nome": "R14.2",
        "descricao": "nas sequências axi ou oxi, x para qis",
        "tipo": "regex",
        "padrao": r"aux([ií])l(\w+)",
        "sub": r"auss\1l\2",
    },
]

# =========================
# BLOCO 1
# =========================

BLOCO_1 = [
    {"nome": "R1", "descricao": "lh para li", "tipo": "regex", "padrao": r"lh", "sub": "li"},
    {"nome": "R2", "descricao": "nh para ni", "tipo": "regex", "padrao": r"nh", "sub": "ni"},
    {"nome": "R3", "descricao": "h em início de palavra é eliminado", "tipo": "regex", "padrao": r"\bh", "sub": ""},
    {"nome": "R4", "descricao": "r em início de palavra para rr", "tipo": "regex", "padrao": r"\br", "sub": "rr"},
    {"nome": "R5", "descricao": "r após n para rr", "tipo": "regex", "padrao": r"(?<=n)r", "sub": "rr"},
]

# =========================
# BLOCO 2
# =========================

BLOCO_2 = [
    # {"nome": "R6", "descricao": "c antes de a ou o para q", "tipo": "regex", "padrao": r"c(?=[ao])", "sub": "q"},
    {"nome": "R7", "descricao": "que/qui em início de palavra para qe/qi", "tipo": "regex", "padrao": r"\bqu([ei])", "sub": r"q\1"},
    {"nome": "R8", "descricao": "que/qui em final de palavra para qe/qi", "tipo": "regex", "padrao": r"qu([ei])\b", "sub": r"q\1"},
    {"nome": "R9", "descricao": "que/qui medial para q#e/q#i", "tipo": "regex", "padrao": r"(?<=\w)qu([ei])(?=\w)", "sub": r"q\1"},
]

# =========================
# BLOCO 3
# =========================

# =========================
# EXCEÇÕES E FUNÇÃO DA R13
# =========================

EXCECOES_R13 = [
    r"\baguent\w+\b",
    r"\bli[nm]gui\w+\b",
    r"\beguela\b",
]

PADRAO_R13 = r"(?<=\w)gu([ei])(?=\w)"
SUB_R13 = r"g\1"


def aplicar_R13_com_excecoes(texto):
    protegidas = {}

    def proteger(match):
        chave = f"§§R13_EXC_{len(protegidas)}§§"
        protegidas[chave] = match.group(0)
        return chave

    texto_protegido = texto

    # 1. Protege palavras excepcionadas
    for padrao in EXCECOES_R13:
        texto_protegido = re.sub(padrao, proteger, texto_protegido)

    # 2. Aplica a R13 no restante do texto
    texto_protegido = re.sub(PADRAO_R13, SUB_R13, texto_protegido)

    # 3. Restaura as palavras excepcionadas
    for chave, palavra_original in protegidas.items():
        texto_protegido = texto_protegido.replace(chave, palavra_original)

    return texto_protegido

BLOCO_3 = [
    {"nome": "R10", "descricao": "g antes de e ou i para j", "tipo": "regex", "padrao": r"g(?=[ei])", "sub": "j"},
    {"nome": "R11", "descricao": "gue/gui em início de palavra para ge/gi", "tipo": "regex", "padrao": r"\bgu([ei])", "sub": r"g\1"},
    {"nome": "R12", "descricao": "gue/gui em final de palavra para ge/gi", "tipo": "regex", "padrao": r"gu([ei])\b", "sub": r"g\1"},
    {"nome": "R13", "descricao": "gue/gui medial para g#e/g#i", "tipo": "funcao", "funcao": aplicar_R13_com_excecoes,},
]

# =========================
# BLOCO 4
# =========================

BLOCO_4 = [
    # {"nome": "R14", "descricao": "nas sequências axi ou oxi, x para qis", "tipo": "regex", "padrao": r"(taxis?|axiomas?|axilas?|maximiz)", "sub": r"(taqisis?|aqisiomas?|aqisilas?|maqisimiz)"},
    {"nome": "R15", "descricao": "na sequência exV, x para z", "tipo": "regex", "padrao": r"(?<=e)x(?=[aeiouãõ])", "sub": "z"},
    {"nome": "R16", "descricao": "z em final de palavra para s", "tipo": "regex", "padrao": r"z\b", "sub": "s"},
    {"nome": "R17", "descricao": "x antes de p ou t para s", "tipo": "regex", "padrao": r"x(?=[pt])", "sub": "s"}, 
    {"nome": "R17a", "descricao": "x antes de c e consoante", "tipo": "regex", "padrao": r"x(c[lr])", "sub": r"s\1"},
    {"nome": "R17b", "descricao": "x final de palavra", "tipo": "regex", "padrao": r"(\b\w+[aeiou])x\b", "sub": r"\1qis"}, # xerox, torax mas não ex
]

# =========================
# BLOCO 5
# =========================

BLOCO_5 = [
    {"nome": "R18", "descricao": "ãos para auns", "tipo": "regex", "padrao": r"ãos", "sub": "auns"},
    {"nome": "R19", "descricao": "ões para oens", "tipo": "regex", "padrao": r"ões", "sub": "oens"}, 
    {"nome": "R20", "descricao": "ães para aens", "tipo": "regex", "padrao": r"ães", "sub": "aens"},
    {"nome": "R21", "descricao": "õem para oem", "tipo": "regex", "padrao": r"õem", "sub": "oem"},
    {"nome": "R22", "descricao": "ão para aum", "tipo": "regex", "padrao": r"ão", "sub": "aum"},
    {"nome": "R23", "descricao": "õe para oem", "tipo": "regex", "padrao": r"õe", "sub": "oem"},
    {"nome": "R24", "descricao": "ãe para aem", "tipo": "regex", "padrao": r"ãe", "sub": "aem"},
    {"nome": "R25", "descricao": "am em final de palavra para aum", "tipo": "regex", "padrao": r"am\b", "sub": "aum"},
    {"nome": "R26", "descricao": "ã para am", "tipo": "regex", "padrao": r"ã", "sub": "am"},
]

# =========================
# BLOCO 6
# =========================

BLOCO_6 = [
    {"nome": "R27", "descricao": "s entre vogais para z", "tipo": "regex", "padrao": r"(?<=[aeiouãõ])s(?=[aeiouãõ])", "sub": "z"}, #antisociais > antizociais
    {"nome": "R28", "descricao": "digrafo xc ou sc para s", "tipo": "regex", "padrao": r"(?:xc|sc)([ei])", "sub": r"s\1"},
    {"nome": "R14", "descricao": "nas sequências axi ou oxi, x para qis", "tipo": "regex", "padrao": r"([ao])xi", "sub": r"\1qisi"},
    {"nome": "R29", "descricao": "ç antecedido ou nao por s para s", "tipo": "regex", "padrao": r"s?ç", "sub": "s"},
    {"nome": "R30", "descricao": "digrafo ss para s", "tipo": "regex", "padrao": r"ss", "sub": "s"},
    {"nome": "R31", "descricao": "c antes de e ou i para s", "tipo": "regex", "padrao": r"c(?=[ei])", "sub": "s"},
    {"nome": "R32", "descricao": "ch para x", "tipo": "regex", "padrao": r"ch", "sub": "x"},
]

# =========================
# BLOCO 7
# =========================

BLOCO_7 = [
    {"nome": "R33", "descricao": "m antes de tudo menos p,b", "tipo": "regex", "padrao": r"n(?=[cgjqrx])", "sub": "m"}, # só as não-coronais ou anteriores; o grupo todo pode causar muito estranhamento
    {"nome": "R34", "descricao": "n antes de p,b", "tipo": "regex", "padrao": r"m(?=[pb])", "sub": "n"},
    # {"nome": "R34a", "descricao": "ou como o", "tipo": "regex", "padrao": r"ou", "sub": "o"}, parece dificultar: "o" lido como artigo, "xamo" ? chamo !?
    {"nome": "R35", "descricao": "l pos-vocálico como u (1)", "tipo": "regex", "padrao": r"l(?=[bcdfgjmnpqrstvxz])", "sub": "u"},
    {"nome": "R36", "descricao": "l pos-vocálico como u (2)", "tipo": "regex", "padrao": r"l\b", "sub": "u"},
    {"nome": "R38", "descricao": "ei como e", "tipo": "regex", "padrao": r"ei(?=[rxgj])", "sub": "e"},
    {"nome": "R39", "descricao": "mas como mais", "tipo": "regex", "padrao": r"\bmas\b", "sub": "mais"},
    {"nome": "R40", "descricao": "n final como m", "tipo": "regex", "padrao": r"n\b", "sub": "m"},
    {"nome": "R41", "descricao": "desfazendo falsos encontros consonantais", "tipo": "regex", "padrao": r"([bdfgpt])([dnsmtzqjv])", "sub": r"\1i\2"},
    {"nome": "R41a", "descricao": "desfazendo falsos encontros consonantais com c", "tipo": "regex", "padrao": r"c([dnsmtzqj])", "sub": r"qi\1"}, #qdo c, mudar para q
    {"nome": "R42", "descricao": "desfazendo falsos encontros consonantais (2)", "tipo": "regex", "padrao": r"(m)(n)", "sub": r"\1i\2"}, 
    {"nome": "R43", "descricao": "eliminando hifens", "tipo": "regex", "padrao": r"-", "sub": r""},
    {"nome": "R44", "descricao": "acrescentando i no final de oclusivas", "tipo": "regex", "padrao": r"([bpt])\b", "sub": r"\1i"},
    # {"nome": "R45", "descricao": "acentuando e", "tipo": "regex", "padrao": r"\be\b", "sub": "e'"}, # tem que ser lá em cima por causa da conjunção 'e'
    # {"nome": "R45a", "descricao": "diferenciando nós", "tipo": "regex", "padrao": r"\bnos\b", "sub": "nois"}, # tem que ser lá em cima antes de tirar acento!? "nos casos", "nos viu" e aí nois vira 'no'is' ?
    {"nome": "R46", "descricao": "juntando palavras", "tipo": "regex", "padrao": r"\ba jente\b", "sub": "ajente"},
    {"nome": "R46a", "descricao": "juntando palavras", "tipo": "regex", "padrao": r"\bpor qe\b", "sub": "porqe"},
    # de repente, etc.!? >>> o que, de que?
]

# =========================
# FUNÇÕES GERAIS
# =========================

def juntar_blocos(*blocos):
    regras = []
    for bloco in blocos:
        regras.extend(bloco)
    return regras

def aplicar_uma_regra(texto, regra):
    if regra["tipo"] == "funcao":
        return regra["funcao"](texto)
    if regra["tipo"] == "regex":
        return re.sub(regra["padrao"], regra["sub"], texto)
    raise ValueError(f"Tipo de regra desconhecido: {regra['tipo']}")

def aplicar_regras(texto, regras):
    atual = texto.lower()
    for regra in regras:
        atual = aplicar_uma_regra(atual, regra)
    return atual

REGRAS = juntar_blocos(
    BLOCO_0,
    BLOCO_1,
    BLOCO_2,
    BLOCO_3,
    BLOCO_4,
    BLOCO_5,
    BLOCO_6,
    BLOCO_7,
)

def convert_standard_to_alternative(texto: str) -> str:
    if not texto:
        return ""
    return aplicar_regras(texto, REGRAS)
