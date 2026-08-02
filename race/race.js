import { buildChapters } from "./data.js";
import { openStore, getMyId, setMyId, clearMyId, CLASS_CODE } from "./store.js";

const { weeks, flat, total } = buildChapters();

const CAR_COLORS = [
  { name:"Ember",   hex:"#e8791e" },
  { name:"Gold",    hex:"#e6b34a" },
  { name:"Teal",    hex:"#2f6f63" },
  { name:"Crimson", hex:"#c9384a" },
  { name:"Sky",     hex:"#3d8fd1" },
  { name:"Violet",  hex:"#7d5ba6" },
  { name:"Lime",    hex:"#6fa63b" },
  { name:"Rose",    hex:"#d9698f" }
];

const $  = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

const state = { store:null, racers:[], myId:null, manage:false };

const readCount = (r) => Object.keys(r.read || {}).length;
const me = () => state.racers.find((r) => r.id === state.myId) || null;

/* ------------------------------------------------------------------
   Pace car — how many chapters a student who never falls behind would
   have finished by today.
   ------------------------------------------------------------------ */
function paceChapters(today = new Date()){
  const day = (iso) => { const [y,m,d] = iso.split("-").map(Number); return new Date(y, m-1, d); };
  const now = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  let cum = 0;
  for (const w of weeks){
    const end   = day(w.end);
    const start = new Date(end); start.setDate(end.getDate() - 6);
    const n = w.chapters.length;
    if (now > end){ cum += n; continue; }
    if (now < start) return cum;
    const elapsed = Math.round((now - start) / 86400000) + 1;
    return cum + n * (elapsed / 7);
  }
  return cum;
}

/* ------------------------------------------------------------------
   Track
   ------------------------------------------------------------------ */
const track = {
  path: null, len: 0,
  init(){
    this.path = $("#trackline");
    this.len  = this.path.getTotalLength();
  },
  /* A point along the track, nudged sideways into its own lane. */
  at(fraction, lane = 0){
    const d  = Math.max(0, Math.min(1, fraction)) * this.len;
    const p  = this.path.getPointAtLength(d);
    const q  = this.path.getPointAtLength(Math.min(this.len, d + 1.5));
    let dx = q.x - p.x, dy = q.y - p.y;
    const m = Math.hypot(dx, dy) || 1;
    dx /= m; dy /= m;
    return {
      x: p.x + (-dy) * lane,
      y: p.y + ( dx) * lane,
      angle: Math.atan2(dy, dx) * 180 / Math.PI
    };
  }
};

/* A tick on the track wherever one week ends and the next begins. */
function drawWeekMarkers(){
  const host = $("#marks");
  let cum = 0;
  weeks.forEach((w) => {
    cum += w.chapters.length;
    if (cum === 0 || cum >= total) return;
    const a = track.at(cum / total, -21);
    const b = track.at(cum / total,  21);
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("class", "tick");
    line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
    host.appendChild(line);
  });
}

/* ------------------------------------------------------------------
   Build the week / chapter checklist once, then just toggle state.
   ------------------------------------------------------------------ */
function buildChecklist(){
  const host = $("#weeks");
  const todayWeek = weeks.findIndex((w) => {
    const [y,m,d] = w.end.split("-").map(Number);
    return new Date(y, m-1, d) >= new Date();
  });

  weeks.forEach((w) => {
    const box = document.createElement("details");
    box.className = "week";
    box.dataset.week = w.index;
    if (w.index === todayWeek) box.open = true;

    const sum = document.createElement("summary");
    sum.innerHTML =
      `<span class="w-dates"></span>
       <span class="w-scrip"></span>
       <span class="w-title"></span>
       <span class="w-tally"><b class="done">0</b>/<span class="of"></span></span>`;
    sum.querySelector(".w-dates").textContent = w.d;
    sum.querySelector(".w-scrip").textContent = w.s;
    sum.querySelector(".w-title").textContent = `“${w.t}”`;
    sum.querySelector(".of").textContent = w.chapters.length;
    box.appendChild(sum);

    const body = document.createElement("div");
    body.className = "w-body";

    if (!w.chapters.length){
      body.innerHTML =
        `<p class="w-note">The checkered flag. No chapters to read — this is the
         victory lap for everyone who finished the year.</p>`;
    } else {
      const chips = document.createElement("div");
      chips.className = "chips";
      w.chapters.forEach((c) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "chip";
        b.dataset.ch = c.id;
        b.setAttribute("aria-pressed", "false");
        b.innerHTML = `<span class="tick" aria-hidden="true"></span><span class="lab"></span>`;
        b.querySelector(".lab").textContent = c.label;
        chips.appendChild(b);
      });
      body.appendChild(chips);

      const row = document.createElement("div");
      row.className = "w-actions";
      row.innerHTML =
        `<button type="button" class="linky" data-all="${w.index}">Check the whole week</button>
         <a class="linky" href="">Open this week’s lesson page ›</a>`;
      row.querySelector("a").href = encodeURI(w.href);
      body.appendChild(row);
    }

    box.appendChild(body);
    host.appendChild(box);
  });

  host.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (chip) return toggleChapter(chip.dataset.ch);
    const all = e.target.closest("[data-all]");
    if (all) return checkWholeWeek(Number(all.dataset.all));
  });
}

function toggleChapter(id){
  const r = me();
  if (!r) return flashJoin();
  const now = !r.read[id];
  if (now) r.read[id] = true; else delete r.read[id];   // optimistic
  render();
  state.store.setChapter(r.id, id, now);
}

function checkWholeWeek(index){
  const r = me();
  if (!r) return flashJoin();
  const chapters = weeks[index].chapters;
  const allDone  = chapters.every((c) => r.read[c.id]);
  chapters.forEach((c) => {
    if (allDone) delete r.read[c.id]; else r.read[c.id] = true;
    state.store.setChapter(r.id, c.id, !allDone);
  });
  render();
}

function flashJoin(){
  const j = $("#join");
  j.scrollIntoView({ behavior:"smooth", block:"center" });
  j.classList.remove("nudge");
  void j.offsetWidth;
  j.classList.add("nudge");
}

/* ------------------------------------------------------------------
   Render
   ------------------------------------------------------------------ */
function render(){
  renderCars();
  renderLeaderboard();
  renderMe();
  renderChecklist();
}

function renderCars(){
  const layer  = $("#cars");
  const sorted = [...state.racers].sort((a, b) => a.joined - b.joined);
  const running = sorted.filter((r) => readCount(r) < total);
  const spread  = Math.min(13, 34 / Math.max(1, running.length));
  const seen    = new Set();
  let parked = 0;

  sorted.forEach((r) => {
    seen.add(r.id);
    const done = readCount(r) >= total;

    /* A finished lap lands back on the start line, which would make a
       winner look like they never left. Park them in the infield
       beside the flag instead. */
    const pos = done
      ? { x: 292 + (parked % 5) * 58, y: 162 + Math.floor(parked++ / 5) * 48, angle: 0 }
      : track.at(readCount(r) / total,
          (running.indexOf(r) - (running.length - 1) / 2) * spread);

    let g = layer.querySelector(`[data-racer="${r.id}"]`);
    if (!g){
      g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.dataset.racer = r.id;
      g.setAttribute("class", "car");
      g.innerHTML =
        `<g class="car-body">
           <rect class="tyre" x="-13" y="-10.5" width="7" height="3.5" rx="1.7"></rect>
           <rect class="tyre" x="-13" y="7" width="7" height="3.5" rx="1.7"></rect>
           <rect class="tyre" x="6" y="-10.5" width="7" height="3.5" rx="1.7"></rect>
           <rect class="tyre" x="6" y="7" width="7" height="3.5" rx="1.7"></rect>
           <rect class="shell" x="-17" y="-8.5" width="34" height="17" rx="5"></rect>
           <rect class="glass" x="-4" y="-6" width="11" height="12" rx="3"></rect>
           <rect class="wing" x="-17" y="-8.5" width="4" height="17" rx="2"></rect>
         </g>
         <text class="car-name" y="-23" text-anchor="middle"></text>`;
      layer.appendChild(g);
    }
    g.querySelector(".shell").setAttribute("fill", r.color);
    g.querySelector(".car-name").textContent = r.name;
    g.classList.toggle("is-me", r.id === state.myId);
    g.classList.toggle("finished", done);
    g.style.transform = `translate(${pos.x}px, ${pos.y}px)`;
    g.querySelector(".car-body").style.transform = `rotate(${pos.angle}deg) scale(var(--cs))`;
  });

  layer.querySelectorAll("[data-racer]").forEach((g) => {
    if (!seen.has(g.dataset.racer)) g.remove();
  });

  $("#victory").style.opacity = parked ? 1 : 0;

  // Pace car
  const pace = paceChapters();
  const pp   = track.at(pace / total, 0);
  const ghost = $("#pacecar");
  ghost.style.transform = `translate(${pp.x}px, ${pp.y}px)`;
  ghost.style.opacity = pace > 0 ? 1 : 0;
}

function renderLeaderboard(){
  const host = $("#board");
  host.innerHTML = "";

  if (!state.racers.length){
    host.innerHTML = `<p class="empty">No racers yet. Be the first on the grid.</p>`;
    return;
  }

  [...state.racers]
    .sort((a, b) => readCount(b) - readCount(a) || a.joined - b.joined)
    .forEach((r, i) => {
      const n   = readCount(r);
      const pct = Math.round((n / total) * 100);
      const row = document.createElement("div");
      row.className = "lb" + (r.id === state.myId ? " is-me" : "") + (n >= total ? " won" : "");
      row.innerHTML =
        `<span class="pos">${n >= total ? "🏁" : i + 1}</span>
         <span class="dot"></span>
         <span class="who"></span>
         <span class="num">${n}<small>/${total}</small></span>
         ${state.manage ? `<button class="kill" data-kill="${r.id}" title="Remove racer">×</button>` : ""}
         <span class="bar"><i></i></span>`;
      row.querySelector(".dot").style.background = r.color;
      row.querySelector(".who").textContent = r.name;
      row.querySelector(".bar i").style.width = pct + "%";
      row.querySelector(".bar i").style.background = r.color;
      host.appendChild(row);
    });
}

function renderMe(){
  const r = me();
  $("#join").hidden    = !!r;
  $("#mybar").hidden   = !r;
  if (!r) return;

  const n     = readCount(r);
  const pct   = (n / total) * 100;
  const pace  = paceChapters();
  const delta = n - pace;

  $("#me-name").textContent  = r.name;
  $("#me-name").style.color  = r.color;
  $("#me-read").textContent  = n;
  $("#me-left").textContent  = total - n;
  $("#me-pct").textContent   = pct.toFixed(pct >= 10 ? 0 : 1) + "%";
  $("#me-fill").style.width  = pct + "%";
  $("#me-fill").style.background = r.color;

  const tag = $("#me-pace");
  if (n >= total){
    tag.textContent = "🏁 Finished the race!";
    tag.className = "pacetag ahead";
  } else if (pace === 0){
    tag.textContent = "The race starts August 3";
    tag.className = "pacetag";
  } else if (delta >= 0){
    tag.textContent = `${Math.round(delta)} chapters ahead of pace`;
    tag.className = "pacetag ahead";
  } else {
    tag.textContent = `${Math.abs(Math.round(delta))} chapters behind pace`;
    tag.className = "pacetag behind";
  }

  $("#finish").hidden = n < total;
}

function renderChecklist(){
  const r = me();
  $("#weeks").classList.toggle("locked", !r);
  const read = r ? r.read : {};

  $$("#weeks .chip").forEach((chip) => {
    const on = !!read[chip.dataset.ch];
    chip.classList.toggle("on", on);
    chip.setAttribute("aria-pressed", String(on));
  });

  $$("#weeks .week").forEach((box) => {
    const w = weeks[Number(box.dataset.week)];
    const n = w.chapters.filter((c) => read[c.id]).length;
    box.querySelector(".done").textContent = n;
    box.classList.toggle("complete", w.chapters.length > 0 && n === w.chapters.length);
  });
}

/* ------------------------------------------------------------------
   Joining
   ------------------------------------------------------------------ */
function buildJoin(){
  const swatches = $("#colors");
  CAR_COLORS.forEach((c, i) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "swatch" + (i === 0 ? " on" : "");
    b.style.background = c.hex;
    b.dataset.hex = c.hex;
    b.title = c.name;
    b.setAttribute("aria-label", `${c.name} car`);
    swatches.appendChild(b);
  });
  swatches.addEventListener("click", (e) => {
    const s = e.target.closest(".swatch");
    if (!s) return;
    $$("#colors .swatch").forEach((x) => x.classList.remove("on"));
    s.classList.add("on");
  });

  $("#joinform").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = $("#name").value.trim().slice(0, 22);
    if (!name) return;
    const color = $("#colors .swatch.on")?.dataset.hex || CAR_COLORS[0].hex;
    $("#joinbtn").disabled = true;
    const id = await state.store.addRacer(name, color);
    setMyId(id);
    state.myId = id;
    $("#name").value = "";
    $("#joinbtn").disabled = false;
    render();
  });

  $("#claim").addEventListener("change", (e) => {
    const id = e.target.value;
    if (!id) return;
    setMyId(id);
    state.myId = id;
    render();
  });

  $("#switch").addEventListener("click", () => {
    clearMyId();
    state.myId = null;
    render();
  });

  $("#manage").addEventListener("click", () => {
    state.manage = !state.manage;
    $("#manage").textContent = state.manage ? "Done managing" : "Manage racers";
    renderLeaderboard();
  });

  $("#board").addEventListener("click", (e) => {
    const kill = e.target.closest("[data-kill]");
    if (!kill) return;
    const r = state.racers.find((x) => x.id === kill.dataset.kill);
    if (!r) return;
    if (!confirm(`Remove ${r.name} from the race? Their progress is deleted.`)) return;
    if (r.id === state.myId){ clearMyId(); state.myId = null; }
    state.store.removeRacer(r.id);
  });
}

function refreshClaimList(){
  const sel = $("#claim");
  const keep = sel.value;
  sel.innerHTML = `<option value="">Already racing? Pick your name…</option>`;
  [...state.racers]
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach((r) => {
      const o = document.createElement("option");
      o.value = r.id;
      o.textContent = `${r.name} — ${readCount(r)} chapters`;
      sel.appendChild(o);
    });
  sel.value = keep;
  $("#claimwrap").hidden = state.racers.length === 0;
}

/* ------------------------------------------------------------------
   Go
   ------------------------------------------------------------------ */
async function main(){
  $("#total").textContent    = total;
  $("#total2").textContent   = total;
  $("#classname").textContent = CLASS_CODE;

  track.init();
  drawWeekMarkers();
  buildChecklist();
  buildJoin();

  state.myId = getMyId();
  state.store = await openStore();

  /* A configured leaderboard that could not be reached must say so. If it
     quietly said "practice mode" instead, a student would keep checking
     chapters off into a roster nobody else can see. */
  const tag = $("#mode");
  if (state.store.degraded){
    tag.textContent = "Can’t reach the leaderboard — saved on this device only";
    tag.className = "modetag offline";
  } else if (state.store.mode === "shared"){
    tag.textContent = "Live class leaderboard";
    tag.className = "modetag shared";
  } else {
    tag.textContent = "Practice mode — this device only";
    tag.className = "modetag local";
  }

  state.store.subscribe((racers) => {
    state.racers = racers;
    if (state.myId && !racers.some((r) => r.id === state.myId)){
      clearMyId();
      state.myId = null;
    }
    refreshClaimList();
    render();
  });

  render();
  addEventListener("resize", renderCars);
}

main();
