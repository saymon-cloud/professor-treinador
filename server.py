"""Servidor local do Professor Treinador.

Serve os arquivos estáticos do app, guarda usuários/caderno de erros em SQLite
e faz de ponte (proxy) entre o navegador e o Ollama local, para que as provas
discursiva/oral e as mini-aulas de reforço usem um modelo de linguagem rodando
100% na máquina do usuário.

Uso:
    python server.py

Depois abra http://localhost:8000 no navegador (Chrome recomendado, para o
reconhecimento de voz da Prova Oral funcionar corretamente).

Para a correção discursiva/oral por IA funcionar, é preciso ter o Ollama
instalado e rodando (https://ollama.com) com o modelo configurado abaixo já
baixado:
    ollama pull qwen2.5:7b-instruct
Se o Ollama não estiver disponível, o app cai automaticamente para a correção
local por padrão de resposta.

As mini-aulas do caderno de erros NÃO são geradas na hora: elas são
pré-produzidas offline pelo script generate_mini_lessons.py (que grava o texto
em cada questão dos arquivos data/*.json) para que abrir uma mini-aula seja
instantâneo, sem esperar a IA responder.
"""
import base64
import datetime
import http.server
import json
import os
import re
import socketserver
import sqlite3
import urllib.error
import urllib.request
import webbrowser

PORT = int(os.environ.get("PORT", 8000))
DB_PATH = "treinador.db"

# Se DATABASE_URL estiver definida (ex.: deploy no Render + Postgres do
# Supabase/Neon), o app usa Postgres em vez do arquivo SQLite local — assim os
# dados sobrevivem a cada novo deploy. Localmente, sem essa variável, continua
# tudo em SQLite, sem precisar instalar nada a mais.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
USE_POSTGRES = bool(DATABASE_URL)
if USE_POSTGRES:
    import psycopg
    import psycopg.rows

# Se BASIC_AUTH_USER/BASIC_AUTH_PASS estiverem definidas (recomendado ao expor
# o app publicamente, ex.: no Render), todo acesso passa a exigir esse usuário/
# senha (autenticação HTTP Basic, suportada nativamente pelo navegador).
# Localmente, sem essas variáveis, o app continua sem exigir login extra.
BASIC_AUTH_USER = os.environ.get("BASIC_AUTH_USER", "")
BASIC_AUTH_PASS = os.environ.get("BASIC_AUTH_PASS", "")
AUTH_ENABLED = bool(BASIC_AUTH_USER and BASIC_AUTH_PASS)

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b-instruct"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

GRADE_SYSTEM_PROMPT = (
    "Você é um professor avaliador de Psicologia, rigoroso mas justo. "
    "Você recebe uma pergunta de prova, a resposta padrão esperada, uma lista de "
    "pontos-chave que uma resposta completa deveria abordar, e a resposta escrita "
    "por um candidato (pode ser uma transcrição de fala, com eventuais erros de "
    "transcrição, hesitações ou repetições - ignore esses ruídos e avalie o conteúdo). "
    "Avalie a resposta do candidato atribuindo uma nota de 0 a 10 (pode usar uma casa "
    "decimal), considerando corretas paráfrases e sinônimos que tenham o mesmo "
    "significado dos pontos-chave, mesmo com palavras diferentes das do gabarito. "
    "Penalize afirmações factualmente erradas, invertidas ou contraditórias em relação "
    "à resposta padrão, mesmo que usem o vocabulário certo. Penalize respostas vazias, "
    "irrelevantes ou que apenas repetem a pergunta sem responder. "
    "Responda APENAS com um objeto JSON válido, sem nenhum texto antes ou depois, "
    "sem markdown, no formato exato: "
    '{"score": <número de 0 a 10>, "feedback": "<explicação breve em português, '
    "2 a 4 frases, dizendo o que a resposta acertou e o que faltou ou está incorreto>\"}"
)

# ---------- Banco de dados (usuários e caderno de erros) ----------
# Suporta SQLite (padrão local, zero configuração) e Postgres (quando
# DATABASE_URL está definida, ex.: no deploy online). As funções abaixo usam
# sempre "?" como placeholder; run() converte para "%s" no modo Postgres.

def db():
    if USE_POSTGRES:
        return psycopg.connect(DATABASE_URL, row_factory=psycopg.rows.dict_row)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def run(conn, sql, params=()):
    if USE_POSTGRES:
        cur = conn.cursor()
        cur.execute(sql.replace("?", "%s"), params)
        return cur
    return conn.execute(sql, params)


def init_db():
    conn = db()
    if USE_POSTGRES:
        run(conn, """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        run(conn, """
            CREATE TABLE IF NOT EXISTS errors (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                semester TEXT,
                discipline TEXT,
                subject TEXT,
                mode TEXT,
                question_id TEXT,
                question_text TEXT,
                user_answer TEXT,
                correct_answer TEXT,
                score REAL,
                model_answer TEXT,
                key_points_json TEXT,
                source_json TEXT,
                mini_lesson TEXT,
                resolved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
    else:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                semester TEXT,
                discipline TEXT,
                subject TEXT,
                mode TEXT,
                question_id TEXT,
                question_text TEXT,
                user_answer TEXT,
                correct_answer TEXT,
                score REAL,
                model_answer TEXT,
                key_points_json TEXT,
                source_json TEXT,
                mini_lesson TEXT,
                resolved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            """
        )
        # Migração leve para bancos SQLite criados antes do campo mini_lesson existir.
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(errors)").fetchall()]
        if "mini_lesson" not in cols:
            conn.execute("ALTER TABLE errors ADD COLUMN mini_lesson TEXT")
    conn.commit()
    conn.close()


def now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


VALID_NAME = re.compile(r"^[^\x00-\x1f]{1,60}$")


def get_or_create_user(name):
    name = (name or "").strip()
    if not VALID_NAME.match(name):
        raise ValueError("Nome inválido.")
    conn = db()
    try:
        row = run(conn, "SELECT id, name FROM users WHERE name = ?", (name,)).fetchone()
        if row:
            return dict(row)
        run(conn, "INSERT INTO users(name, created_at) VALUES (?, ?)", (name, now_iso()))
        conn.commit()
        row = run(conn, "SELECT id, name FROM users WHERE name = ?", (name,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_users():
    conn = db()
    try:
        order_by = "LOWER(u.name)" if USE_POSTGRES else "u.name COLLATE NOCASE"
        rows = run(conn,
            "SELECT u.id, u.name, "
            "(SELECT COUNT(*) FROM errors e WHERE e.user_id = u.id AND e.resolved = 0) AS open_errors "
            "FROM users u ORDER BY " + order_by
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def insert_error(payload):
    conn = db()
    try:
        sql = """
            INSERT INTO errors (
                user_id, semester, discipline, subject, mode, question_id, question_text,
                user_answer, correct_answer, score, model_answer, key_points_json,
                source_json, mini_lesson, resolved, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
        """
        params = (
            payload.get("userId"),
            payload.get("semester", ""),
            payload.get("discipline", ""),
            payload.get("subject", ""),
            payload.get("mode", ""),
            payload.get("questionId", ""),
            payload.get("question", ""),
            payload.get("userAnswer", ""),
            payload.get("correctAnswer", ""),
            payload.get("score"),
            payload.get("modelAnswer", ""),
            json.dumps(payload.get("keyPoints", []), ensure_ascii=False),
            json.dumps(payload.get("source"), ensure_ascii=False) if payload.get("source") else None,
            payload.get("miniLesson", ""),
            now_iso(),
        )
        if USE_POSTGRES:
            cur = run(conn, sql + " RETURNING id", params)
            new_id = cur.fetchone()["id"]
        else:
            cur = run(conn, sql, params)
            new_id = cur.lastrowid
        conn.commit()
        return new_id
    finally:
        conn.close()


def list_errors(user_id, resolved=None):
    conn = db()
    try:
        q = "SELECT * FROM errors WHERE user_id = ?"
        params = [user_id]
        if resolved is not None:
            q += " AND resolved = ?"
            params.append(1 if resolved else 0)
        q += " ORDER BY created_at DESC"
        rows = run(conn, q, params).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            try:
                d["keyPoints"] = json.loads(d.pop("key_points_json") or "[]")
            except Exception:
                d["keyPoints"] = []
            src = d.pop("source_json")
            try:
                d["source"] = json.loads(src) if src else None
            except Exception:
                d["source"] = None
            out.append(d)
        return out
    finally:
        conn.close()


def set_error_resolved(error_id, resolved):
    conn = db()
    try:
        run(conn, "UPDATE errors SET resolved = ? WHERE id = ?", (1 if resolved else 0, error_id))
        conn.commit()
    finally:
        conn.close()


def delete_error(error_id):
    conn = db()
    try:
        run(conn, "DELETE FROM errors WHERE id = ?", (error_id,))
        conn.commit()
    finally:
        conn.close()


# ---------- Ollama ----------

def ollama_request(path, payload=None, method="GET", timeout=6):
    url = OLLAMA_HOST + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ollama_available():
    try:
        data = ollama_request("/api/tags", timeout=3)
        names = [m.get("name", "") for m in data.get("models", [])]
        base = OLLAMA_MODEL.split(":")[0]
        return any(n == OLLAMA_MODEL or n.startswith(base + ":") for n in names)
    except Exception:
        return False


def grade_with_llm(question, model_answer, key_points, user_answer):
    key_points_text = "\n".join(
        "- " + str(kp.get("text", "")) for kp in (key_points or []) if kp.get("text")
    )
    user_prompt = (
        "Pergunta da prova:\n" + question + "\n\n"
        "Resposta padrão esperada:\n" + model_answer + "\n\n"
        "Pontos-chave de uma resposta completa:\n" + key_points_text + "\n\n"
        'Resposta do candidato:\n"' + user_answer + '"\n\n'
        "Avalie a resposta do candidato agora."
    )
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": GRADE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.2},
    }
    body = ollama_request("/api/chat", payload, method="POST", timeout=120)
    content = body.get("message", {}).get("content", "")
    result = json.loads(content)
    score = float(result.get("score", 0))
    score = max(0.0, min(10.0, score))
    feedback = str(result.get("feedback", "")).strip()
    return {"score": round(score, 1), "feedback": feedback, "engine": "llm", "model": OLLAMA_MODEL}


# ---------- HTTP handler ----------

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _send_json(self, status, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")
        return json.loads(text) if text.strip() else {}

    def _query(self):
        from urllib.parse import urlparse, parse_qs
        return parse_qs(urlparse(self.path).query)

    def _check_auth(self):
        """Exige usuário/senha (HTTP Basic) quando BASIC_AUTH_USER/PASS estão
        configuradas — usado ao expor o app publicamente. Sem essas variáveis
        (uso local padrão), libera tudo sem pedir nada."""
        if not AUTH_ENABLED:
            return True
        expected = "Basic " + base64.b64encode(
            f"{BASIC_AUTH_USER}:{BASIC_AUTH_PASS}".encode("utf-8")
        ).decode("ascii")
        if self.headers.get("Authorization", "") == expected:
            return True
        body = b"Autenticacao necessaria."
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Professor Treinador"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return False

    def do_GET(self):
        if not self._check_auth():
            return
        from urllib.parse import urlparse
        path = urlparse(self.path).path

        if path == "/api/health":
            self._send_json(200, {"available": ollama_available(), "model": OLLAMA_MODEL})
            return

        if path == "/api/users":
            try:
                self._send_json(200, {"users": list_users()})
            except Exception as exc:
                self._send_json(500, {"error": str(exc)})
            return

        if path == "/api/errors":
            try:
                qs = self._query()
                user_id = int(qs.get("user_id", ["0"])[0])
                resolved_param = qs.get("resolved", [None])[0]
                resolved = None
                if resolved_param is not None:
                    resolved = resolved_param == "1"
                self._send_json(200, {"errors": list_errors(user_id, resolved)})
            except Exception as exc:
                self._send_json(500, {"error": str(exc)})
            return

        super().do_GET()

    def do_POST(self):
        if not self._check_auth():
            return
        from urllib.parse import urlparse
        path = urlparse(self.path).path

        try:
            if path == "/api/grade":
                payload = self._read_json_body()
                result = grade_with_llm(
                    payload.get("question", ""),
                    payload.get("modelAnswer", ""),
                    payload.get("keyPoints", []),
                    payload.get("userAnswer", ""),
                )
                self._send_json(200, result)
                return

            if path == "/api/login":
                payload = self._read_json_body()
                user = get_or_create_user(payload.get("name", ""))
                self._send_json(200, {"user": user})
                return

            if path == "/api/errors":
                payload = self._read_json_body()
                if not payload.get("userId"):
                    self._send_json(400, {"error": "userId é obrigatório"})
                    return
                error_id = insert_error(payload)
                self._send_json(200, {"id": error_id})
                return

            if path == "/api/errors/resolve":
                payload = self._read_json_body()
                set_error_resolved(payload.get("id"), payload.get("resolved", True))
                self._send_json(200, {"ok": True})
                return

            if path == "/api/errors/delete":
                payload = self._read_json_body()
                delete_error(payload.get("id"))
                self._send_json(200, {"ok": True})
                return

            self.send_error(404, "Not found")
        except urllib.error.URLError as exc:
            self._send_json(502, {"error": "Não foi possível conectar ao Ollama: " + str(exc)})
        except Exception as exc:
            self._send_json(502, {"error": str(exc)})

    def log_message(self, format, *args):
        # Silencia o log de requisições de polling (deixa o console mais limpo).
        # args[0] nem sempre é string (ex.: send_error loga o código HTTP como int),
        # então convertemos com str() antes de checar substring.
        if args and "/api/health" in str(args[0]):
            return
        super().log_message(format, *args)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    init_db()
    url = f"http://localhost:{PORT}"
    # Em ambiente de nuvem (Postgres configurado) não faz sentido tentar abrir
    # um navegador local nem tratar "porta ocupada" como "já está rodando".
    is_cloud = USE_POSTGRES

    if not is_cloud:
        try:
            httpd = ThreadingHTTPServer(("", PORT), Handler)
        except OSError:
            print(f"O Professor Treinador já está rodando em {url}. Abrindo no navegador...")
            try:
                webbrowser.open(url)
            except Exception:
                pass
            return
    else:
        httpd = ThreadingHTTPServer(("", PORT), Handler)

    with httpd:
        print(f"Professor Treinador rodando em {url}" if not is_cloud else f"Professor Treinador rodando na porta {PORT}")
        print("Banco de dados: " + ("Postgres (nuvem)" if USE_POSTGRES else f"SQLite local ({DB_PATH})"))
        print("Autenticação HTTP Basic: " + ("ativa" if AUTH_ENABLED else "desativada"))
        if ollama_available():
            print(f"IA de correção ativa: Ollama + {OLLAMA_MODEL}")
        else:
            print("IA de correção indisponível (Ollama não encontrado ou modelo não baixado).")
            if not is_cloud:
                print(f"Para ativar, instale o Ollama e rode: ollama pull {OLLAMA_MODEL}")
            print("O app funcionará normalmente com a correção local por padrão de resposta.")
        print("Pressione Ctrl+C para parar.")
        if not is_cloud:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
