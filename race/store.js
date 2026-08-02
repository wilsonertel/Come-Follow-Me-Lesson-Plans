/* ------------------------------------------------------------------
   Scripture Race — storage

   One small interface with two implementations behind it:

     • firebase  — every racer on one live leaderboard (needs a config)
     • local     — this browser only, no setup, works offline

   Both expose the same four calls, so the page never has to care
   which one it got:

     store.subscribe(fn)              fn(racers) on every change
     store.addRacer(name, color)      -> racerId
     store.setChapter(id, ch, read)
     store.removeRacer(id)

   A racer looks like:  { id, name, color, read:{chapterId:true}, joined }
   ------------------------------------------------------------------ */

import { FIREBASE_CONFIG, DEFAULT_CLASS } from "./config.js";

const params     = new URLSearchParams(location.search);
export const CLASS_CODE = (params.get("class") || DEFAULT_CLASS).trim().toLowerCase();

const asArray = (obj) =>
  Object.entries(obj || {}).map(([id, r]) => ({
    id,
    name:   r.name || "Racer",
    color:  r.color || "#e8791e",
    read:   r.read || {},
    joined: r.joined || 0
  }));

/* ------------------------------ local ------------------------------ */

function localStore(){
  const KEY = `cfm-race:${CLASS_CODE}`;
  const listeners = new Set();

  const load = () => {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch { return {}; }
  };
  const save = (data) => {
    localStorage.setItem(KEY, JSON.stringify(data));
    emit();
  };
  const emit = () => {
    const racers = asArray(load());
    listeners.forEach((fn) => fn(racers));
  };

  // Keep two tabs on the same device in step.
  addEventListener("storage", (e) => { if (e.key === KEY) emit(); });

  return {
    mode: "local",
    subscribe(fn){ listeners.add(fn); fn(asArray(load())); },
    addRacer(name, color){
      const data = load();
      const id = "r" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
      data[id] = { name, color, read:{}, joined: Date.now() };
      save(data);
      return Promise.resolve(id);
    },
    setChapter(id, chapter, read){
      const data = load();
      if (!data[id]) return Promise.resolve();
      data[id].read = data[id].read || {};
      if (read) data[id].read[chapter] = true;
      else delete data[id].read[chapter];
      save(data);
      return Promise.resolve();
    },
    removeRacer(id){
      const data = load();
      delete data[id];
      save(data);
      return Promise.resolve();
    }
  };
}

/* ---------------------------- firebase ----------------------------- */

async function firebaseStore(){
  const CDN = "https://www.gstatic.com/firebasejs/10.12.2";
  const { initializeApp } = await import(`${CDN}/firebase-app.js`);
  const { getDatabase, ref, onValue, push, set, remove, serverTimestamp } =
    await import(`${CDN}/firebase-database.js`);

  const db   = getDatabase(initializeApp(FIREBASE_CONFIG));
  const root = ref(db, `race/${CLASS_CODE}/racers`);

  return {
    mode: "shared",
    subscribe(fn){
      onValue(root, (snap) => fn(asArray(snap.val())));
    },
    async addRacer(name, color){
      const node = push(root);
      await set(node, { name, color, read:{}, joined: serverTimestamp() });
      return node.key;
    },
    setChapter(id, chapter, read){
      const node = ref(db, `race/${CLASS_CODE}/racers/${id}/read/${chapter}`);
      return read ? set(node, true) : remove(node);
    },
    removeRacer(id){
      return remove(ref(db, `race/${CLASS_CODE}/racers/${id}`));
    }
  };
}

/* ---------------------------- selection ---------------------------- */

export async function openStore(){
  if (FIREBASE_CONFIG && FIREBASE_CONFIG.databaseURL){
    try { return await firebaseStore(); }
    catch (err){
      console.error("Shared leaderboard unavailable, falling back to this device only.", err);
      const s = localStore();
      s.degraded = true;
      return s;
    }
  }
  return localStore();
}

/* Which racer is using this device. */
const ME = `cfm-race-me:${CLASS_CODE}`;
export const getMyId  = ()   => localStorage.getItem(ME);
export const setMyId  = (id) => localStorage.setItem(ME, id);
export const clearMyId = ()  => localStorage.removeItem(ME);
