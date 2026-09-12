/* Professor Treinador — lógica principal (vanilla JS, sem dependências) */

const state = {
  currentUser: null,       // {id, name}
  manifest: null,
  banks: {},                // disciplineId -> parsed JSON
  currentCourse: null,      // manifest course object (trilha: Psicologia, Concurso PCPR, ...)
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
  answeredMap: {},          // "mode:questionId" -> true/false (acertou?), carregado do servidor por usuário
  filterRemove: { answered: false, wrong: false, correct: false }, // filtro "Remover" na tela do assunto
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
  const writtenAnswersBtn = document.getElementById("writtenAnswersBtn");
  if (state.currentUser) {
    chip.textContent = "👤 " + state.currentUser.name + " (trocar)";
    chip.classList.remove("hidden");
    notebookBtn.classList.remove("hidden");
    writtenAnswersBtn.classList.remove("hidden");
    refreshNotebookCount();
  } else {
    chip.classList.add("hidden");
    notebookBtn.classList.add("hidden");
    writtenAnswersBtn.classList.add("hidden");
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
    loadAnsweredMap();
    return true;
  } catch (e) {
    return false;
  }
}

// ---------- Mapa de respostas já dadas (para o filtro "Remover" na tela do assunto) ----------

async function loadAnsweredMap() {
  if (!state.currentUser) { state.answeredMap = {}; return; }
  try {
    const res = await fetch(`/api/answers?user_id=${state.currentUser.id}`);
    if (!res.ok) return;
    const data = await res.json();
    const map = {};
    (data.answers || []).forEach(a => { map[a.mode + ":" + a.question_id] = !!a.correct; });
    state.answeredMap = map;
  } catch (e) {
    console.warn("Não foi possível carregar o histórico de respostas:", e);
  }
}

async function recordAnswer({ q, mode, correct, userAnswer, score }) {
  if (!state.currentUser) return;
  state.answeredMap[mode + ":" + q.id] = correct; // atualização otimista, já reflete no filtro na hora
  try {
    const res = await fetch("/api/answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: state.currentUser.id,
        questionId: q.id,
        mode,
        subject: q.subject || q.topic || "",
        correct,
        semester: state.currentSemester ? state.currentSemester.label : "",
        discipline: state.currentDiscipline ? state.currentDiscipline.title : "",
        question: q.question,
        userAnswer: userAnswer || "",
        modelAnswer: q.modelAnswer || q.explanation || "",
        keyPoints: q.keyPoints || [],
        source: q.source || null,
        miniLesson: q.miniLesson || "",
        score: typeof score === "number" ? score : null,
      }),
    });
    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      if (res.status === 502 && /usuário|user|foreign key|constraint/i.test(errBody.error || "")) {
        const revalidated = await doLoginSilently(state.currentUser.name);
        if (revalidated) { await recordAnswer({ q, mode, correct, userAnswer, score }); return; }
      }
      console.error("Falha ao registrar resposta:", res.status, errBody.error || "");
    }
  } catch (e) {
    console.warn("Não foi possível registrar a resposta (rede/servidor indisponível):", e);
  }
}

async function doLogin(name) {
  const ok = await doLoginSilently(name);
  if (ok) {
    showScreen("screen-courses");
    renderCourses();
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

document.getElementById("writtenAnswersBtn").addEventListener("click", () => {
  showScreen("screen-written-answers");
  setCrumbs("Respostas escritas");
  loadWrittenAnswers("all");
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
    if (btn.dataset.back === "screen-courses") { setCrumbs(""); }
    else if (btn.dataset.back === "screen-semesters") { crumbsPath([state.currentCourse && state.currentCourse.label]); }
    else if (btn.dataset.back === "screen-disciplines") { crumbsPath([state.currentCourse && state.currentCourse.label, state.currentSemester && state.currentSemester.label]); }
    else if (btn.dataset.back === "screen-subjects") { crumbsPath([state.currentCourse && state.currentCourse.label, state.currentSemester && state.currentSemester.label, state.currentDiscipline && state.currentDiscipline.title]); }
    else if (btn.dataset.back === "screen-subject-detail") { crumbsPath([state.currentCourse && state.currentCourse.label, state.currentSemester && state.currentSemester.label, state.currentDiscipline && state.currentDiscipline.title, subjectsLabel()]); }
  });
});

document.getElementById("brandHome").addEventListener("click", () => {
  window.speechSynthesis && window.speechSynthesis.cancel();
  if (!state.currentUser) { showScreen("screen-login"); return; }
  showScreen("screen-courses");
  setCrumbs("");
  renderCourses();
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

// ---------- Tela: cursos/trilhas ----------

async function renderCourses() {
  await loadManifest();
  const grid = document.getElementById("courseGrid");
  grid.innerHTML = "";
  state.manifest.courses.forEach(course => {
    const totalDisciplines = course.semesters.reduce((sum, s) => sum + (s.disciplines || []).length, 0);
    const card = document.createElement("button");
    card.className = "semester-card";
    card.innerHTML = `
      <span class="semester-title">${course.icon ? course.icon + " " : ""}${escapeHtml(course.label)}</span>
      <span class="semester-desc">${escapeHtml(course.subtitle || "")}</span>
    `;
    card.addEventListener("click", () => selectCourse(course));
    grid.appendChild(card);
  });
}

function selectCourse(course) {
  state.currentCourse = course;
  document.getElementById("semestersSubtitle").textContent = course.subtitle || "";
  crumbsPath([course.label]);
  renderSemesters(course);
  showScreen("screen-semesters");
}

// ---------- Tela: semestres ----------

function renderSemesters(course) {
  const grid = document.getElementById("semesterGrid");
  grid.innerHTML = "";
  course.semesters.forEach(sem => {
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
  crumbsPath([state.currentCourse.label, sem.label]);
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
  crumbsPath([state.currentCourse.label, state.currentSemester.label, disc.title]);
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

function subjectSourceDocuments(questions) {
  const docs = new Set();
  questions.forEach(q => {
    if (q.source && q.source.document) docs.add(q.source.document);
  });
  return [...docs];
}

function diffCounts(questions) {
  const counts = { baixo: 0, medio: 0, dificil: 0 };
  questions.forEach(q => {
    const d = ["baixo", "medio", "dificil"].includes(q.difficulty) ? q.difficulty : "medio";
    counts[d]++;
  });
  return counts;
}

// Agrupa os assuntos (subject) de um banco por documento-fonte (PDF), formando
// uma árvore: tronco = PDF, galhos = assuntos/tópicos daquele PDF. Um assunto
// cujas questões apontem para mais de um PDF é agrupado sob o primeiro
// documento encontrado (caso raro). Quando as questões de um assunto trazem
// um campo opcional `section`, ele vira um ou mais níveis de pasta entre o
// tronco e o assunto: uma string cria 1 nível (comportamento legado); um
// array de strings cria um nível de pasta por item do array, permitindo
// aninhamento em quantos níveis o PDF realmente tiver (ex.: ["2. Título da
// seção", "2.3 Subseção"]). Documentos/assuntos sem `section` mantêm o
// comportamento antigo (tronco -> assuntos direto).
function sectionPath(q) {
  if (!q.section) return [];
  return Array.isArray(q.section) ? q.section : [q.section];
}

function collectSubjectsTree(bank) {
  const subjectsMap = collectSubjects(bank);
  const docs = {};
  Object.keys(subjectsMap).forEach(subject => {
    const buckets = subjectsMap[subject];
    const all = [...buckets.objective, ...buckets.discursive, ...buckets.oral];
    const doc = subjectSourceDocuments(all)[0] || "Outros materiais";
    const withSection = all.find(q => q.section);
    const path = withSection ? sectionPath(withSection) : [];

    if (!docs[doc]) docs[doc] = { children: new Map(), subjects: new Map() };
    let node = docs[doc];
    path.forEach(seg => {
      if (!node.children.has(seg)) node.children.set(seg, { children: new Map(), subjects: new Map() });
      node = node.children.get(seg);
    });
    node.subjects.set(subject, buckets);
  });
  return docs;
}

// Quando as questões de um assunto trazem um campo opcional `order` (posição
// do título/subtítulo dentro do PDF), usamos essa ordem para exibir os
// assuntos/pastas na mesma sequência em que aparecem no material, em vez de
// alfabética. Sem essa informação, a ordenação cai para o nome.
function subjectOrderValue(buckets) {
  const all = [...buckets.objective, ...buckets.discursive, ...buckets.oral];
  let min = null;
  all.forEach(q => {
    if (typeof q.order === "number" && (min === null || q.order < min)) min = q.order;
  });
  return min;
}

function groupOrderValue(node) {
  let min = null;
  node.children.forEach(child => {
    const v = groupOrderValue(child);
    if (v !== null && (min === null || v < min)) min = v;
  });
  node.subjects.forEach(buckets => {
    const v = subjectOrderValue(buckets);
    if (v !== null && (min === null || v < min)) min = v;
  });
  return min;
}

function groupAllSubjectNames(node) {
  const names = [];
  node.children.forEach(child => names.push(...groupAllSubjectNames(child)));
  node.subjects.forEach((buckets, label) => names.push(label));
  return names;
}

function groupTotalQuestions(node) {
  let total = 0;
  node.children.forEach(child => { total += groupTotalQuestions(child); });
  node.subjects.forEach(buckets => { total += buckets.objective.length + buckets.discursive.length + buckets.oral.length; });
  return total;
}

// Combina subpastas e assuntos-folha de um nó em uma única lista ordenada
// (por `order`, com fallback alfabético), preservando a sequência real do
// material mesmo quando pastas e assuntos se intercalam num mesmo nível.
function sortedNodeEntries(node) {
  const entries = [];
  node.children.forEach((child, label) => entries.push({ kind: "group", label, node: child }));
  node.subjects.forEach((buckets, label) => entries.push({ kind: "leaf", label, buckets }));
  entries.sort((a, b) => {
    const oa = a.kind === "leaf" ? subjectOrderValue(a.buckets) : groupOrderValue(a.node);
    const ob = b.kind === "leaf" ? subjectOrderValue(b.buckets) : groupOrderValue(b.node);
    if (oa !== null && ob !== null) return oa - ob;
    if (oa !== null) return -1;
    if (ob !== null) return 1;
    return a.label.localeCompare(b.label, "pt-BR", { numeric: true });
  });
  return entries;
}

function renderTreeBranch(subject, buckets, parentEl) {
  const all = [...buckets.objective, ...buckets.discursive, ...buckets.oral];
  const dc = diffCounts(all);
  const badges = ["baixo", "medio", "dificil"]
    .filter(d => dc[d] > 0)
    .map(d => `<span class="diff-badge ${d}">${DIFF_LABEL[d]} ${dc[d]}</span>`)
    .join("");

  const branch = document.createElement("button");
  branch.className = "tree-branch" + (state.selectedSubjects.has(subject) ? " selected" : "");
  branch.dataset.subject = subject;
  branch.innerHTML = `
    <span class="tree-checkbox branch-checkbox"></span>
    <span class="tree-branch-body">
      <span class="tree-branch-title">${escapeHtml(subject)}</span>
      <span class="tree-branch-meta">${all.length} questões · ${buckets.objective.length} obj · ${buckets.discursive.length} disc · ${buckets.oral.length} oral</span>
      <div class="diff-badges">${badges}</div>
    </span>
  `;
  branch.addEventListener("click", () => toggleSubject(subject, branch));
  parentEl.appendChild(branch);
}

// Renderiza recursivamente as subpastas e os assuntos-folha de um nó dentro
// de `parentEl`. Cada nível de pasta reaproveita o mesmo template (📁),
// aninhando quantas vezes o `section` de origem exigir.
function renderTreeGroupEntries(node, parentEl) {
  sortedNodeEntries(node).forEach(entry => {
    if (entry.kind === "leaf") {
      renderTreeBranch(entry.label, entry.buckets, parentEl);
      return;
    }
    const subjectNames = groupAllSubjectNames(entry.node);
    const total = groupTotalQuestions(entry.node);

    const groupEl = document.createElement("div");
    groupEl.className = "tree-section";
    groupEl.innerHTML = `
      <div class="tree-section-header">
        <span class="tree-checkbox trunk-checkbox"></span>
        <span class="tree-section-title">📁 ${escapeHtml(entry.label)}</span>
        <span class="tree-section-meta">${subjectNames.length} assunto${subjectNames.length > 1 ? "s" : ""} · ${total} questões</span>
      </div>
      <div class="tree-branches"></div>
    `;
    const childBranchesEl = groupEl.querySelector(".tree-branches");
    renderTreeGroupEntries(entry.node, childBranchesEl);
    groupEl.querySelector(".tree-section-header").addEventListener("click", () => toggleTrunk(subjectNames, groupEl));
    parentEl.appendChild(groupEl);
    updateTrunkCheckboxState(groupEl, subjectNames);
  });
}

function renderSubjects() {
  const bank = state.banks[state.currentDiscipline.id];
  const tree = collectSubjectsTree(bank);
  const container = document.getElementById("subjectGrid");
  container.innerHTML = "";
  container.classList.add("subject-tree");

  Object.keys(tree).sort((a, b) => a.localeCompare(b, "pt-BR")).forEach(doc => {
    const docNode = tree[doc];
    const allSubjectNames = groupAllSubjectNames(docNode);
    const trunkTotal = groupTotalQuestions(docNode);

    const trunk = document.createElement("div");
    trunk.className = "tree-trunk";
    trunk.innerHTML = `
      <div class="tree-trunk-header">
        <span class="tree-checkbox trunk-checkbox"></span>
        <span class="tree-trunk-title">📄 ${escapeHtml(doc)}</span>
        <span class="tree-trunk-meta">${allSubjectNames.length} assunto${allSubjectNames.length > 1 ? "s" : ""} · ${trunkTotal} questões</span>
      </div>
      <div class="tree-branches"></div>
    `;
    const branchesRoot = trunk.querySelector(".tree-branches");
    renderTreeGroupEntries(docNode, branchesRoot);

    trunk.querySelector(".tree-trunk-header").addEventListener("click", () => toggleTrunk(allSubjectNames, trunk));
    container.appendChild(trunk);
    updateTrunkCheckboxState(trunk, allSubjectNames);
  });

  updateSubjectsActionBar();
}

// Sobe pela árvore do DOM a partir de `el`, atualizando o checkbox de cada
// pasta/tronco ancestral (podem ser vários níveis, ao contrário do antigo
// esquema fixo de 2 níveis).
function updateAncestorCheckboxes(el) {
  let ancestor = el.closest(".tree-section, .tree-trunk");
  while (ancestor) {
    const namesInAncestor = [...ancestor.querySelectorAll(".tree-branch")].map(b => b.dataset.subject);
    updateTrunkCheckboxState(ancestor, namesInAncestor);
    if (ancestor.classList.contains("tree-trunk")) break;
    const parent = ancestor.parentElement;
    ancestor = parent ? parent.closest(".tree-section, .tree-trunk") : null;
  }
}

function toggleSubject(subject, branchEl) {
  if (state.selectedSubjects.has(subject)) {
    state.selectedSubjects.delete(subject);
    branchEl.classList.remove("selected");
  } else {
    state.selectedSubjects.add(subject);
    branchEl.classList.add("selected");
  }
  updateAncestorCheckboxes(branchEl);
  updateSubjectsActionBar();
}

function toggleTrunk(subjectNames, groupEl) {
  const allSelected = subjectNames.every(s => state.selectedSubjects.has(s));
  subjectNames.forEach(s => {
    if (allSelected) state.selectedSubjects.delete(s);
    else state.selectedSubjects.add(s);
  });
  groupEl.querySelectorAll(".tree-branch").forEach(b => {
    b.classList.toggle("selected", state.selectedSubjects.has(b.dataset.subject));
  });
  updateTrunkCheckboxState(groupEl, subjectNames);
  if (!groupEl.classList.contains("tree-trunk") && groupEl.parentElement) {
    updateAncestorCheckboxes(groupEl.parentElement);
  }
  updateSubjectsActionBar();
}

function updateTrunkCheckboxState(groupEl, subjectNames) {
  const cb = groupEl.querySelector(".trunk-checkbox");
  const selectedCount = subjectNames.filter(s => state.selectedSubjects.has(s)).length;
  cb.classList.remove("checked", "indeterminate");
  if (selectedCount > 0 && selectedCount === subjectNames.length) cb.classList.add("checked");
  else if (selectedCount > 0) cb.classList.add("indeterminate");
}

function updateSubjectsActionBar() {
  const n = state.selectedSubjects.size;
  document.getElementById("subjectsSelectedCount").textContent =
    n === 0 ? "Nenhum assunto selecionado" : n === 1 ? "1 assunto selecionado" : `${n} assuntos selecionados`;
  document.getElementById("subjectsContinueBtn").disabled = n === 0;
}

document.getElementById("subjectsSelectAll").addEventListener("click", () => {
  document.querySelectorAll("#subjectGrid .tree-branch").forEach(branch => {
    state.selectedSubjects.add(branch.dataset.subject);
    branch.classList.add("selected");
  });
  document.querySelectorAll("#subjectGrid .tree-section").forEach(sectionEl => {
    const subjectNames = [...sectionEl.querySelectorAll(".tree-branch")].map(b => b.dataset.subject);
    updateTrunkCheckboxState(sectionEl, subjectNames);
  });
  document.querySelectorAll("#subjectGrid .tree-trunk").forEach(trunkEl => {
    const subjectNames = [...trunkEl.querySelectorAll(".tree-branch")].map(b => b.dataset.subject);
    updateTrunkCheckboxState(trunkEl, subjectNames);
  });
  updateSubjectsActionBar();
});

document.getElementById("subjectsClearAll").addEventListener("click", () => {
  state.selectedSubjects.clear();
  document.querySelectorAll("#subjectGrid .tree-branch").forEach(branch => branch.classList.remove("selected"));
  document.querySelectorAll("#subjectGrid .tree-section").forEach(sectionEl => {
    const subjectNames = [...sectionEl.querySelectorAll(".tree-branch")].map(b => b.dataset.subject);
    updateTrunkCheckboxState(sectionEl, subjectNames);
  });
  document.querySelectorAll("#subjectGrid .tree-trunk").forEach(trunkEl => {
    const subjectNames = [...trunkEl.querySelectorAll(".tree-branch")].map(b => b.dataset.subject);
    updateTrunkCheckboxState(trunkEl, subjectNames);
  });
  updateSubjectsActionBar();
});

document.getElementById("subjectsContinueBtn").addEventListener("click", () => {
  if (state.selectedSubjects.size === 0) return;
  state.currentSubjects = [...state.selectedSubjects];
  state.currentMode = "objective";
  state.currentDifficulty = "all";
  state.filterRemove = { answered: false, wrong: false, correct: false };
  document.querySelectorAll("#answerFilterChips .chip").forEach(c => c.classList.remove("active"));
  document.getElementById("subjectTitle").textContent = subjectsLabel();
  document.getElementById("subjectDisciplineLabel").textContent = state.currentDiscipline.title;
  crumbsPath([state.currentCourse.label, state.currentSemester.label, state.currentDiscipline.title, subjectsLabel()]);
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

function applyAnswerFilters(pool, mode) {
  const { answered, wrong, correct } = state.filterRemove;
  if (!answered && !wrong && !correct) return pool;
  return pool.filter(q => {
    const key = mode + ":" + q.id;
    if (!(key in state.answeredMap)) return true; // nunca respondida -> mantém
    const wasCorrect = state.answeredMap[key];
    if (answered) return false;
    if (wrong && !wasCorrect) return false;
    if (correct && wasCorrect) return false;
    return true;
  });
}

function renderSubjectDetail() {
  document.querySelectorAll(".tab-btn").forEach(t => {
    t.classList.toggle("active", t.dataset.mode === state.currentMode);
  });

  const pool = applyAnswerFilters(currentSubjectPool(state.currentMode), state.currentMode);
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
  document.getElementById("printExamBtn").disabled = filtered.length === 0;
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

document.querySelectorAll("#answerFilterChips .chip").forEach(chip => {
  chip.addEventListener("click", () => {
    chip.classList.toggle("active");
    state.filterRemove[chip.dataset.filter] = chip.classList.contains("active");
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
  const pool = filterByDifficulty(applyAnswerFilters(currentSubjectPool(state.currentMode), state.currentMode), state.currentDifficulty);
  if (pool.length === 0) return;
  const questions = pool.slice();
  shuffle(questions);
  state.questions = questions; // usa o máximo de questões disponíveis
  state.index = 0;
  state.answers = [];
  // Rascunho digitado e resultado já avaliado por questão (índice), para
  // permitir pular uma discursiva e voltar a ela depois sem perder o que já
  // foi escrito ou refazer uma correção que já tinha sido feita.
  state.discDrafts = new Array(questions.length).fill("");
  state.discResults = new Array(questions.length).fill(null);

  crumbsPath([
    state.currentCourse.label, state.currentSemester.label, state.currentDiscipline.title, subjectsLabel(),
    { objective: "Objetiva", discursive: "Discursiva", oral: "Oral" }[state.currentMode],
  ]);

  if (state.currentMode === "objective") renderObjective();
  else if (state.currentMode === "discursive") renderDiscursive();
  else renderOral();
}

// ---------- Impressão: caderno de questões (prova) ----------

document.getElementById("printExamBtn").addEventListener("click", () => {
  const pool = filterByDifficulty(applyAnswerFilters(currentSubjectPool(state.currentMode), state.currentMode), state.currentDifficulty);
  if (pool.length === 0) return;
  const questions = pool.slice();
  shuffle(questions);
  openPrintableExam(questions, state.currentMode);
});

function openPrintableExam(questions, mode) {
  const modeLabel = { objective: "Prova Objetiva", discursive: "Prova Discursiva", oral: "Prova Oral" }[mode];
  const title = `${state.currentDiscipline.title} — ${subjectsLabel()}`;
  const letters = ["a", "b", "c", "d", "e"];

  let questionsHtml = "";
  let gabaritoHtml = "";

  questions.forEach((q, idx) => {
    const n = idx + 1;
    questionsHtml += `<div class="pq">
      <p class="pq-head"><strong>${n}.</strong> <span class="pq-topic">${escapeHtml(q.topic || q.subject || "")}</span></p>
      <p class="pq-text">${escapeHtml(q.question)}</p>`;

    if (mode === "objective") {
      questionsHtml += `<ul class="pq-options">` +
        letters.filter(l => q.options && q.options[l]).map(l => `<li>(${l.toUpperCase()}) ${escapeHtml(q.options[l])}</li>`).join("") +
        `</ul>`;
      gabaritoHtml += `<div class="pg-item"><strong>${n}.</strong> ${(q.correct || "").toUpperCase()}</div>`;
    } else {
      questionsHtml += `<div class="pq-lines"></div>`;
      gabaritoHtml += `<div class="pg-block"><strong>${n}. ${escapeHtml(q.question)}</strong><p>${escapeHtml(q.modelAnswer || q.explanation || "")}</p></div>`;
    }
    questionsHtml += `</div>`;
  });

  const html = `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>${escapeHtml(title)} — ${modeLabel}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: Georgia, "Times New Roman", serif; color: #111; max-width: 800px; margin: 24px auto; padding: 0 16px; line-height: 1.5; }
  h1 { font-size: 20px; margin-bottom: 4px; }
  .print-meta { color: #444; font-size: 14px; margin: 0 0 12px; }
  .print-fields { display: flex; justify-content: space-between; gap: 24px; border-top: 1px solid #999; border-bottom: 1px solid #999; padding: 10px 0; margin-bottom: 24px; font-size: 14px; }
  .pq { margin-bottom: 22px; page-break-inside: avoid; }
  .pq-head { margin: 0 0 2px; }
  .pq-topic { color: #666; font-size: 12px; font-style: italic; }
  .pq-text { margin: 4px 0 8px; font-weight: 600; }
  .pq-options { list-style: none; padding: 0; margin: 0; }
  .pq-options li { margin: 4px 0 4px 12px; }
  .pq-lines { border-bottom: 1px solid #bbb; height: 28px; margin: 6px 0; }
  .pq-lines + .pq-lines { margin-top: -2px; }
  .print-gabarito { page-break-before: always; margin-top: 24px; }
  .print-gabarito h2 { font-size: 18px; border-bottom: 2px solid #111; padding-bottom: 6px; }
  .pg-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px 4px; font-size: 14px; }
  .pg-block { margin-bottom: 14px; font-size: 14px; }
  .pg-block p { margin: 4px 0 0; color: #333; }
  .print-actions { margin: 16px 0; }
  @media print { .print-actions { display: none; } }
</style>
</head>
<body>
  <div class="print-actions"><button onclick="window.print()">🖨️ Imprimir / Salvar PDF</button></div>
  <header>
    <h1>${escapeHtml(title)}</h1>
    <p class="print-meta">${modeLabel} · ${questions.length} questões · gerado pelo Professor Treinador</p>
    <div class="print-fields">
      <span>Nome: _______________________________________</span>
      <span>Data: ____ / ____ / ________</span>
    </div>
  </header>
  <main>${questionsHtml}</main>
  <section class="print-gabarito">
    <h2>Gabarito</h2>
    ${mode === "objective" ? `<div class="pg-grid">${gabaritoHtml}</div>` : gabaritoHtml}
  </section>
</body>
</html>`;

  const win = window.open("", "_blank");
  if (!win) {
    alert("Não foi possível abrir a janela de impressão. Permita pop-ups para este site e tente novamente.");
    return;
  }
  win.document.open();
  win.document.write(html);
  win.document.close();
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
  const objUserAnswer = objSelectedKey ? `${objSelectedKey.toUpperCase()}) ${q.options[objSelectedKey]}` : "";
  recordAnswer({ q, mode: "objective", correct, userAnswer: objUserAnswer, score: correct ? 10 : 0 });

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
  const cached = state.discResults[state.index];

  document.getElementById("discProgress").style.width = (state.index / state.questions.length * 100) + "%";
  document.getElementById("discCounter").textContent = `Questão ${state.index + 1} de ${state.questions.length}`;
  document.getElementById("discTopic").textContent = (q.topic || "") + (q.difficulty ? "  ·  " + (DIFF_LABEL[q.difficulty] || q.difficulty) : "");
  document.getElementById("discQuestion").textContent = q.question;

  const answerEl = document.getElementById("discAnswer");
  const prevBtn = document.getElementById("discPrevBtn");
  const submitBtn = document.getElementById("discSubmitBtn");
  const skipBtn = document.getElementById("discSkipBtn");
  const nextBtn = document.getElementById("discNextBtn");

  prevBtn.disabled = state.index === 0;

  if (cached) {
    // Questão já respondida nesta sessão: mostra o que foi enviado e a
    // correção já obtida, sem permitir reenviar; só navegação.
    answerEl.value = state.discDrafts[state.index] || "";
    answerEl.disabled = true;
    renderOpenFeedback("discFeedback", cached, q);
    document.getElementById("discFeedback").classList.remove("hidden");
    submitBtn.classList.add("hidden");
    skipBtn.classList.add("hidden");
    nextBtn.classList.remove("hidden");
  } else {
    answerEl.value = state.discDrafts[state.index] || "";
    answerEl.disabled = false;
    document.getElementById("discFeedback").classList.add("hidden");
    submitBtn.classList.remove("hidden");
    submitBtn.disabled = false;
    submitBtn.textContent = "Enviar resposta";
    skipBtn.classList.remove("hidden");
    nextBtn.classList.add("hidden");
  }
}

// Salva o rascunho da questão atual (se ainda não enviada) e navega para
// `newIndex`. Ao ultrapassar o fim da lista, volta para a primeira questão
// ainda pendente (pulada) em vez de encerrar direto, e só finaliza a sessão
// quando não sobrar nenhuma.
function discGoTo(newIndex) {
  if (!state.discResults[state.index]) {
    state.discDrafts[state.index] = document.getElementById("discAnswer").value;
  }
  if (newIndex >= state.questions.length) {
    const pendingIdx = state.discResults.findIndex(r => !r);
    if (pendingIdx !== -1) {
      state.index = pendingIdx;
      renderDiscursive();
      return;
    }
    document.getElementById("discProgress").style.width = "100%";
    finishSession();
    return;
  }
  state.index = Math.max(0, newIndex);
  renderDiscursive();
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

  state.discResults[state.index] = result;
  state.discDrafts[state.index] = userText;
  state.answers.push({ question: q.question, score: result.score, correct: result.score >= 6 });
  recordAnswer({ q, mode: "discursive", correct: result.score >= 6, userAnswer: userText, score: result.score });
  if (result.score < 6) {
    recordError({ q, mode: "discursive", userAnswer: userText, correctAnswer: q.modelAnswer, score: result.score });
  }

  btn.textContent = originalLabel;
  btn.disabled = false;
  btn.classList.add("hidden");
  document.getElementById("discSkipBtn").classList.add("hidden");
  document.getElementById("discNextBtn").classList.remove("hidden");
});

document.getElementById("discPrevBtn").addEventListener("click", () => discGoTo(state.index - 1));
document.getElementById("discSkipBtn").addEventListener("click", () => discGoTo(state.index + 1));
document.getElementById("discNextBtn").addEventListener("click", () => discGoTo(state.index + 1));

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
  recordAnswer({ q, mode: "oral", correct: result.score >= 6, userAnswer: text, score: result.score });
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
  crumbsPath([state.currentCourse.label, state.currentSemester.label, state.currentDiscipline.title, subjectsLabel()]);
});

document.getElementById("homeBtn").addEventListener("click", () => {
  showScreen("screen-courses");
  setCrumbs("");
  renderCourses();
});

// ---------- Agrupamento hierárquico (matéria > assunto > subassunto) ----------
// Reaproveitado pelo Caderno de erros e por Respostas escritas: os dois
// guardam apenas `discipline` (título) e `subject` (o assunto-folha) junto de
// cada registro; para agrupar por assunto/subassunto, procuramos, no próprio
// banco de questões já carregado (ou carregado sob demanda aqui), uma questão
// atual com aquele `subject` e usamos seu campo opcional `section` (string ou
// array) como o caminho de pastas entre a matéria e o assunto-folha.

function findDisciplineByTitle(title) {
  if (!state.manifest || !title) return null;
  for (const course of state.manifest.courses) {
    for (const sem of course.semesters) {
      for (const d of (sem.disciplines || [])) {
        if (d.title === title) return d;
      }
    }
  }
  return null;
}

async function resolveSectionPath(disciplineTitle, subject) {
  const discipline = findDisciplineByTitle(disciplineTitle);
  if (!discipline || !subject) return [];
  let bank;
  try {
    bank = await loadBank(discipline);
  } catch (e) {
    return [];
  }
  const all = [...(bank.objective || []), ...(bank.discursive || []), ...(bank.oral || [])];
  const q = all.find(x => x.subject === subject);
  if (!q || !q.section) return [];
  return Array.isArray(q.section) ? q.section : [q.section];
}

// Agrupa `records` (cada um com .discipline e .subject) em uma árvore
// { [disciplina]: { children: { [pastaSeção]: {...} }, items: { [assunto]: [registros] } } }.
async function groupRecordsHierarchically(records) {
  const pathCache = new Map();
  const uniqueKeys = [...new Set(records.map(r => (r.discipline || "") + " " + (r.subject || "")))];
  await Promise.all(uniqueKeys.map(async key => {
    const [discipline, subject] = key.split(" ");
    pathCache.set(key, await resolveSectionPath(discipline, subject));
  }));

  const root = {};
  records.forEach(r => {
    const disciplineLabel = r.discipline || "Sem disciplina";
    const key = (r.discipline || "") + " " + (r.subject || "");
    const path = pathCache.get(key) || [];
    if (!root[disciplineLabel]) root[disciplineLabel] = { children: {}, items: {} };
    let node = root[disciplineLabel];
    path.forEach(seg => {
      if (!node.children[seg]) node.children[seg] = { children: {}, items: {} };
      node = node.children[seg];
    });
    const subjectLabel = r.subject || "Sem assunto";
    if (!node.items[subjectLabel]) node.items[subjectLabel] = [];
    node.items[subjectLabel].push(r);
  });
  return root;
}

// Renderiza recursivamente subpastas (seções) e, no nível mais interno, os
// assuntos-folha com seus itens (via `renderItem`, uma das duas funções de
// renderização já existentes: renderNotebookItem ou renderWrittenAnswerItem).
function renderHierNode(node, container, depth, renderItem) {
  Object.keys(node.children).sort((a, b) => a.localeCompare(b, "pt-BR", { numeric: true })).forEach(label => {
    const heading = document.createElement("div");
    heading.className = "hier-heading hier-section";
    heading.style.paddingLeft = (depth * 18) + "px";
    heading.textContent = "📁 " + label;
    container.appendChild(heading);
    renderHierNode(node.children[label], container, depth + 1, renderItem);
  });
  Object.keys(node.items).sort((a, b) => a.localeCompare(b, "pt-BR", { numeric: true })).forEach(subject => {
    const heading = document.createElement("div");
    heading.className = "hier-heading hier-subject";
    heading.style.paddingLeft = (depth * 18) + "px";
    heading.textContent = "📌 " + subject;
    container.appendChild(heading);
    node.items[subject].forEach(r => container.appendChild(renderItem(r)));
  });
}

async function renderHierarchical(records, container, renderItem) {
  await loadManifest();
  const root = await groupRecordsHierarchically(records);
  container.innerHTML = "";
  Object.keys(root).sort((a, b) => a.localeCompare(b, "pt-BR", { numeric: true })).forEach(disciplineLabel => {
    const heading = document.createElement("div");
    heading.className = "hier-heading hier-discipline";
    heading.textContent = "📚 " + disciplineLabel;
    container.appendChild(heading);
    renderHierNode(root[disciplineLabel], container, 1, renderItem);
  });
}

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
    if (!errors.length) {
      listEl.innerHTML = `<div class="notebook-empty">Nenhum erro por aqui${filter === "open" ? " — parabéns! 🎉" : "."}</div>`;
      return;
    }
    await renderHierarchical(errors, listEl, renderNotebookItem);
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
      <span class="notebook-item-meta">${modeLabel} · ${date}</span>
      <span class="notebook-item-score">${scoreTxt}</span>
    </div>
    <div class="notebook-item-question" title="Clique para refazer esta questão">${escapeHtml(err.question_text)}</div>
    <div class="notebook-item-answer">Sua resposta: ${escapeHtml(err.user_answer || "—")}</div>
    ${err.correct_answer ? `<div class="notebook-item-answer">Esperado: ${escapeHtml(err.correct_answer)}</div>` : ""}
    <div class="notebook-item-actions">
      <button class="btn-retry">🔁 Refazer questão</button>
      <button class="btn-lesson">📖 Ver mini-aula</button>
      <button class="btn-toggle-resolved">${err.resolved ? "↺ Reabrir" : "✔ Marcar como revisado"}</button>
      <button class="btn-delete">🗑 Excluir</button>
    </div>
  `;

  div.querySelector(".notebook-item-question").addEventListener("click", () => openRetryModal(err));
  div.querySelector(".btn-retry").addEventListener("click", () => openRetryModal(err));
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

// ---------- Respostas escritas (histórico completo de discursivas/orais) ----------

document.querySelectorAll("#writtenAnswersFilter .chip").forEach(chip => {
  chip.addEventListener("click", () => {
    document.querySelectorAll("#writtenAnswersFilter .chip").forEach(c => c.classList.remove("active"));
    chip.classList.add("active");
    loadWrittenAnswers(chip.dataset.filter);
  });
});

let writtenAnswersCache = [];

async function loadWrittenAnswers(filter) {
  const listEl = document.getElementById("writtenAnswersList");
  const subtitleEl = document.getElementById("writtenAnswersSubtitle");
  if (!state.currentUser) { listEl.innerHTML = ""; return; }
  subtitleEl.textContent = `Todas as respostas discursivas e orais que ${state.currentUser.name} já enviou, com a resposta padrão e a fonte, para consulta.`;
  listEl.innerHTML = "<p class='subtitle'>Carregando...</p>";

  try {
    const modes = filter === "all" ? ["discursive", "oral"] : [filter];
    const results = await Promise.all(modes.map(m =>
      fetch(`/api/answers?user_id=${state.currentUser.id}&mode=${m}`).then(r => r.json())
    ));
    const answers = results.flatMap(d => d.answers || []).sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
    writtenAnswersCache = answers;
    if (!answers.length) {
      listEl.innerHTML = `<div class="notebook-empty">Nenhuma resposta escrita registrada ainda.</div>`;
      return;
    }
    await renderHierarchical(answers, listEl, renderWrittenAnswerItem);
  } catch (e) {
    listEl.innerHTML = "<p class='subtitle'>Não foi possível carregar as respostas escritas.</p>";
  }
}

function renderWrittenAnswerItem(a) {
  const div = document.createElement("div");
  div.className = "notebook-item";
  const date = a.created_at ? a.created_at.replace("T", " ").slice(0, 16) : "";
  const modeLabel = { discursive: "Discursiva", oral: "Oral" }[a.mode] || a.mode;
  const scoreTxt = typeof a.score === "number" ? a.score.toFixed(1) + " / 10" : "—";

  div.innerHTML = `
    <div class="notebook-item-head">
      <span class="notebook-item-meta">${modeLabel} · ${date}</span>
      <span class="notebook-item-score">${scoreTxt}</span>
    </div>
    <div class="notebook-item-question">${escapeHtml(a.question_text || "")}</div>
    <div class="notebook-item-answer-view">Sua resposta: <span class="written-answer-text">${escapeHtml(a.user_answer || "—")}</span></div>
    <textarea class="written-answer-edit hidden" rows="4">${escapeHtml(a.user_answer || "")}</textarea>
    <details class="model-answer"><summary style="cursor:pointer;color:var(--accent)">Ver resposta padrão</summary>${a.model_answer || ""}</details>
    ${renderSourceLine(a.source)}
    <div class="notebook-item-actions">
      <button class="btn-edit-answer">✏️ Editar</button>
      <button class="btn-save-answer hidden">💾 Salvar</button>
      <button class="btn-cancel-edit-answer hidden">✕ Cancelar</button>
      <button class="btn-delete-answer">🗑 Excluir</button>
    </div>
  `;

  const viewEl = div.querySelector(".notebook-item-answer-view");
  const textEl = div.querySelector(".written-answer-text");
  const editEl = div.querySelector(".written-answer-edit");
  const editBtn = div.querySelector(".btn-edit-answer");
  const saveBtn = div.querySelector(".btn-save-answer");
  const cancelBtn = div.querySelector(".btn-cancel-edit-answer");
  const deleteBtn = div.querySelector(".btn-delete-answer");

  editBtn.addEventListener("click", () => {
    viewEl.classList.add("hidden");
    editEl.classList.remove("hidden");
    editBtn.classList.add("hidden");
    saveBtn.classList.remove("hidden");
    cancelBtn.classList.remove("hidden");
    editEl.focus();
  });

  cancelBtn.addEventListener("click", () => {
    editEl.value = a.user_answer || "";
    viewEl.classList.remove("hidden");
    editEl.classList.add("hidden");
    editBtn.classList.remove("hidden");
    saveBtn.classList.add("hidden");
    cancelBtn.classList.add("hidden");
  });

  saveBtn.addEventListener("click", async () => {
    const newText = editEl.value;
    saveBtn.disabled = true;
    try {
      await fetch("/api/answers/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: a.id, userAnswer: newText }),
      });
      a.user_answer = newText;
      textEl.textContent = newText || "—";
      const cached = writtenAnswersCache.find(x => x.id === a.id);
      if (cached) cached.user_answer = newText;
    } catch (e) {
      alert("Não foi possível salvar a edição. Verifique se o servidor está rodando.");
    } finally {
      saveBtn.disabled = false;
      viewEl.classList.remove("hidden");
      editEl.classList.add("hidden");
      editBtn.classList.remove("hidden");
      saveBtn.classList.add("hidden");
      cancelBtn.classList.add("hidden");
    }
  });

  deleteBtn.addEventListener("click", async () => {
    if (!confirm("Excluir esta resposta escrita? Essa ação não pode ser desfeita.")) return;
    await fetch("/api/answers/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: a.id }),
    });
    writtenAnswersCache = writtenAnswersCache.filter(x => x.id !== a.id);
    div.remove();
    if (!writtenAnswersCache.length) {
      document.getElementById("writtenAnswersList").innerHTML =
        '<div class="notebook-empty">Nenhuma resposta escrita registrada ainda.</div>';
    }
  });

  return div;
}

// Monta um PDF (via impressão do navegador) com todas as respostas escritas
// atualmente carregadas: pergunta, resposta dada e resposta padrão + fonte.
document.getElementById("writtenAnswersPdfBtn").addEventListener("click", () => {
  if (!writtenAnswersCache.length) {
    alert("Não há respostas escritas para incluir no PDF.");
    return;
  }
  openPrintableWrittenAnswers(writtenAnswersCache);
});

function openPrintableWrittenAnswers(answers) {
  const title = `Respostas escritas — ${state.currentUser ? state.currentUser.name : ""}`;
  const modeLabel = { discursive: "Discursiva", oral: "Oral" };

  const itemsHtml = answers.map((a, idx) => {
    const n = idx + 1;
    const date = a.created_at ? a.created_at.replace("T", " ").slice(0, 16) : "";
    const scoreTxt = typeof a.score === "number" ? a.score.toFixed(1) + " / 10" : "—";
    const srcTxt = a.source && a.source.document
      ? `${a.source.document}${a.source.page ? ", p. " + a.source.page : ""}`
      : "";
    return `<div class="pq">
      <p class="pq-head"><strong>${n}.</strong> <span class="pq-topic">${escapeHtml(a.discipline || "")} · ${escapeHtml(a.subject || "")} · ${modeLabel[a.mode] || a.mode} · ${date} · Nota: ${scoreTxt}</span></p>
      <p class="pq-text">${escapeHtml(a.question_text || "")}</p>
      <p class="pg-block"><strong>Sua resposta:</strong><br>${escapeHtml(a.user_answer || "—")}</p>
      <p class="pg-block"><strong>Resposta padrão:</strong><br>${(a.model_answer || "").replace(/\n/g, "<br>")}${srcTxt ? `<br><em>Fonte: ${escapeHtml(srcTxt)}</em>` : ""}</p>
    </div>`;
  }).join("");

  const html = `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>${escapeHtml(title)}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: Georgia, "Times New Roman", serif; color: #111; max-width: 800px; margin: 24px auto; padding: 0 16px; line-height: 1.5; }
  h1 { font-size: 20px; margin-bottom: 4px; }
  .print-meta { color: #444; font-size: 14px; margin: 0 0 20px; }
  .pq { margin-bottom: 26px; padding-bottom: 18px; border-bottom: 1px solid #ccc; page-break-inside: avoid; }
  .pq-head { margin: 0 0 2px; }
  .pq-topic { color: #666; font-size: 12px; font-style: italic; }
  .pq-text { margin: 4px 0 10px; font-weight: 600; }
  .pg-block { font-size: 14px; margin: 8px 0; }
  .print-actions { margin: 16px 0; }
  @media print { .print-actions { display: none; } }
</style>
</head>
<body>
  <div class="print-actions"><button onclick="window.print()">🖨️ Imprimir / Salvar PDF</button></div>
  <header>
    <h1>${escapeHtml(title)}</h1>
    <p class="print-meta">${answers.length} respostas · gerado pelo Professor Treinador</p>
  </header>
  <main>${itemsHtml}</main>
</body>
</html>`;

  const win = window.open("", "_blank");
  if (!win) {
    alert("Não foi possível abrir a janela de impressão. Permita pop-ups para este site e tente novamente.");
    return;
  }
  win.document.open();
  win.document.write(html);
  win.document.close();
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

// ---------- Modal: refazer questão errada (a partir do caderno de erros) ----------

const retryModal = document.getElementById("retryModal");
document.getElementById("retryModalClose").addEventListener("click", () => {
  window.speechSynthesis && window.speechSynthesis.cancel();
  retryModal.classList.add("hidden");
});
retryModal.addEventListener("click", (e) => {
  if (e.target === retryModal) {
    window.speechSynthesis && window.speechSynthesis.cancel();
    retryModal.classList.add("hidden");
  }
});

// Localiza, no banco de questões atual, a questão original referente a um
// registro do caderno de erros (o registro salva apenas question_id + texto,
// não a questão inteira — por isso é preciso ir buscá-la no bank).
async function findQuestionForError(err) {
  await loadManifest();
  let discipline = null;
  outer:
  for (const course of state.manifest.courses) {
    for (const sem of course.semesters) {
      discipline = (sem.disciplines || []).find(d => d.title === err.discipline);
      if (discipline) break outer;
    }
  }
  if (!discipline) return null;
  const bank = await loadBank(discipline);
  const pool = bank[err.mode] || [];
  return pool.find(q => q.id === err.question_id) || null;
}

async function openRetryModal(err) {
  const body = document.getElementById("retryModalBody");
  document.getElementById("retryModalTitle").textContent = "🔁 Refazer questão — " + (err.subject || "");
  body.innerHTML = "<p class='subtitle'>Carregando questão...</p>";
  retryModal.classList.remove("hidden");

  let q;
  try {
    q = await findQuestionForError(err);
  } catch (e) {
    q = null;
  }

  if (!q) {
    body.innerHTML = `<p class="subtitle">Não foi possível carregar esta questão do banco atual (o material pode ter sido atualizado desde então). Você ainda pode consultar sua resposta e a esperada diretamente no card do caderno de erros.</p>`;
    return;
  }

  if (err.mode === "objective") renderRetryObjective(err, q, body);
  else renderRetryOpen(err, q, body);
}

function retryQuestionHeaderHtml(q) {
  const meta = (q.topic || "") + (q.difficulty ? "  ·  " + (DIFF_LABEL[q.difficulty] || q.difficulty) : "");
  return `
    <p class="q-topic">${escapeHtml(meta)}</p>
    <h2 class="q-text">${escapeHtml(q.question)}</h2>
  `;
}

function renderRetryObjective(err, q, body) {
  body.innerHTML = `
    ${retryQuestionHeaderHtml(q)}
    <div id="retryOptions" class="options-list"></div>
    <div id="retryFeedback" class="feedback-box hidden"></div>
    <div class="action-row">
      <button id="retryConfirmBtn" class="primary-btn" disabled>Confirmar</button>
    </div>
  `;

  const optsEl = document.getElementById("retryOptions");
  let selectedKey = null;
  let confirmed = false;

  Object.entries(q.options).forEach(([key, text]) => {
    const item = document.createElement("div");
    item.className = "option-item";
    item.innerHTML = `<span class="option-letter">${key.toUpperCase()})</span><span>${text}</span>`;
    item.dataset.key = key;
    item.addEventListener("click", () => {
      if (confirmed) return;
      optsEl.querySelectorAll(".option-item").forEach(o => o.classList.remove("selected"));
      item.classList.add("selected");
      selectedKey = key;
      document.getElementById("retryConfirmBtn").disabled = false;
    });
    optsEl.appendChild(item);
  });

  document.getElementById("retryConfirmBtn").addEventListener("click", () => {
    confirmed = true;
    const correct = selectedKey === q.correct;
    optsEl.querySelectorAll(".option-item").forEach(o => {
      if (o.dataset.key === q.correct) o.classList.add("correct");
      else if (o.dataset.key === selectedKey) o.classList.add("incorrect");
    });

    const fb = document.getElementById("retryFeedback");
    fb.className = "feedback-box " + (correct ? "ok" : "bad");
    fb.innerHTML = `
      <div class="feedback-score ${correct ? "good" : "low"}">${correct ? "✔ Correto!" : "✘ Incorreto"}</div>
      ${q.explanation ? `<div>${q.explanation}</div>` : ""}
      ${!correct ? `<div style="margin-top:8px;color:var(--text-dim)">Resposta correta: <b>${q.correct.toUpperCase()}</b></div>` : ""}
      ${renderSourceLine(q.source)}
      ${correct && !err.resolved ? `<div class="action-row" style="margin-top:14px;"><button id="retryMarkResolvedBtn" class="primary-btn">✔ Marcar como revisado no caderno</button></div>` : ""}
    `;
    fb.classList.remove("hidden");
    document.getElementById("retryConfirmBtn").classList.add("hidden");

    if (correct && !err.resolved) {
      document.getElementById("retryMarkResolvedBtn").addEventListener("click", () => markErrorResolvedFromRetry(err));
    }
  });
}

function renderRetryOpen(err, q, body) {
  body.innerHTML = `
    ${retryQuestionHeaderHtml(q)}
    <textarea id="retryAnswer" rows="8" placeholder="Digite sua resposta aqui..."></textarea>
    <div id="retryFeedback" class="feedback-box hidden"></div>
    <div class="action-row">
      <button id="retrySubmitBtn" class="primary-btn">Enviar resposta</button>
    </div>
  `;

  document.getElementById("retrySubmitBtn").addEventListener("click", async () => {
    const textEl = document.getElementById("retryAnswer");
    const userText = textEl.value.trim();
    if (!userText) { alert("Escreva uma resposta antes de enviar."); return; }

    const btn = document.getElementById("retrySubmitBtn");
    btn.disabled = true;
    btn.textContent = "Avaliando...";
    textEl.disabled = true;

    const result = await gradeAnswer(q, userText);

    const fb = document.getElementById("retryFeedback");
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
      ${result.score >= 6 && !err.resolved ? `<div class="action-row" style="margin-top:14px;"><button id="retryMarkResolvedBtn" class="primary-btn">✔ Marcar como revisado no caderno</button></div>` : ""}
    `;
    fb.classList.remove("hidden");
    btn.classList.add("hidden");

    if (result.score >= 6 && !err.resolved) {
      document.getElementById("retryMarkResolvedBtn").addEventListener("click", () => markErrorResolvedFromRetry(err));
    }
  });
}

async function markErrorResolvedFromRetry(err) {
  err.resolved = 1;
  await fetch("/api/errors/resolve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: err.id, resolved: true }),
  });
  retryModal.classList.add("hidden");
  const activeFilterEl = document.querySelector("#notebookFilter .chip.active");
  if (activeFilterEl) loadNotebook(activeFilterEl.dataset.filter);
  refreshNotebookCount();
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
      await renderCourses();
      showScreen("screen-courses");
      return;
    }
  }
  clearUserLocal();
  showScreen("screen-login");
  loadUsersIntoLogin();
}

init();
checkAI();
