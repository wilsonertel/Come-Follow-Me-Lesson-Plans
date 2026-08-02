/* ------------------------------------------------------------------
   Scripture Race — settings
   ------------------------------------------------------------------ */

/* The name of your class. Everyone who opens the race with the same
   class code sees the same leaderboard. Students can also be sent to
   a different class with  race/index.html?class=sunbeams              */
export const DEFAULT_CLASS = "class-2026";

/* ------------------------------------------------------------------
   SHARED LEADERBOARD (optional)

   Leave this as  null  and the race runs in practice mode: everything
   works, but each device keeps its own copy of the roster.

   To put the whole class on one live track, create a free Firebase
   project with a Realtime Database, then paste its config object here.
   Step-by-step instructions are in race/SETUP.md.
   ------------------------------------------------------------------ */
export const FIREBASE_CONFIG = {
  apiKey: "AIzaSyBDLl1WiPlx_zkVRNCjeW90e4hBugNHMeg",
  authDomain: "scripture-race.firebaseapp.com",
  databaseURL: "https://scripture-race-default-rtdb.firebaseio.com",
  projectId: "scripture-race",
  storageBucket: "scripture-race.firebasestorage.app",
  messagingSenderId: "403376175896",
  appId: "1:403376175896:web:f8d5dfc41666d32d977c6d"
};

/*  Example of a filled-in config:

export const FIREBASE_CONFIG = {
  apiKey: "AIzaSy…",
  authDomain: "scripture-race.firebaseapp.com",
  databaseURL: "https://scripture-race-default-rtdb.firebaseio.com",
  projectId: "scripture-race",
  appId: "1:000000000000:web:0000000000000000000000"
};
*/
