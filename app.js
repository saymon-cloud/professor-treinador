/* Professor Treinador — lógica principal (vanilla JS, sem dependências) */

const state = {
  currentUser: null,       // {id, name}
  manifest: null,
  banks: {},                // disciplineId -> parsed JSON
  currentSemester: null,    // manifest semester object
  currentDiscipline: null,  // {id, file, icon, title}
  selectedSubjects: new Set(), // seleção em andamento na tela de assuntos
  currentSubjects: [],      // assuntos confirmados para a sessão (1 ou mais)
  currentMode: "objective",
  currentDifficulty: "all",
  questions: [],
  index: 0,
  answers: [],
  recognition: null,
  finalTranscript: "",
};

const DIFF_LABEL = { baixo: "Baixo", medio: "Médio", dificil: "Difícil" };

// ---------- Utilidades de texto / correção heurística ----------

const STOPWORDS = new Set([
  "de","a","o","que","e","do","da","em","um","uma","para","com","nao","os","as","dos","das",
  "no","na","por","mais","como","mas","se","ao","ele","ela","seu","sua","ou","quando","muito",
  "tambem","so","pelo","pela","ate","isso","entre","depois","sem","mesmo","aos","seus","quem",
  "nas","me","esse","eles","voce","essa","nem","suas","meu","as","minha","pelos","elas","seja",
  "qual","sera","nos","tenho","lhe","deles","essas","esses","pelas","este","dele","tu","te",
  "voces","vos","lhes","meus","minhas","teu","tua","teus","tuas","nosso","nossa","nossos",
  "nossas","dela","delas","esta","estes","estas","aquele","aquela","aqueles","aquelas","isto",
  "aquilo","estou","esta","estamos","estao","tem","ser","sao","era","foi","fica","fico","tudo",
  "onde","cada","pode","pois","dessa","desse","disso","assim","entao","porque","porem","apenas",
  "sobre","dentro","fora","diante","atraves","ainda","sempre","nunca","todos","todas","alguns",
  "algumas","outro","outra","outros","outras","ja","la","aqui","aquilo","numa","num"
]);

function normalizeText(str) {
  return (str || "")
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function stem(word) {
  return word.length > 6 ? word.slice(0, 6) : word;
}

function significantStems(str) {
  return normalizeText(str)
    .split(" ")
    .filter(w => w.length >= 4 && !STOPWORDS.has(w))
    .map(stem);
}

function keywordMatches(keyword, normUserText, userStemSet) {
  const normKeyword = normalizeText(keyword);
  if (!normKeyword) return false;
  if (normUserText.includes(normKeyword)) return true;
  const compactUser = normUserText.replace(/\s+/g, "");
  const compactKeyword = normKeyword.replace(/\s+/g, "");
  if (compactKeyword.length >= 6 && compactUser.includes(compactKeyword)) return true;
  const kwStems = normKeyword.split(" ").filter(w => w.length >= 4 && !STOPWORDS.has(w)).map(stem);
  if (kwStems.length === 0) return false;
  const hits = kwStems.filter(s => userStemSet.has(s)).length;
  const threshold = kwStems.length === 1 ? 1 : Math.ceil(kwStems.length * 0.6);
  return hits >= threshold;
}

function gradeOpenAnswer(userText, keyPoints, modelAnswer) {
  const normUser = " " + normalizeText(userText) + " ";
  const userStemSet = new Set(significantStems(userText));
  let totalWeight = 0, gotWeight = 0;
  const details = [];
  (keyPoints || []).forEach(kp => {
    const weight = kp.weight || 1;
    totalWeight += weight;
    const matched = (kp.keywords || []).some(k => keywordMatches(k, normUser, userStemSet));
    if (matched) gotWeight += weight;
    details.push({ text: kp.text, matched });
  });
  const wordCount = normalizeText(userText).split(" ").filter(Boolean).length;
  let score = totalWeight > 0 ? (gotWeight / totalWeight) * 10 : 0;

  if (modelAnswer && wordCount >= 6) {
    const modelStems = new Set(significantStems(modelAnswer));
    if (modelStems.size > 0) {
      let overlap = 0;
      modelStems.forEach(s => { if (userStemSet.has(s)) overlap++; });
      const relevanceRatio = overlap / modelStems.size;
      const relevanceBonus = Math.min(3, relevanceRatio * 6) * (1 - score / 10);
      score = Math.min(10, score + relevanceBonus);
    }
  }

  if (wordCount < 6) score = Math.min(score, 2);
  score = Math.round(score * 10) / 10;
  return { score, details, wordCount };
}

function scoreClass(score) {
  if (score >= 7) return "good";
  if (score >= 4) return "mid";
  return "low";
}

function escapeHtml(str) {
  return (str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderSourceLine(source) {
  if (!source || !source.document) return "";
  let line = "📄 Fonte: " + escapeHtml(source.document);
  if (source.page) line += ", p. " + escapeHtml(String(source.page));
  if (source.citation) line += " — " + escapeHtml(source.citation);
  return `<div class="source-line">${line}</div>`;
}

// ---------- Correção por IA (Llama/Qwen local via Ollama, com fallback local) ----------

let aiAvailable = null;
let aiModelName = null;

async function checkAI() {
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    aiAvailable = !!data.available;
    aiModelName = data.model || null;
  } catch (e) {
    aiAvailable = false;
  }
  updateAIBadge();
}

function updateAIBadge() {
  const el = document.getElementById("aiBadge");
  if (!el) return;
  if (aiAvailable) {
    el.textContent = "🤖 IA (" + (aiModelName || "modelo local") + ") ativa";
    el.className = "ai-badge ai-on";
  } else if (aiAvailable === false) {
    el.textContent = "⚙️ IA indisponível";
    el.className = "ai-badge ai-off";
  } else {
    el.textContent = "";
    el.className = "ai-badge";
  }
}

async function gradeWithLLM(question, modelAnswer, keyPoints, userAnswer) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120000);
  try {
    const res = await fetch("/api/grade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, modelAnswer, keyPoints, userAnswer }),
      signal: controller.signal,
    });
    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw new Error(errBody.error || ("Falha na avaliação por IA (" + res.status + ")"));
    }
    const data = await res.json();
    if (typeof data.score !== "number") throw new Error("Resposta de IA em formato inválido");
    return data;
  } finally {
    clearTimeout(timeoutId);
  }
}

async function gradeAnswer(q, userText) {
  if (aiAvailable !== false) {
    try {
      const llm = await gradeWithLLM(q.question, q.modelAnswer, q.keyPoints, userText);
      aiAvailable = true;
      updateAIBadge();
      return { score: llm.score, feedback: llm.feedback, engine: "llm", model: llm.model };
    } catch (err) {
      console.warn("Avaliação por IA indisponível, usando correção local:", err);
      aiAvailable = false;
      updateAIBadge();
    }
  }
  const local = gradeOpenAnswer(userText, q.keyPoints, q.modelAnswer);
  return { score: local.score, details: local.details, engine: "heuristic" };
}

// ---------- Login / usuário ----------

function saveUserLocal(user) {
  try { localStorage.setItem("treinador_user", JSON.stringify(user)); } catch (e) {}
}
function loadUserLocal() {
  try {
    const raw = localStorage.getItem("treinador_user");
    return raw ? JSON.parse(raw) : null;
  } catch (e) { return null; }
}
function clearUserLocal() {
  try { localStorage.removeItem("treinador_user"); } catch (e) {}
}

function updateUserChip() {
  const chip = document.getElementById("userChip");
  const notebookBtn = document.getElementById("notebookBtn");
  if (state.currentUser) {
    chip.textContent = "👤 " + state.currentUser.name + " (trocar)";
    chip.classList.remove("hidden");
    notebookBtn.classList.remove("hidden");
    refreshNotebookCount();
  } else {
    chip.classList.add("hidden");
    notebookBtn.classList.add("hidden");
  }
}

async function refreshNotebookCount() {
  if (!state.currentUser) return;
  try {
    const res = await fetch(`/api/errors?user_id=${state.currentUser.id}&resolved=0`);
    const data = await res.json();
    const n = (data.errors || []).length;
    const badge = document.getElementById("notebookCount");
    if (n > 0) {
      badge.textContent = String(n);
      badge.classList.remove("hidden");
    } else {
      badge.classList.add("hidden");
    }
  } catch (e) {}
}

async function loadUsersIntoLogin() {
  const grid = document.getElementById("userGrid");
  grid.innerHTML = "<p class='subtitle'>Carregando usuários...</p>";
  try {
    const res = await fetch("/api/users");
    const data = await res.json();
    grid.innerHTML = "";
    (data.users || []).forEach(u => {
      const card = document.createElement("button");
      card.className = "user-card";
      const initial = (u.name || "?").trim().charAt(0).toUpperCase();
      card.innerHTML = `
        <span class="user-avatar">${escapeHtml(initial)}</span>
        <span class="user-name">${escapeHtml(u.name)}</span>
        <span class="user-meta">${u.open_errors > 0 ? u.open_errors + " erro(s) a revisar" : "caderno em dia"}</span>
      `;
      card.addEventListener("click", () => doLogin(u.name));
      grid.appendChild(card);
    });
    if (!(data.users || []).length) {
      grid.innerHTML = "<p class='subtitle'>Nenhum usuário ainda. Crie o primeiro abaixo.</p>";
    }
  } catch (e) {
    grid.innerHTML = "<p class='subtitle'>Não foi possível carregar usuários (servidor offline?).</p>";
  }
}

// Faz (ou refaz) login pelo nome, sem alertas — usado para revalidar um usuário
// salvo localmente contra o banco de dados atual do servidor (ex.: depois de o
// servidor ser reiniciado com um banco novo/limpo). Retorna true em caso de sucesso.
async function doLoginSilently(name) {
  name = (name || "").trim();
  if (!name) return false;
  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    state.currentUser = data.user;
    saveUserLocal(data.user);
    updateUserChip();
    return true;
  } catch (e) {
    return false;
  }
}

async function doLogin(name) {
  const ok = await doLoginSilently(name);
  if (ok) {
    showScreen("screen-semesters");
    renderSemesters();
  } else {
    alert("Não foi possível entrar. Verifique se o servidor está rodando.");
  }
}

document.getElementById("newUserBtn").addEventListener("click", () => {
  doLogin(document.getElementById("newUserName").value);
});
document.getElementById("newUserName").addEventListener("keydown", (e) => {
  if (e.key === "Enter") doLogin(document.getElementById("newUserName").value);
});

document.getElementById("userChip").addEventListener("click", () => {
  state.currentUser = null;
  clearUserLocal();
  updateUserChip();
  showScreen("screen-login");
  setCrumbs("");
  loadUsersIntoLogin();
});

document.getElementById("notebookBtn").addEventListener("click", () => {
  showScreen("screen-notebook");
  setCrumbs("Caderno de erros");
  loadNotebook("open");
});
document.getElementById("notebookFromResultsBtn").addEventListener("click", () => {
  showScreen("screen-notebook");
  setCrumbs("Caderno de erros");
  loadNotebook("open");
});

// ---------- Registro de erros ----------

async function recordError({ q, mode, userAnswer, correctAnswer, score }) {
  if (!state.currentUser) {
    console.warn("Erro não registrado: nenhum usuário logado.");
    return;
  }
  try {
    const res = await fetch("/api/errors", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: state.currentUser.id,
        semester: state.currentSemester ? state.currentSemester.label : "",
        discipline: state.currentDiscipline ? state.currentDiscipline.title : "",
        subject: q.subject || q.topic || "",
        mode,
        questionId: q.id,
        question: q.question,
        userAnswer,
        correctAnswer,
        score,
        modelAnswer: q.modelAnswer || q.explanation || "",
        keyPoints: q.keyPoints || [],
        source: q.source || null,
        miniLesson: q.miniLesson || "",
      }),
    });
    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      // Usuário local desatualizado (ex.: banco de dados foi recriado) — revalida e tenta de novo uma vez.
      if (res.status === 502 && /usuário|user|foreign key|constraint/i.test(errBody.error || "")) {
        const revalidated = await doLoginSilently(state.currentUser.name);
        if (revalidated) {
          await recordError({ q, mode, userAnswer, correctAnswer, score });
          return;
        }
      }
      console.error("Falha ao registrar erro no caderno:", res.status, errBody.error || "");
      return;
    }
    refreshNotebookCount();
  } catch (e) {
    console.warn("Não foi possível registrar o erro (rede/servidor indisponível):", e);
  }
}

// ---------- Navegação de telas ----------

function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo(0, 0);
}

function setCrumbs(text) {
  document.getElementById("crumbs").textContent = text || "";
}

function crumbsPath(parts) {
  setCrumbs(parts.filter(Boolean).join("  ›  "));
}

document.querySelectorAll("[data-back]").forEach(btn => {
  btn.addEventListener("click", () => {
    if (state.recognition) { try { state.recognition.stop(); } catch (e) {} }
    window.speechSynthesis && window.speechSynthesis.cancel();
    showScreen(btn.dataset.back);
    if (btn.dataset.back === "screen-semesters") { setCrumbs(""); }
    else if (btn.dataset.back === "screen-disciplines") { crumbsPath([state.currentSemester && state.currentSemester.label]); }
    else if (btn.dataset.back === "screen-subjects") { crumbsPath([state.currentSemester && state.currentSemester.label, state.currentDiscipline && state.currentDiscipline.title]); }
    else if (btn.dataset.back === "screen-subject-detail") { crumbsPath([state.currentSemester && state.currentSemester.label, state.currentDiscipline && state.currentDiscipline.title, subjectsLabel()]); }
  });
});

document.getElementById("brandHome").addEventListener("click", () => {
  window.speechSynthesis && window.speechSynthesis.cancel();
  if (!state.currentUser) { showScreen("screen-login"); return; }
  showScreen("screen-semesters");
  setCrumbs("");
  renderSemesters();
});

// ---------- Carregamento de dados ----------

async function loadManifest() {
  if (state.manifest) return state.manifest;
  const res = await fetch("data/manifest.json");
  state.manifest = await res.json();
  return state.manifest;
}

async function loadBank(discipline) {
  if (state.banks[discipline.id]) return state.banks[discipline.id];
  const res = await fetch(discipline.file);
  if (!res.ok) throw new Error("Falha ao carregar " + discipline.file);
  const json = await res.json();
  state.banks[discipline.id] = json;
  return json;
}

// ---------- Tela: semestres ----------

async function renderSemesters() {
  await loadManifest();
  const grid = document.getElementById("semesterGrid");
  grid.innerHTML = "";
  state.manifest.semesters.forEach(sem => {
    const card = document.createElement("button");
    card.className = "semester-card" + (sem.available ? "" : " disabled");
    card.innerHTML = `
      <span class="semester-title">${escapeHtml(sem.label)}</span>
      <span class="semester-desc">${sem.available ? (sem.disciplines.length + " disciplinas disponíveis") : "Em breve"}</span>
    `;
    if (sem.available) {
      card.addEventListener("click", () => selectSemester(sem));
    }
    grid.appendChild(card);
  });
}

function selectSemester(sem) {
  state.currentSemester = sem;
  document.getElementById("semesterTitle").textContent = sem.label;
  crumbsPath([sem.label]);
  renderDisciplines(sem);
  showScreen("screen-disciplines");
}

// ---------- Tela: disciplinas ----------

function renderDisciplines(sem) {
  const grid = document.getElementById("disciplineGrid");
  grid.innerHTML = "";
  sem.disciplines.forEach(disc => {
    const btn = document.createElement("button");
    btn.className = "disc-card";
    btn.innerHTML = `
      <span class="disc-icon">${disc.icon}</span>
      <span class="disc-title">${escapeHtml(disc.title)}</span>
      <span class="disc-desc">Carregando banco de questões...</span>
    `;
    btn.addEventListener("click", () => selectDiscipline(disc));
    grid.appendChild(btn);

    loadBank(disc).then(bank => {
      const objN = (bank.objective || []).length;
      const discN = (bank.discursive || []).length;
      const oralN = (bank.oral || []).length;
      const descEl = btn.querySelector(".disc-desc");
      if (descEl) descEl.outerHTML = `<span class="disc-stats">${objN} objetivas · ${discN} discursivas · ${oralN} orais</span>`;
    }).catch(() => {
      const descEl = btn.querySelector(".disc-desc");
      if (descEl) descEl.textContent = "Erro ao carregar (rode via server.py)";
    });
  });
}

async function selectDiscipline(disc) {
  state.currentDiscipline = disc;
  document.getElementById("disciplineTitleSubjects").textContent = disc.title;
  crumbsPath([state.currentSemester.label, disc.title]);
  await loadBank(disc);
  state.selectedSubjects = new Set();
  renderSubjects();
  showScreen("screen-subjects");
}

// ---------- Tela: assuntos (seleção múltipla) ----------

function collectSubjects(bank) {
  const map = {};
  ["objective", "discursive", "oral"].forEach(mode => {
    (bank[mode] || []).forEach(q => {
      const subj = q.subject || q.topic || "Geral";
      if (!map[subj]) map[subj] = { objective: [], discursive: [], oral: [] };
      map[subj][mode].push(q);
    });
  });
  return map;
}

function diffCounts(questions) {
  const counts = { baixo: 0, medio: 0, dificil: 0 };
  questions.forEach(q => {
    const d = ["baixo", "medio", "dificil"].includes(q.difficulty) ? q.difficulty : "medio";
    counts[d]++;
  });
  return counts;
}

function renderSubjects() {
  const bank = state.banks[state.currentDiscipline.id];
  const subjectsMap = collectSubjects(bank);
  const grid = document.getElementById("subjectGrid");
  grid.innerHTML = "";

  Object.keys(subjectsMap).sort((a, b) => a.localeCompare(b, "pt-BR")).forEach(subject => {
    const buckets = subjectsMap[subject];
    const all = [...buckets.objective, ...buckets.discursive, ...buckets.oral];
    const dc = diffCounts(all);
    const badges = ["baixo", "medio", "dificil"]
      .filter(d => dc[d] > 0)
      .map(d => `<span class="diff-badge ${d}">${DIFF_LABEL[d]} ${dc[d]}</span>`)
      .join("");

    const card = document.createElement("button");
    card.className = "subject-card" + (state.selectedSubjects.has(subject) ? " selected" : "");
    card.dataset.subject = subject;
    card.innerHTML = `
      <span class="subject-checkbox">✓</span>
      <span class="subject-title">${escapeHtml(subject)}</span>
      <span class="subject-total">${all.length} questões · ${buckets.objective.length} obj · ${buckets.discursive.length} disc · ${buckets.oral.length} oral</span>
      <div class="diff-badges">${badges}</div>
    `;
    card.addEventListener("click", () => toggleSubject(subject, card));
    grid.appendChild(card);
  });

  updateSubjectsActionBar();
}

function toggleSubject(subject, cardEl) {
  if (state.selectedSubjects.has(subject)) {
    state.selectedSubjects.delete(subject);
    cardEl.classList.remove("selected");
  } else {
    state.selectedSubjects.add(subject);
    cardEl.classList.add("selected");
  }
  updateSubjectsActionBar();
}

function updateSubjectsActionBar() {
  const n = state.selectedSubjects.size;
  document.getElementById("subjectsSelectedCount").textContent =
    n === 0 ? "Nenhum assunto selecionado" : n === 1 ? "1 assunto selecionado" : `${n} assuntos selecionados`;
  document.getElementById("subjectsContinueBtn").disabled = n === 0;
}

document.getElementById("subjectsSelectAll").addEventListener("click", () => {
  document.querySelectorAll("#subjectGrid .subject-card").forEach(card => {
    state.selectedSubjects.add(card.dataset.subject);
    card.classList.add("selected");
  });
  updateSubjectsActionBar();
});

document.getElementById("subjectsClearAll").addEventListener("click", () => {
  state.selectedSubjects.clear();
  document.querySelectorAll("#subjectGrid .subject-card").forEach(card => card.classList.remove("selected"));
  updateSubjectsActionBar();
});

document.getElementById("subjectsContinueBtn").addEventListener("click", () => {
  if (state.selectedSubjects.size === 0) return;
  state.currentSubjects = [...state.selectedSubjects];
  state.currentMode = "objective";
  state.currentDifficulty = "all";
  document.getElementById("subjectTitle").textContent = subjectsLabel();
  document.getElementById("subjectDisciplineLabel").textContent = state.currentDiscipline.title;
  crumbsPath([state.currentSemester.label, state.currentDiscipline.title, subjectsLabel()]);
  renderSubjectDetail();
  showScreen("screen-subject-detail");
});

// ---------- Tela: assunto(s) + abas de modo + dificuldade ----------

function subjectsLabel() {
  const subs = state.currentSubjects;
  if (!subs || subs.length === 0) return "";
  if (subs.length === 1) return subs[0];
  if (subs.length <= 3) return subs.join(" + ");
  return `${subs.length} assuntos selecionados`;
}

function currentSubjectPool(mode) {
  const bank = state.banks[state.currentDiscipline.id];
  const subs = new Set(state.currentSubjects);
  return (bank[mode] || []).filter(q => subs.has(q.subject || q.topic || "Geral"));
}

function renderSubjectDetail() {
  document.querySelectorAll(".tab-btn").forEach(t => {
    t.classList.toggle("active", t.dataset.mode === state.currentMode);
  });

  const pool = currentSubjectPool(state.currentMode);
  const dc = diffCounts(pool);
  document.querySelector('.chip-count[data-count="all"]').textContent = pool.length ? `(${pool.length})` : "";
  ["baixo", "medio", "dificil"].forEach(d => {
    document.querySelector(`.chip-count[data-count="${d}"]`).textContent = dc[d] ? `(${dc[d]})` : "";
  });

  document.querySelectorAll("#difficultyChips .chip").forEach(c => {
    c.classList.toggle("active", c.dataset.diff === state.currentDifficulty);
  });

  const filtered = filterByDifficulty(pool, state.currentDifficulty);
  const summary = document.getElementById("poolSummary");
  const modeLabel = { objective: "objetivas", discursive: "discursivas", oral: "orais" }[state.currentMode];
  summary.textContent = filtered.length > 0
    ? `${filtered.length} questões ${modeLabel} disponíveis para este assunto nesse filtro.`
    : `Nenhuma questão ${modeLabel} disponível para este filtro ainda.`;

  document.getElementById("startBtn").disabled = filtered.length === 0;
}

function filterByDifficulty(pool, diff) {
  if (diff === "all") return pool;
  return pool.filter(q => (["baixo", "medio", "dificil"].includes(q.difficulty) ? q.difficulty : "medio") === diff);
}

document.querySelectorAll(".tab-btn").forEach(tab => {
  tab.addEventListener("click", () => {
    state.currentMode = tab.dataset.mode;
    state.currentDifficulty = "all";
    renderSubjectDetail();
  });
});

document.querySelectorAll("#difficultyChips .chip").forEach(chip => {
  chip.addEventListener("click", () => {
    state.currentDifficulty = chip.dataset.diff;
    renderSubjectDetail();
  });
});

document.getElementById("startBtn").addEventListener("click", startSession);

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

function startSession() {
  const pool = filterByDifficulty(currentSubjectPool(state.currentMode), state.currentDifficulty);
  if (pool.length === 0) return;
  const questions = pool.slice();
  shuffle(questions);
  state.questions = questions; // usa o máximo de questões disponíveis
  state.index = 0;
  state.answers = [];

  crumbsPath([
    state.currentSemester.label, state.currentDiscipline.title, subjectsLabel(),
    { objective: "Objetiva", discursive: "Discursiva", oral: "Oral" }[state.currentMode],
  ]);

  if (state.currentMode === "objective") renderObjective();
  else if (state.currentMode === "discursive") renderDiscursive();
  else renderOral();
}

// ---------- Modo Objetivo ----------

let objSelectedKey = null;
let objConfirmed = false;

function renderObjective() {
  showScreen("screen-objective");
  const q = state.questions[state.index];
  objSelectedKey = null;
  objConfirmed = false;

  document.getElementById("objProgress").style.width = ((state.index) / state.questions.length * 100) + "%";
  document.getElementById("objCounter").textContent = `Questão ${state.index + 1} de ${state.questions.length}`;
  document.getElementById("objTopic").textContent = (q.topic || "") + (q.difficulty ? "  ·  " + (DIFF_LABEL[q.difficulty] || q.difficulty) : "");
  document.getElementById("objQuestion").textContent = q.question;

  const optsEl = document.getElementById("objOptions");
  optsEl.innerHTML = "";
  Object.entries(q.options).forEach(([key, text]) => {
    const item = document.createElement("div");
    item.className = "option-item";
    item.innerHTML = `<span class="option-letter">${key.toUpperCase()})</span><span>${text}</span>`;
    item.addEventListener("click", () => {
      if (objConfirmed) return;
      document.querySelectorAll("#objOptions .option-item").forEach(o => o.classList.remove("selected"));
      item.classList.add("selected");
      objSelectedKey = key;
      document.getElementById("objConfirmBtn").disabled = false;
    });
    item.dataset.key = key;
    optsEl.appendChild(item);
  });

  document.getElementById("objFeedback").classList.add("hidden");
  document.getElementById("objConfirmBtn").classList.remove("hidden");
  document.getElementById("objConfirmBtn").disabled = true;
  document.getElementById("objNextBtn").classList.add("hidden");
}

document.getElementById("objConfirmBtn").addEventListener("click", () => {
  const q = state.questions[state.index];
  const correct = objSelectedKey === q.correct;
  objConfirmed = true;

  document.querySelectorAll("#objOptions .option-item").forEach(o => {
    if (o.dataset.key === q.correct) o.classList.add("correct");
    else if (o.dataset.key === objSelectedKey) o.classList.add("incorrect");
  });

  const fb = document.getElementById("objFeedback");
  fb.className = "feedback-box " + (correct ? "ok" : "bad");
  fb.innerHTML = `<div class="feedback-score ${correct ? "good" : "low"}">${correct ? "✔ Correto!" : "✘ Incorreto"}</div>
    ${q.explanation ? `<div>${q.explanation}</div>` : ""}
    ${!correct ? `<div style="margin-top:8px;color:var(--text-dim)">Resposta correta: <b>${q.correct.toUpperCase()}</b></div>` : ""}
    ${renderSourceLine(q.source)}`;
  fb.classList.remove("hidden");

  state.answers.push({ question: q.question, score: correct ? 10 : 0, correct });

  if (!correct) {
    recordError({
      q, mode: "objective",
      userAnswer: objSelectedKey ? (objSelectedKey.toUpperCase() + ") " + (q.options[objSelectedKey] || "")) : "(não respondida)",
      correctAnswer: q.correct.toUpperCase() + ") " + q.options[q.correct],
      score: 0,
    });
  }

  document.getElementById("objConfirmBtn").classList.add("hidden");
  document.getElementById("objNextBtn").classList.remove("hidden");
});

document.getElementById("objNextBtn").addEventListener("click", () => {
  state.index++;
  if (state.index >= state.questions.length) {
    document.getElementById("objProgress").style.width = "100%";
    finishSession();
  } else {
    renderObjective();
  }
});

// ---------- Modo Discursivo ----------

function renderDiscursive() {
  showScreen("screen-discursive");
  const q = state.questions[state.index];

  document.getElementById("discProgress").style.width = (state.index / state.questions.length * 100) + "%";
  document.getElementById("discCounter").textContent = `Questão ${state.index + 1} de ${state.questions.length}`;
  document.getElementById("discTopic").textContent = (q.topic || "") + (q.difficulty ? "  ·  " + (DIFF_LABEL[q.difficulty] || q.difficulty) : "");
  document.getElementById("discQuestion").textContent = q.question;
  document.getElementById("discAnswer").value = "";
  document.getElementById("discAnswer").disabled = false;
  document.getElementById("discFeedback").classList.add("hidden");
  document.getElementById("discSubmitBtn").classList.remove("hidden");
  document.getElementById("discNextBtn").classList.add("hidden");
}

document.getElementById("discSubmitBtn").addEventListener("click", async () => {
  const q = state.questions[state.index];
  const userText = document.getElementById("discAnswer").value.trim();
  if (!userText) { alert("Escreva uma resposta antes de enviar."); return; }

  const btn = document.getElementById("discSubmitBtn");
  const originalLabel = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Avaliando...";
  document.getElementById("discAnswer").disabled = true;

  const result = await gradeAnswer(q, userText);
  renderOpenFeedback("discFeedback", result, q);

  state.answers.push({ question: q.question, score: result.score, correct: result.score >= 6 });
  if (result.score < 6) {
    recordError({ q, mode: "discursive", userAnswer: userText, correctAnswer: q.modelAnswer, score: result.score });
  }

  btn.textContent = originalLabel;
  btn.disabled = false;
  btn.classList.add("hidden");
  document.getElementById("discNextBtn").classList.remove("hidden");
});

document.getElementById("discNextBtn").addEventListener("click", () => {
  state.index++;
  if (state.index >= state.questions.length) {
    document.getElementById("discProgress").style.width = "100%";
    finishSession();
  } else {
    renderDiscursive();
  }
});

function renderOpenFeedback(boxId, result, q) {
  const fb = document.getElementById(boxId);
  const cls = scoreClass(result.score);
  fb.className = "feedback-box " + (cls === "good" ? "ok" : cls === "low" ? "bad" : "");

  let bodyHtml;
  if (result.engine === "llm") {
    bodyHtml = `
      <div>${escapeHtml(result.feedback) || "Sem comentários adicionais."}</div>
      <div class="engine-tag">🤖 Avaliado por IA (${escapeHtml(result.model) || "modelo local"}, local)</div>
    `;
  } else {
    const items = (result.details || []).map(d =>
      `<li class="${d.matched ? "hit" : "miss"}">${d.text}</li>`
    ).join("");
    bodyHtml = `
      <div>Pontos avaliados na sua resposta:</div>
      <ul class="keypoint-list">${items}</ul>
      <div class="engine-tag">⚙️ Avaliado localmente por padrão de resposta (IA indisponível)</div>
    `;
  }

  fb.innerHTML = `
    <div class="feedback-score ${cls}">Nota: ${result.score.toFixed(1)} / 10</div>
    ${bodyHtml}
    <details class="model-answer"><summary style="cursor:pointer;color:var(--accent)">Ver resposta padrão</summary>${q.modelAnswer || ""}</details>
    ${renderSourceLine(q.source)}
  `;
  fb.classList.remove("hidden");
}

// ---------- Modo Oral ----------

let SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;

function renderOral() {
  showScreen("screen-oral");
  const q = state.questions[state.index];

  document.getElementById("oralProgress").style.width = (state.index / state.questions.length * 100) + "%";
  document.getElementById("oralCounter").textContent = `Questão ${state.index + 1} de ${state.questions.length}`;
  document.getElementById("oralTopic").textContent = (q.topic || "") + (q.difficulty ? "  ·  " + (DIFF_LABEL[q.difficulty] || q.difficulty) : "");
  document.getElementById("oralQuestion").textContent = q.question;
  document.getElementById("oralStatus").textContent = "";
  document.getElementById("oralTranscriptBox").classList.add("hidden");
  document.getElementById("oralTranscript").textContent = "";
  document.getElementById("oralFeedback").classList.add("hidden");
  document.getElementById("oralNextBtn").classList.add("hidden");
  document.getElementById("oralRecordBtn").classList.remove("hidden");
  document.getElementById("oralStopBtn").classList.add("hidden");
  state.finalTranscript = "";

  const fallback = document.getElementById("oralFallback");
  if (!SpeechRecognitionCtor) {
    fallback.classList.remove("hidden");
    document.getElementById("oralRecordBtn").classList.add("hidden");
    document.getElementById("oralAnswerText").value = "";
  } else {
    fallback.classList.add("hidden");
  }

  speakQuestion(q.question);
}

function speakQuestion(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "pt-BR";
  utter.rate = 0.98;
  window.speechSynthesis.speak(utter);
}

document.getElementById("oralListenBtn").addEventListener("click", () => {
  const q = state.questions[state.index];
  speakQuestion(q.question);
});

document.getElementById("oralRecordBtn").addEventListener("click", () => {
  if (!SpeechRecognitionCtor) return;
  window.speechSynthesis && window.speechSynthesis.cancel();

  state.recognition = new SpeechRecognitionCtor();
  state.recognition.lang = "pt-BR";
  state.recognition.continuous = true;
  state.recognition.interimResults = true;
  state.finalTranscript = "";

  state.recognition.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) state.finalTranscript += transcript + " ";
      else interim += transcript;
    }
    document.getElementById("oralTranscriptBox").classList.remove("hidden");
    document.getElementById("oralTranscript").textContent = (state.finalTranscript + interim).trim();
  };
  state.recognition.onerror = (event) => {
    document.getElementById("oralStatus").textContent = "Erro no reconhecimento de voz: " + event.error + ". Tente novamente ou use o modo texto.";
  };
  state.recognition.onend = () => {
    document.getElementById("oralRecordBtn").classList.remove("hidden");
    document.getElementById("oralStopBtn").classList.add("hidden");
  };

  state.recognition.start();
  document.getElementById("oralStatus").textContent = "🔴 Ouvindo... fale sua resposta e clique em 'Parar e avaliar' quando terminar.";
  document.getElementById("oralRecordBtn").classList.add("hidden");
  document.getElementById("oralStopBtn").classList.remove("hidden");
});

document.getElementById("oralStopBtn").addEventListener("click", () => {
  if (state.recognition) state.recognition.stop();
  finalizeOralAnswer(state.finalTranscript.trim());
});

document.getElementById("oralFallbackSubmit").addEventListener("click", () => {
  const text = document.getElementById("oralAnswerText").value.trim();
  if (!text) { alert("Digite uma resposta antes de enviar."); return; }
  finalizeOralAnswer(text);
});

async function finalizeOralAnswer(text) {
  const q = state.questions[state.index];
  if (!text) text = "";

  document.getElementById("oralRecordBtn").classList.add("hidden");
  document.getElementById("oralStopBtn").classList.add("hidden");
  document.getElementById("oralFallbackSubmit").disabled = true;
  document.getElementById("oralStatus").textContent = "Avaliando resposta...";

  const result = await gradeAnswer(q, text);
  renderOpenFeedback("oralFeedback", result, q);
  document.getElementById("oralStatus").textContent = "";
  document.getElementById("oralFallbackSubmit").disabled = false;

  state.answers.push({ question: q.question, score: result.score, correct: result.score >= 6, transcript: text });
  if (result.score < 6) {
    recordError({ q, mode: "oral", userAnswer: text, correctAnswer: q.modelAnswer, score: result.score });
  }

  document.getElementById("oralFallback").classList.add("hidden");
  document.getElementById("oralNextBtn").classList.remove("hidden");
}

document.getElementById("oralNextBtn").addEventListener("click", () => {
  state.index++;
  if (state.index >= state.questions.length) {
    document.getElementById("oralProgress").style.width = "100%";
    finishSession();
  } else {
    renderOral();
  }
});

// ---------- Resultado final ----------

function finishSession() {
  window.speechSynthesis && window.speechSynthesis.cancel();
  const total = state.answers.reduce((sum, a) => sum + a.score, 0);
  const avg = state.answers.length ? total / state.answers.length : 0;
  const roundedAvg = Math.round(avg * 10) / 10;

  document.getElementById("finalScoreValue").textContent = roundedAvg.toFixed(1);
  const circle = document.getElementById("finalScoreCircle");
  circle.style.borderColor = roundedAvg >= 7 ? "var(--good)" : roundedAvg >= 4 ? "var(--warn)" : "var(--bad)";

  const modeLabel = { objective: "Prova Objetiva", discursive: "Prova Discursiva", oral: "Prova Oral" }[state.currentMode];
  document.getElementById("finalScoreLabel").textContent = `${subjectsLabel()} — ${modeLabel} — ${state.answers.length} questões`;

  const list = document.getElementById("resultsList");
  list.innerHTML = "";
  state.answers.forEach((a, i) => {
    const cls = scoreClass(a.score);
    const div = document.createElement("div");
    div.className = "result-item " + cls;
    div.innerHTML = `<div class="rq">${i + 1}. ${a.question}</div><div class="rs">${a.score.toFixed(1)} / 10</div>`;
    list.appendChild(div);
  });

  refreshNotebookCount();
  showScreen("screen-results");
}

document.getElementById("retryBtn").addEventListener("click", () => {
  showScreen("screen-subject-detail");
  crumbsPath([state.currentSemester.label, state.currentDiscipline.title, subjectsLabel()]);
});

document.getElementById("homeBtn").addEventListener("click", () => {
  showScreen("screen-semesters");
  setCrumbs("");
  renderSemesters();
});

// ---------- Caderno de erros ----------

document.querySelectorAll("#notebookFilter .chip").forEach(chip => {
  chip.addEventListener("click", () => {
    document.querySelectorAll("#notebookFilter .chip").forEach(c => c.classList.remove("active"));
    chip.classList.add("active");
    loadNotebook(chip.dataset.filter);
  });
});

async function loadNotebook(filter) {
  const listEl = document.getElementById("notebookList");
  const subtitleEl = document.getElementById("notebookSubtitle");
  if (!state.currentUser) { listEl.innerHTML = ""; return; }
  subtitleEl.textContent = `Erros registrados de ${state.currentUser.name} durante as provas discursivas, orais e objetivas.`;
  listEl.innerHTML = "<p class='subtitle'>Carregando...</p>";

  let url = `/api/errors?user_id=${state.currentUser.id}`;
  if (filter === "open") url += "&resolved=0";
  else if (filter === "resolved") url += "&resolved=1";

  try {
    const res = await fetch(url);
    const data = await res.json();
    const errors = data.errors || [];
    listEl.innerHTML = "";
    if (!errors.length) {
      listEl.innerHTML = `<div class="notebook-empty">Nenhum erro por aqui${filter === "open" ? " — parabéns! 🎉" : "."}</div>`;
      return;
    }
    errors.forEach(err => listEl.appendChild(renderNotebookItem(err)));
  } catch (e) {
    listEl.innerHTML = "<p class='subtitle'>Não foi possível carregar o caderno de erros.</p>";
  }
}

function renderNotebookItem(err) {
  const div = document.createElement("div");
  div.className = "notebook-item" + (err.resolved ? " resolved" : "");
  const date = err.created_at ? err.created_at.replace("T", " ").slice(0, 16) : "";
  const modeLabel = { objective: "Objetiva", discursive: "Discursiva", oral: "Oral" }[err.mode] || err.mode;
  const scoreTxt = typeof err.score === "number" ? err.score.toFixed(1) + " / 10" : "—";

  div.innerHTML = `
    <div class="notebook-item-head">
      <span class="notebook-item-meta">${escapeHtml(err.discipline)} · ${escapeHtml(err.subject)} · ${modeLabel} · ${date}</span>
      <span class="notebook-item-score">${scoreTxt}</span>
    </div>
    <div class="notebook-item-question">${escapeHtml(err.question_text)}</div>
    <div class="notebook-item-answer">Sua resposta: ${escapeHtml(err.user_answer || "—")}</div>
    ${err.correct_answer ? `<div class="notebook-item-answer">Esperado: ${escapeHtml(err.correct_answer)}</div>` : ""}
    <div class="notebook-item-actions">
      <button class="btn-lesson">📖 Ver mini-aula</button>
      <button class="btn-toggle-resolved">${err.resolved ? "↺ Reabrir" : "✔ Marcar como revisado"}</button>
      <button class="btn-delete">🗑 Excluir</button>
    </div>
  `;

  div.querySelector(".btn-lesson").addEventListener("click", () => openLessonModal(err));
  div.querySelector(".btn-toggle-resolved").addEventListener("click", async () => {
    await fetch("/api/errors/resolve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: err.id, resolved: !err.resolved }),
    });
    const activeFilter = document.querySelector("#notebookFilter .chip.active").dataset.filter;
    loadNotebook(activeFilter);
    refreshNotebookCount();
  });
  div.querySelector(".btn-delete").addEventListener("click", async () => {
    if (!confirm("Excluir este registro do caderno de erros?")) return;
    await fetch("/api/errors/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: err.id }),
    });
    const activeFilter = document.querySelector("#notebookFilter .chip.active").dataset.filter;
    loadNotebook(activeFilter);
    refreshNotebookCount();
  });

  return div;
}

// ---------- Modal de mini-aula ----------

const lessonModal = document.getElementById("lessonModal");
document.getElementById("lessonModalClose").addEventListener("click", () => {
  lessonModal.classList.add("hidden");
});
lessonModal.addEventListener("click", (e) => {
  if (e.target === lessonModal) lessonModal.classList.add("hidden");
});

// Monta uma mini-aula simples a partir do próprio material, para os poucos
// casos em que a mini-aula pré-produzida ainda não existe para a questão
// (ex.: banco de questões atualizado antes de rodar o gerador). Nunca chama IA.
function composeFallbackLesson(err) {
  const parts = [];
  if (err.model_answer) parts.push(err.model_answer.trim());
  const keyPoints = err.keyPoints || [];
  if (keyPoints.length) {
    const pts = keyPoints.map(kp => kp.text).filter(Boolean).join("; ");
    if (pts) parts.push("Pontos essenciais: " + pts + ".");
  }
  if (err.source && err.source.document) {
    let ref = "Para aprofundar, ";
    if (err.source.citation) ref += "autor/obra de referência: " + err.source.citation + " — ";
    ref += "leia mais em " + err.source.document + (err.source.page ? ", p. " + err.source.page : "") + ".";
    parts.push(ref);
  }
  if (!parts.length) parts.push(`Revise o conteúdo sobre "${err.subject || "este tema"}" no material da disciplina.`);
  return parts.join(" ");
}

function openLessonModal(err) {
  document.getElementById("lessonModalTitle").textContent = "Mini-aula — " + err.subject;
  document.getElementById("lessonLoading").classList.add("hidden");
  lessonModal.classList.remove("hidden");

  if (err.mini_lesson) {
    document.getElementById("lessonContent").textContent = err.mini_lesson;
    document.getElementById("lessonEngineTag").textContent = "📖 Mini-aula pré-produzida";
  } else {
    document.getElementById("lessonContent").textContent = composeFallbackLesson(err);
    document.getElementById("lessonEngineTag").textContent = "⚙️ Baseado no material da disciplina (mini-aula ainda não pré-produzida para esta questão)";
  }
}

// ---------- Inicialização ----------

async function init() {
  const saved = loadUserLocal();
  if (saved && saved.name) {
    // Revalida contra o servidor em vez de confiar cegamente no id salvo:
    // se o banco de dados foi recriado/limpo, isso recria o usuário e evita
    // que os erros fiquem sendo gravados com um userId que não existe mais.
    const ok = await doLoginSilently(saved.name);
    if (ok) {
      await renderSemesters();
      showScreen("screen-semesters");
      return;
    }
  }
  clearUserLocal();
  showScreen("screen-login");
  loadUsersIntoLogin();
}

init();
checkAI();
