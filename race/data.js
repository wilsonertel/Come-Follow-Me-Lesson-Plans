/* ------------------------------------------------------------------
   Scripture Race — course data
   Every Come, Follow Me chapter from August 3, 2026 to the end of the
   year. Weeks, dates, titles and folder names match the official
   outline as listed on the home page.
   ------------------------------------------------------------------ */

/* Each week:
     d    date range shown to students
     s    scripture block (as printed in the outline)
     t    lesson title
     u    folder under lessons/2026 - Old Testament/
     end  last day of the week (used for the pace car)
     r    refs: [display book, id slug, [[firstCh, lastCh], ...]]      */

export const WEEKS = [
  { d:"August 3–9", s:"Esther", t:"Thou Art Come … for Such a Time as This",
    u:"August/august-3-9-esther", end:"2026-08-09",
    r:[["Esther","esther",[[1,10]]]] },

  { d:"August 10–16", s:"Job 1–3; 12–14; 19; 21–24; 38–40; 42", t:"Yet Will I Trust in Him",
    u:"August/august-10-16-job-1-3-12-14-19-21-24-38-40-42", end:"2026-08-16",
    r:[["Job","job",[[1,3],[12,14],[19,19],[21,24],[38,40],[42,42]]]] },

  { d:"August 17–23", s:"Psalms 1–2; 8; 19–33; 40; 46", t:"The Lord Is My Shepherd",
    u:"August/august-17-23-psalms-1-2-8-19-33-40-46", end:"2026-08-23",
    r:[["Psalm","ps",[[1,2],[8,8],[19,33],[40,40],[46,46]]]] },

  { d:"August 24–30", s:"Psalms 49–51; 61–66; 69–72; 77–78; 85–86", t:"I Will Declare What He Hath Done for My Soul",
    u:"August/august-24-30-psalms-49-51-61-66-69-72-77-78-85-86", end:"2026-08-30",
    r:[["Psalm","ps",[[49,51],[61,66],[69,72],[77,78],[85,86]]]] },

  { d:"August 31 – September 6", s:"Psalms 102–103; 110; 116–119; 127–128; 135–139; 146–150",
    t:"Let Every Thing That Hath Breath Praise the Lord",
    u:"September/august-31-september-6-psalms-102-103-110-116-119-127-128-135-139-146-150", end:"2026-09-06",
    r:[["Psalm","ps",[[102,103],[110,110],[116,119],[127,128],[135,139],[146,150]]]] },

  { d:"September 7–13", s:"Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12", t:"He Shall Direct Thy Paths",
    u:"September/september-7-13-proverbs-1-4-15-16-22-31-ecclesiastes-1-3-11-12", end:"2026-09-13",
    r:[["Proverbs","prov",[[1,4],[15,16],[22,22],[31,31]]],
       ["Ecclesiastes","eccl",[[1,3],[11,12]]]] },

  { d:"September 14–20", s:"Isaiah 1–12", t:"God Is My Salvation",
    u:"September/september-14-20-isaiah-1-12", end:"2026-09-20",
    r:[["Isaiah","isa",[[1,12]]]] },

  { d:"September 21–27", s:"Isaiah 13–14; 22; 24–30; 35", t:"A Marvellous Work and a Wonder",
    u:"September/september-21-27-isaiah-13-14-22-24-30-35", end:"2026-09-27",
    r:[["Isaiah","isa",[[13,14],[22,22],[24,30],[35,35]]]] },

  { d:"September 28 – October 4", s:"Isaiah 40–49", t:"Comfort Ye My People",
    u:"October/september-28-october-4-isaiah-40-49", end:"2026-10-04",
    r:[["Isaiah","isa",[[40,49]]]] },

  { d:"October 5–11", s:"Isaiah 50–57", t:"He Hath Borne Our Griefs, and Carried Our Sorrows",
    u:"October/october-5-11-isaiah-50-57", end:"2026-10-11",
    r:[["Isaiah","isa",[[50,57]]]] },

  { d:"October 12–18", s:"Isaiah 58–66", t:"The Redeemer Shall Come to Zion",
    u:"October/october-12-18-isaiah-58-66", end:"2026-10-18",
    r:[["Isaiah","isa",[[58,66]]]] },

  { d:"October 19–25", s:"Jeremiah 1–3; 7; 16–18; 20", t:"Before I Formed Thee in the Belly I Knew Thee",
    u:"October/october-19-25-jeremiah-1-3-7-16-18-20", end:"2026-10-25",
    r:[["Jeremiah","jer",[[1,3],[7,7],[16,18],[20,20]]]] },

  { d:"October 26 – November 1", s:"Jeremiah 31–33; 36–39; Lamentations 1; 3", t:"I Will Turn Their Mourning into Joy",
    u:"November/october-26-november-1-jeremiah-31-33-36-39-lamentations-1-3", end:"2026-11-01",
    r:[["Jeremiah","jer",[[31,33],[36,39]]],
       ["Lamentations","lam",[[1,1],[3,3]]]] },

  { d:"November 2–8", s:"Ezekiel 1–3; 33–34; 36–37; 47", t:"A New Spirit Will I Put within You",
    u:"November/november-2-8-ezekiel-1-3-33-34-36-37-47", end:"2026-11-08",
    r:[["Ezekiel","ezek",[[1,3],[33,34],[36,37],[47,47]]]] },

  { d:"November 9–15", s:"Daniel 1–7", t:"There Is No Other God That Can Deliver",
    u:"November/november-9-15-daniel-1-7", end:"2026-11-15",
    r:[["Daniel","dan",[[1,7]]]] },

  { d:"November 16–22", s:"Hosea 1–6; 10–14; Joel", t:"I Will Love Them Freely",
    u:"November/november-16-22-hosea-1-6-10-14-joel", end:"2026-11-22",
    r:[["Hosea","hos",[[1,6],[10,14]]],
       ["Joel","joel",[[1,3]]]] },

  { d:"November 23–29", s:"Amos; Obadiah; Jonah", t:"Seek the Lord, and Ye Shall Live",
    u:"November/november-23-29-amos-obadiah-jonah", end:"2026-11-29",
    r:[["Amos","amos",[[1,9]]],
       ["Obadiah","obad",[[1,1]]],
       ["Jonah","jonah",[[1,4]]]] },

  { d:"November 30 – December 6", s:"Micah; Nahum; Habakkuk; Zephaniah", t:"He Delighteth in Mercy",
    u:"December/november-30-december-6-micah-nahum-habakkuk-zephaniah", end:"2026-12-06",
    r:[["Micah","micah",[[1,7]]],
       ["Nahum","nahum",[[1,3]]],
       ["Habakkuk","hab",[[1,3]]],
       ["Zephaniah","zeph",[[1,3]]]] },

  { d:"December 7–13", s:"Haggai 1–2; Zechariah 1–4; 7–14", t:"Holiness unto the Lord",
    u:"December/december-7-13-haggai-1-2-zechariah-1-4-7-14", end:"2026-12-13",
    r:[["Haggai","hag",[[1,2]]],
       ["Zechariah","zech",[[1,4],[7,14]]]] },

  { d:"December 14–20", s:"Malachi", t:"I Have Loved You, Saith the Lord",
    u:"December/december-14-20-malachi", end:"2026-12-20",
    r:[["Malachi","mal",[[1,4]]]] },

  { d:"December 21–27", s:"Christmas", t:"We Have Waited for Him, and He Will Save Us",
    u:"December/december-21-27-christmas", end:"2026-12-27",
    r:[] }
];

/* Expand the ranges into a flat, ordered list of chapters. */
export function buildChapters(){
  const weeks = [];
  const flat  = [];
  WEEKS.forEach((w, wi) => {
    const chapters = [];
    w.r.forEach(([book, slug, ranges]) => {
      ranges.forEach(([a, b]) => {
        for (let c = a; c <= b; c++){
          const ch = { id:`${slug}-${c}`, book, num:c, label:`${book} ${c}`, week:wi };
          chapters.push(ch);
          flat.push(ch);
        }
      });
    });
    weeks.push({ ...w, index:wi, chapters, href:`../lessons/2026 - Old Testament/${w.u}/index.html` });
  });
  return { weeks, flat, total: flat.length };
}
