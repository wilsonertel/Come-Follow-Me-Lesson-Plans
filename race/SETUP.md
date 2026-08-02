# Turning on the shared class leaderboard

The Scripture Race works the moment you open it — but until you do the steps
below it runs in **practice mode**, where each phone or laptop keeps its own
private roster. Kids can play with it, but they won't see each other.

To put the whole class on one live track, you need a free Firebase Realtime
Database. It takes about ten minutes, once, and costs nothing at this size.

---

## 1. Make the project

1. Go to <https://console.firebase.google.com> and sign in with a Google account.
2. **Add project** → name it something like `scripture-race` → Continue.
3. Turn **off** Google Analytics (you don't need it) → Create project.

## 2. Make the database

1. In the left sidebar: **Build → Realtime Database** → **Create Database**.
2. Pick a location near you.
3. Choose **Start in test mode** → Enable.

> Test mode leaves the database open to anyone for 30 days. Step 4 replaces
> those rules with something tighter, so do not skip it.

## 3. Get your config and paste it in

1. Click the ⚙️ gear next to **Project Overview** → **Project settings**.
2. Scroll to **Your apps** → click the web icon `</>`.
3. Nickname it `race`, skip Firebase Hosting, → **Register app**.
4. Firebase shows a block of code. You only need the `firebaseConfig` object.
5. Open **`race/config.js`** in this repo and replace `null` with it:

```js
export const FIREBASE_CONFIG = {
  apiKey: "AIzaSy…",
  authDomain: "scripture-race.firebaseapp.com",
  databaseURL: "https://scripture-race-default-rtdb.firebaseio.com",
  projectId: "scripture-race",
  appId: "1:000000000000:web:0000000000000000000000"
};
```

Make sure `databaseURL` is in there — that's the one the race actually uses.
If Firebase didn't show it, copy it off the Realtime Database page.

Commit and push. The tag at the top of the race page will flip from
"Practice mode" to **"Live class leaderboard"**.

## 4. Lock the rules down

In **Realtime Database → Rules**, replace what's there with:

```json
{
  "rules": {
    "race": {
      "$class": {
        "racers": {
          ".read": true,
          ".write": true,
          "$racer": {
            "name":   { ".validate": "newData.isString() && newData.val().length > 0 && newData.val().length <= 30" },
            "color":  { ".validate": "newData.isString() && newData.val().length <= 9" },
            "joined": { ".validate": "newData.isNumber()" },
            "read":   { "$chapter": { ".validate": "newData.isBoolean()" } }
          }
        }
      }
    }
  }
}
```

This keeps the race open — no logins for the kids — while making sure nothing
outside `race/*/racers` is writable, names stay short, and a chapter flag can
only ever be `true`.

> An earlier version of this file added `"$other": { ".validate": false }` to
> reject unrecognised keys. It was removed: a `$` wildcard sitting beside named
> keys at the same level may also match those named keys, in which case every
> write is rejected and nobody can join. It blocked only junk fields the page
> never reads, which is not worth that risk.

### What "open" honestly means

Your Firebase config ships inside a public web page, so it is not a secret.
Anyone who views the page source could add a racer or erase one. For a class
reading chart that's a fine trade for "no passwords for eight-year-olds," and
the rules above mean the worst case is a silly name on the leaderboard, which
you can delete with **Manage racers**. Don't store anything private here, and
don't reuse this Firebase project for anything that matters.

---

## Running more than one class

Send different groups to different tracks with a `?class=` on the link:

```
race/index.html?class=sunday-school
race/index.html?class=wilson-family
```

Each class code gets its own roster and its own leaderboard. Whatever you set
as `DEFAULT_CLASS` in `config.js` is what a plain link uses.

## Starting over

To clear the roster, open **Realtime Database → Data** in the Firebase console
and delete the `race` node. Everyone re-joins the next time they open the page.
