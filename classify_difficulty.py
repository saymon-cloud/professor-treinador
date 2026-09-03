"""Classifica a dificuldade (baixo/medio/dificil) de todas as questoes usando o Ollama local.
Roda uma vez, grava o campo "difficulty" direto nos arquivos JSON. Script de uso unico.
"""
import json
import sys
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b-instruct"
FILES = ["data/fundamentos.json", "data/neuro.json", "data/teorias_cc.json", "data/desenvolvimento.json"]
BATCH_SIZE = 10

SYSTEM_PROMPT = (
    "Voce e um professor experiente de Psicologia que classifica a dificuldade de questoes de prova. "
    "Para cada questao recebida, classifique a dificuldade em uma destas tres categorias: "
    '"baixo" (definicao/conceito basico, resposta direta, memorizacao simples), '
    '"medio" (exige compreender relacoes entre conceitos ou aplicar o conceito a um exemplo/caso), '
    '"dificil" (exige sintetizar varios conceitos, detalhes tecnicos especificos, ou distinguir alternativas '
    'muito parecidas / varios pontos-chave interligados). '
    "Responda APENAS com um objeto JSON valido no formato exato: "
    '{"difficulties": {"<id_da_questao>": "baixo|medio|dificil", ...}}. '
    "Inclua uma entrada para CADA id recebido, sem texto fora do JSON."
)


def call_ollama(items):
    lines = []
    for it in items:
        lines.append(f"ID: {it['id']}")
        lines.append(f"Pergunta: {it['question']}")
        if it.get("options"):
            for k, v in it["options"].items():
                lines.append(f"  {k}) {v}")
        if it.get("modelAnswer"):
            lines.append(f"Resposta padrao: {it['modelAnswer']}")
        if it.get("keyPoints"):
            kp = "; ".join(kp.get("text", "") for kp in it["keyPoints"])
            lines.append(f"Pontos-chave esperados: {kp}")
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
        "options": {"temperature": 0.1},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    content = body.get("message", {}).get("content", "")
    result = json.loads(content)
    return result.get("difficulties", {})


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
        path = fname
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        changed = False
        for section in ["objective", "discursive", "oral"]:
            questions = data.get(section, [])
            for batch in batches(questions, BATCH_SIZE):
                todo = [q for q in batch if not q.get("difficulty")]
                if not todo:
                    total_done += len(batch)
                    continue
                attempt = 0
                diffs = None
                while attempt < 5:
                    attempt += 1
                    try:
                        diffs = call_ollama(todo)
                        break
                    except Exception as exc:
                        print(f"  erro (tentativa {attempt}) em {fname}/{section}: {exc}", flush=True)
                        time.sleep(8)
                if diffs is None:
                    print(f"  desistindo deste lote por enquanto (sera tentado na proxima execucao)", flush=True)
                    total_done += len(batch)
                    continue
                for q in todo:
                    d = diffs.get(q["id"])
                    if d not in ("baixo", "medio", "dificil"):
                        d = "medio"
                    q["difficulty"] = d
                changed = True
                total_done += len(batch)
                print(f"[{total_done}/{total_all}] {fname} / {section} — lote de {len(batch)} classificado", flush=True)
                # salva incrementalmente para nao perder progresso
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        if not changed:
            print(f"{fname}: nada a fazer (ja classificado)", flush=True)

    print("CONCLUIDO: todas as questoes classificadas.", flush=True)


if __name__ == "__main__":
    main()
