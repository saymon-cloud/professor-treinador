"""Pre-produz a mini-aula de cada questao usando o Ollama local, gravando o
texto no campo "miniLesson" de cada questao nos arquivos JSON. Roda uma vez
(script de uso unico); o servidor NUNCA gera mini-aula ao vivo — ele so serve
o texto ja pronto gravado aqui, tornando a abertura da mini-aula instantanea.
"""
import json
import sys
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b-instruct"
FILES = ["data/fundamentos.json", "data/neuro.json", "data/teorias_cc.json", "data/desenvolvimento.json"]
BATCH_SIZE = 5

SYSTEM_PROMPT = (
    "Voce e um professor de Psicologia escrevendo mini-aulas de reforco para um "
    "banco de conteudo que sera mostrado a estudantes que errarem cada questao "
    "especifica de uma prova. Para CADA questao recebida, escreva uma mini-aula "
    "curta (entre 120 e 200 palavras), em portugues, explicando corretamente o "
    "conceito cobrado e destacando eventuais confusoes comuns relacionadas ao "
    "tema. SEMPRE que possivel, cite explicitamente o(s) autor(es)/teorico(s) "
    "associados ao conceito (use a citacao fornecida quando houver, ou nomes de "
    "autores/teoricos claramente relacionados ao tema apenas se tiver certeza) e "
    "situe a ideia na obra/teoria desse autor -- esse embasamento teorico/autoral "
    "e o foco principal da mini-aula, nao apenas repetir a resposta padrao. Nao "
    "invente citacoes, nomes ou datas que nao tenha certeza; se nao houver autor "
    "claro, apenas nao cite nenhum. Responda APENAS com um objeto JSON valido, "
    "sem texto fora dele, no formato exato: "
    '{"lessons": {"<id_da_questao>": "<texto da mini-aula>", ...}}. '
    "Inclua uma entrada para CADA id recebido."
)


def call_ollama(items):
    lines = []
    for it in items:
        lines.append(f"ID: {it['id']}")
        lines.append(f"Assunto: {it.get('subject','')}")
        lines.append(f"Pergunta: {it['question']}")
        if it.get("options"):
            for k, v in it["options"].items():
                marker = " (CORRETA)" if k == it.get("correct") else ""
                lines.append(f"  {k}) {v}{marker}")
        if it.get("modelAnswer"):
            lines.append(f"Resposta padrao: {it['modelAnswer']}")
        if it.get("explanation"):
            lines.append(f"Explicacao: {it['explanation']}")
        if it.get("keyPoints"):
            kp = "; ".join(kp.get("text", "") for kp in it["keyPoints"])
            lines.append(f"Pontos-chave esperados: {kp}")
        src = it.get("source") or {}
        if src.get("citation"):
            lines.append(f"Citacao de referencia no material: {src['citation']}")
        if src.get("document"):
            lines.append(f"Fonte no material: {src['document']}" + (f", p. {src.get('page')}" if src.get("page") else ""))
        lines.append("")
    user_prompt = "\n".join(lines)

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.4},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    content = body.get("message", {}).get("content", "")
    result = json.loads(content)
    return result.get("lessons", {})


def batches(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    total_done = 0
    total_all = 0
    for fname in FILES:
        with open(fname, "r", encoding="utf-8") as f:
            data = json.load(f)
        for section in ["objective", "discursive", "oral"]:
            total_all += len(data.get(section, []))

    for fname in FILES:
        with open(fname, "r", encoding="utf-8") as f:
            data = json.load(f)

        for section in ["objective", "discursive", "oral"]:
            questions = data.get(section, [])
            for batch in batches(questions, BATCH_SIZE):
                todo = [q for q in batch if not q.get("miniLesson")]
                if not todo:
                    total_done += len(batch)
                    continue
                attempt = 0
                lessons = None
                while attempt < 5:
                    attempt += 1
                    try:
                        lessons = call_ollama(todo)
                        break
                    except Exception as exc:
                        print(f"  erro (tentativa {attempt}) em {fname}/{section}: {exc}", flush=True)
                        time.sleep(8)
                if lessons is None:
                    print("  desistindo deste lote por enquanto (sera tentado na proxima execucao)", flush=True)
                    total_done += len(batch)
                    continue
                for q in todo:
                    lesson = str(lessons.get(q["id"], "")).strip()
                    if lesson:
                        q["miniLesson"] = lesson
                total_done += len(batch)
                print(f"[{total_done}/{total_all}] {fname} / {section} — lote de {len(batch)} pré-produzido", flush=True)
                with open(fname, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

    print("CONCLUIDO: todas as mini-aulas pré-produzidas.", flush=True)


if __name__ == "__main__":
    main()
