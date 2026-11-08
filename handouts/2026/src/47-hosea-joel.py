# Week 47 · November 16–22, 2026 · Hosea 1–6; 10–14; Joel — "I Will Love Them Freely"
# Content only. Layout lives in template/build.py. Build with:
#     python3 template/build.py build handouts/2026/src/47-hosea-joel.py
# Research notes and sources: notes/research-log.md (2026 · Week 47) and notes/outlines/2026-47-*.md
from build import (p, lead, h3, card, pull, steps, parallel_cards, points, helps,
                   resto, ideas, christ)

HERO_SVG = """<svg width="200" height="220" viewBox="0 0 200 220">
<defs>
 <radialGradient id="dawn" cx=".5" cy=".62" r=".6"><stop offset="0" stop-color="#f6c66a" stop-opacity=".75"/><stop offset=".55" stop-color="#e2708a" stop-opacity=".28"/><stop offset="1" stop-color="#e2708a" stop-opacity="0"/></radialGradient>
 <linearGradient id="petal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf3"/><stop offset="1" stop-color="#f6cdd6"/></linearGradient>
 <radialGradient id="fadeR" cx=".5" cy=".55" r=".55"><stop offset=".7" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
 <mask id="soft"><rect width="200" height="220" fill="url(#fadeR)"/></mask>
</defs>
<g mask="url(#soft)">
<circle cx="100" cy="136" r="96" fill="url(#dawn)"/>
<path d="M58 150 a42 42 0 0 1 84 0 Z" fill="#f2c46d"/>
<path d="M0 150 Q50 136 100 148 T200 144 V220 H0 Z" fill="#1b1326"/>
<path d="M0 150 Q50 136 100 148 T200 144" fill="none" stroke="#f4a0b2" stroke-opacity=".55" stroke-width="1.5"/>
</g>
<path d="M100 214 C100 190 101 160 100 118" stroke="#6fae93" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M100 190 C82 186 70 172 66 156 C84 160 96 172 100 190 Z" fill="#4f8f78"/>
<path d="M101 176 C118 172 130 160 134 144 C116 148 104 160 101 176 Z" fill="#5f9f86"/>
<path d="M100 120 C88 104 88 82 100 62 C112 82 112 104 100 120 Z" fill="url(#petal)"/>
<path d="M99 121 C82 116 70 100 66 80 C84 86 96 100 99 121 Z" fill="url(#petal)"/>
<path d="M101 121 C118 116 130 100 134 80 C116 86 104 100 101 121 Z" fill="url(#petal)"/>
<g fill="#cfe8f4" stroke="#ffffff" stroke-opacity=".7" stroke-width=".8">
 <path d="M70 162 c0 -4 3 -7 3 -7 s3 3 3 7 a3 3 0 0 1 -6 0 Z"/>
 <path d="M128 150 c0 -4 3 -7 3 -7 s3 3 3 7 a3 3 0 0 1 -6 0 Z"/>
 <path d="M140 116 c0 -3 2.4 -5.5 2.4 -5.5 s2.4 2.5 2.4 5.5 a2.4 2.4 0 0 1 -4.8 0 Z" opacity=".8"/>
 <path d="M56 124 c0 -3 2.4 -5.5 2.4 -5.5 s2.4 2.5 2.4 5.5 a2.4 2.4 0 0 1 -4.8 0 Z" opacity=".8"/>
</g>
</svg>"""

# ---------------------------------------------------------------- 1. HISTORY
HISTORY = [
    p("**When.** Hosea preached in the **8th century BC**, in the northern kingdom of Israel. His book opens by naming the kings he lived under: Uzziah, Jotham, Ahaz, and Hezekiah of Judah, and “Jeroboam the son of Joash, king of Israel” ([[Hosea 1:1]]). That is **Jeroboam II**, who reigned about **786–746 BC** and was the longest-reigning king the northern kingdom ever had ([[2 Kings 14:23–25]]). Hosea is the only prophet from the northern kingdom whose writings we still have (Bible Dictionary, “Hosea”)."),
    p("**Rich, then falling apart.** Under Jeroboam II the north was prosperous. Its farms, olive presses, and vineyards were busy, and the land was full of people. But Hosea saw what the money was doing to hearts: “they were filled, and their heart was exalted; therefore have they forgotten me” ([[Hosea 13:6]]). After Jeroboam died, Israel had **six kings in about 25 years, and four of them were assassinated** ([[2 Kings 15:10|2 Kings 15:10]], [[2 Kings 15:14|14]], [[2 Kings 15:25|25]], [[2 Kings 15:30|30]]). Hosea’s line “We have no king, because we feared not the Lord” ([[Hosea 10:3]]) fits that chaos."),
    p("**Who was in power.** The superpower was **Assyria**. Its king **Tiglath-pileser III** (ruled 745–727 BC), called “Pul” in the Bible, forced King Menahem to pay a thousand talents of silver ([[2 Kings 15:19]]). Israel’s leaders zigzagged between Assyria and Egypt for protection. Hosea mocks them as running to Assyria for a cure that can’t heal ([[Hosea 5:13]]) and making “a covenant with the Assyrians” while sending “oil… into Egypt” ([[Hosea 12:1]]). When Israel’s last king, Hoshea, stopped paying tribute and turned to Egypt, Assyria besieged Samaria for three years. The city fell in **722/721 BC**, and the people were carried away into Assyria ([[2 Kings 17:4–6]]). These are the “lost ten tribes.”"),
    p("**Where.** Hosea often calls the northern kingdom **Ephraim**, after its largest tribe. Its capital was **Samaria**. Nearly two centuries earlier, Jeroboam I had set up golden calves at **Bethel** and **Dan** ([[1 Kings 12:28–29]]). Bethel means “house of God,” but Hosea sarcastically renames it **Beth-aven**, “house of wickedness” ([[Hosea 4:15]]; [[Hosea 10:5]]). Other places in the book are the **valley of Jezreel**, where King Jehu seized the throne in a bloodbath ([[Hosea 1:4]]), and Gilgal and Gilead."),
    p("**Culture and faith.** Israel was a farming society that lived or died by rain. Its neighbors worshipped **Baal**, a Canaanite storm god believed to send rain and fertile harvests. Many Israelites kept the Lord’s feast days while also thanking Baal for the crops. Hosea’s complaint is exactly that: “she did not know that I gave her corn, and wine, and oil” ([[Hosea 2:8]]). In Hosea, “whoredom” and “adultery” are mostly a picture for this divided loyalty: breaking a covenant with God by giving His love to someone else."),
    p("**Joel** is different. He preached in **Judah**, the southern kingdom, and he never names a king, so no one knows when he lived. Scripture Helps says “probably somewhere between the ninth and fifth centuries BC.” His message came after a terrible **locust plague and drought** ([[Joel 1:4]]; [[Joel 1:10–12]]), and he speaks to priests at a working temple ([[Joel 1:13–14]])."),
    card("Archaeology anchors",
         "**The Black Obelisk of Shalmaneser III** (British Museum). Found by Austen Henry Layard at Nimrud in 1846, it shows a king of Israel bowing to the Assyrian king, labeled “Yaua of Bit-Omri.” Most scholars read this as **Jehu**, the founder of the dynasty condemned in [[Hosea 1:4]]. A few think it means a different king, so call it the most likely reading. If it is Jehu, it is the earliest known picture of a biblical figure.",
         "**The Samaria Ostraca** (Istanbul Archaeology Museums). In 1910 a Harvard team led by George Reisner dug up 102 inscribed pottery shards at Samaria’s royal palace, 63 of them readable. They are 8th-century receipts for deliveries of **wine and fine olive oil**, dated by a king’s regnal years. Many scholars think the king was Jeroboam II. They are a real snapshot of the economy Hosea preached to (“corn, and wine, and oil,” [[Hosea 2:8]]). Most of the people’s names honor the Lord, but some are built on **Baal**, the same divided loyalty Hosea describes in [[Hosea 2:16–17]].",
         "**Kuntillet ʿAjrud** (Sinai, c. 800 BC). Ink inscriptions at this desert waystation, linked to the northern kingdom, give blessings by “Yahweh of Samaria and his asherah.” Scholars debate whether “asherah” means a goddess or a sacred wooden pole. Either way, the inscriptions show the kind of mixed worship Hosea condemned, from his own century.",
         "**Sargon II’s inscriptions.** The Assyrian king boasts of taking Samaria and resettling about **27,000** of its people across his empire. That matches [[2 Kings 17:6]], the deportation Hosea warned was coming."),
    card("Hosea and Joel at a glance",
         "**Hosea** (14 chapters). **Chapters 1–3:** Hosea’s marriage to Gomer, their three children, her unfaithfulness, and his effort to bring her home. **Chapters 4–14:** the Lord’s case against Israel, mixed with some of the most tender promises in scripture. This week’s reading skips chapters 7–9.",
         "**Joel** (3 chapters). **Chapter 1:** the locusts and the drought. **2:1–17:** the “day of the Lord” and a call to come back with all your heart. **2:18–32:** restored harvests and the Spirit poured out. **Chapter 3:** the nations judged in “the valley of decision,” and a fountain flowing from the house of the Lord.",
         "**Locusts in living memory.** In 1915 a locust plague stripped the land around Jerusalem from spring to fall. John D. Whiting of the American Colony photographed it and wrote “Jerusalem’s Locust Plague” for *National Geographic* (December 1915), quoting Joel again and again. Joel’s description was not exaggerated."),
    card("Honest note: what scholars still debate",
         "**Was Hosea’s marriage literal or symbolic?** Scripture Helps says scholars “have long debated” this, and that either way the message is the same: the covenant between God and Israel. **Is the woman in Hosea 3 Gomer?** The chapter doesn’t name her. Most readers, including the manual’s artwork, assume she is.",
         "**How long did Hosea preach?** The Bible Dictionary thinks he probably died before about 736 BC, because he never mentions the wars and deportations that followed. Other scholars stretch his ministry to the 720s, since [[Hosea 1:1]] names Hezekiah. **Who is “king Jareb”** ([[Hosea 5:13]]; [[Hosea 10:6]])? No such king is known. It may be a title, something like “the great king,” rather than a name. **When did Joel live?** Proposals run from the 800s BC to after the exile. It’s fine to tell students we don’t know.",
         warm=True),
]

# ---------------------------------------------------------------- 2. PASSAGE SUMMARY
SUMMARY = [
    lead("Hosea starts with a family, turns into a courtroom, and ends with a love song. Joel goes from a locust plague to the Spirit poured out on everyone."),
    steps([
        ("[[Hosea 1]]", "A family that becomes a sermon",
         "The Lord tells Hosea to marry Gomer, and her unfaithfulness becomes a picture of Israel’s. Their three children carry names like warning signs. **Jezreel** (“God sows”) recalls the bloodshed in the valley of Jezreel ([[Hosea 1:4]]). **Lo-ruhamah** means “not pitied” or “no mercy” ([[Hosea 1:6]]). **Lo-ammi** means “not my people” ([[Hosea 1:9]]). But the chapter won’t end there: in the very place where they were called “not my people,” they will be called “the sons of the living God” ([[Hosea 1:10]])."),
        ("[[Hosea 2:1–13]]", "The case against an unfaithful bride",
         "Israel is the wife who says, “I will go after my lovers, that give me my bread and my water” ([[Hosea 2:5]]). She never realized it was the Lord who “gave her corn, and wine, and oil” ([[Hosea 2:8]]). So He will “hedge up thy way with thorns” ([[Hosea 2:6]]). Some consequences are walls built in love, so she will finally say, “I will go and return to my first husband” ([[Hosea 2:7]])."),
        ("[[Hosea 2:14–23]]", "The Lord wins her back",
         "Instead of rejecting her, the Lord will “allure her, and bring her into the wilderness, and speak comfortably unto her” ([[Hosea 2:14]]). He will turn “the valley of Achor” into “a door of hope” ([[Hosea 2:15]]). Achor, which means “trouble,” was where Achan’s sin was punished ([[Joshua 7:24–26]]), so even the place of failure becomes an entrance. She will call Him **Ishi**, “my husband,” not **Baali** ([[Hosea 2:16]]). He will “betroth thee unto me for ever” in righteousness, judgment, lovingkindness, mercies, and faithfulness ([[Hosea 2:19–20]]). The children’s names are reversed: “Thou art my people… Thou art my God” ([[Hosea 2:23]])."),
        ("[[Hosea 3]]", "Love that pays the price",
         "“Go yet, love a woman… according to the love of the Lord toward the children of Israel” ([[Hosea 3:1]]). Hosea **buys her back** for fifteen pieces of silver and a homer and a half of barley ([[Hosea 3:2]]). Israel will go “many days without a king,” and then “in the latter days” will “return, and seek the Lord their God, and David their king” ([[Hosea 3:4–5]])."),
        ("[[Hosea 4]]–5", "The Lord’s lawsuit",
         "The Lord has “a controversy” with the land: “no truth, nor mercy, nor knowledge of God” ([[Hosea 4:1]]). “My people are destroyed for lack of knowledge” ([[Hosea 4:6]]), and the priests are as guilty as anyone: “like people, like priest” ([[Hosea 4:9]]). Ephraim runs to Assyria for healing that never comes ([[Hosea 5:13]]). So the Lord steps back “till they acknowledge their offence, and seek my face” ([[Hosea 5:15]])."),
        ("[[Hosea 6]]", "Goodness that evaporates",
         "The people sing, “Come, and let us return unto the Lord: for he hath torn, and he will heal us” ([[Hosea 6:1–3]]). But the Lord sees through it: “your goodness is as a morning cloud, and as the early dew it goeth away” ([[Hosea 6:4]]). What He wants is “mercy, and not sacrifice; and the knowledge of God more than burnt offerings” ([[Hosea 6:6]]). They kept the rituals and broke the covenant ([[Hosea 6:7]])."),
        ("[[Hosea 10]]", "An empty vine and an unplowed field",
         "“Israel is an empty vine, he bringeth forth fruit unto himself” ([[Hosea 10:1]]). “Their heart is divided” ([[Hosea 10:2]]), and the golden calf of Beth-aven will be hauled off to Assyria as tribute ([[Hosea 10:5–6]]). Then comes the farming invitation the children’s section uses: “Sow to yourselves in righteousness, reap in mercy; break up your fallow ground: for it is time to seek the Lord” ([[Hosea 10:12]]). What they have actually planted is wickedness ([[Hosea 10:13]])."),
        ("[[Hosea 11]]", "A father teaching a toddler to walk",
         "“When Israel was a child, then I loved him, and called my son out of Egypt” ([[Hosea 11:1]]). “I taught Ephraim also to go, taking them by their arms” and drew them “with bands of love” ([[Hosea 11:3–4]]). Then comes the most heartbroken verse in the book: “How shall I give thee up, Ephraim?” Admah and Zeboim were cities destroyed along with Sodom ([[Deuteronomy 29:23]]), and the Lord cannot bear to do that to His child: “mine heart is turned within me” ([[Hosea 11:8]]). “I am God, and not man” ([[Hosea 11:9]]), so His love outlasts ours."),
        ("[[Hosea 12]]–13", "Remember Jacob; there is no other Savior",
         "Israel’s ancestor Jacob wrestled, “wept, and made supplication” ([[Hosea 12:3–4]]), and the invitation is to do the same: “turn thou to thy God: keep mercy and judgment, and wait on thy God continually” ([[Hosea 12:6]]). The Lord reminds them, “there is no saviour beside me” ([[Hosea 13:4]]), and “O Israel, thou hast destroyed thyself; but in me is thine help” ([[Hosea 13:9]]). He promises, “I will ransom them from the power of the grave… O death, I will be thy plagues” ([[Hosea 13:14]])."),
        ("[[Hosea 14]]", "“I will love them freely”",
         "The book ends with an invitation and even supplies the words to pray: “Take with you words, and turn to the Lord” ([[Hosea 14:1–2]]). Instead of sacrificed bulls, Israel will offer “the calves of our lips,” meaning praise and confession ([[Hosea 14:2]]). The Lord answers: “I will heal their backsliding, I will love them freely” ([[Hosea 14:4]]). Then Hosea turns to plants: dew, a lily, roots like Lebanon’s cedars, an olive tree, grain, a vine ([[Hosea 14:5–7]]). Finally Ephraim asks, “What have I to do any more with idols?” ([[Hosea 14:8]])."),
        ("[[Joel 1]]–[[Joel 2:17|2:17]]", "Locusts, and a call to come home",
         "Wave after wave of insects strips the land: “That which the palmerworm hath left hath the locust eaten” ([[Joel 1:4]]). These are probably stages or kinds of locust. Vines, fig trees, and grain are gone, and even the temple offerings stop ([[Joel 1:9–13]]). Joel calls a fast and a solemn assembly in the house of the Lord ([[Joel 1:14]]). He sees an even greater “day of the Lord” coming and asks, “who can abide it?” ([[Joel 2:11]]). The answer: “turn ye even to me with all your heart… And rend your heart, and not your garments” ([[Joel 2:12–13]]). Everyone is to gather, even the children, and even a bride and groom on their wedding day ([[Joel 2:16]])."),
        ("[[Joel 2:18–32]]", "Restoration, and the Spirit poured out",
         "The Lord will send grain, wine, and oil again ([[Joel 2:19]]) and promises, “I will restore to you the years that the locust hath eaten” ([[Joel 2:25]]). Then the great promise: “I will pour out my spirit upon all flesh; and your sons and your daughters shall prophesy, your old men shall dream dreams, your young men shall see visions” ([[Joel 2:28–29]]). Signs in the sun and moon come before the day of the Lord ([[Joel 2:30–31]]), and “whosoever shall call on the name of the Lord shall be delivered” ([[Joel 2:32]])."),
        ("[[Joel 3]]", "The valley of decision",
         "The nations that scattered Israel are gathered to “the valley of Jehoshaphat,” a name meaning “the Lord judges” ([[Joel 3:2]]; [[Joel 3:12]]). Joel flips Isaiah’s famous line, “Beat your plowshares into swords” ([[Joel 3:10]]; compare [[Isaiah 2:4]]): the nations arm themselves, but it won’t help them. “Multitudes, multitudes in the valley of decision” ([[Joel 3:14]]). Yet “the Lord will be the hope of his people” ([[Joel 3:16]]), and “a fountain shall come forth of the house of the Lord” ([[Joel 3:18]]). That is the same image as Ezekiel’s temple river from last week ([[Ezekiel 47:1]])."),
    ]),
    card("Hard questions students may ask",
         "**Why would God tell a prophet to marry an unfaithful woman?** Scripture Helps says scholars have long debated whether this was literal or symbolic. Either way, God isn’t approving of unfaithfulness. The story is meant to hurt. It lets us feel what broken covenants feel like from God’s side, and then how far He will go to restore them.",
         "**Is God’s anger the opposite of His love?** In Hosea He is described as a lion and a bear ([[Hosea 13:7–8]]), but this is the anger of a betrayed husband and parent, and it is never the last word. His heart “is turned within” Him ([[Hosea 11:8]]), and at the end His “anger is turned away” ([[Hosea 14:4]]). Many of Israel’s troubles were the natural result of their own choices: “thou hast destroyed thyself; but in me is thine help” ([[Hosea 13:9]]).",
         "**What about the violent verses?** [[Hosea 13:16]] describes what Assyrian armies really did to conquered cities. Prophets described those horrors as warnings, the way a doctor warns what an untreated disease will do. They were not cheering for it.",
         "**Were Joel’s locusts real?** Most modern interpreters think Joel saw a real plague and used it as a picture of a coming “day of the Lord.” Some ancient Jewish readers took the locusts as symbols for invading armies. The Lord Himself calls them “my great army” ([[Joel 2:25]]).",
         "**Hasn’t Joel 2:28 already happened?** Scripture Helps says it has “multiple fulfillments”: Peter said it was happening on the day of Pentecost ([[Acts 2:16–21]]), and in 1823 Moroni told Joseph Smith it “was not yet fulfilled, but was soon to be” ([[Joseph Smith—History 1:41]]).",
         warm=True),
    card("Word study: hesed",
         "The Hebrew word **hesed** means loyal, covenant-keeping love. The KJV translates it several ways, so it’s easy to miss how often Hosea uses it. It is the “lovingkindness” the Lord promises in [[Hosea 2:19]], the “mercy” missing from the land in [[Hosea 4:1]], the “goodness” that evaporates like dew in [[Hosea 6:4]], the “mercy” God wants more than sacrifice in [[Hosea 6:6]], and the “mercy” to reap and keep in [[Hosea 10:12]] and [[Hosea 12:6]]. Scripture Helps quotes President Russell M. Nelson: because God has hesed for those who covenant with Him, He keeps working with them and helps them find their way back. Hosea’s whole point fits in one sentence: **Israel’s hesed evaporated like morning dew; God’s never does.**"),
    pull("I will heal their backsliding, I will love them freely", "[[Hosea 14:4]]"),
]

# ---------------------------------------------------------------- 3. BOOK OF MORMON PARALLELS
PARALLELS = [
    lead("Lehi’s family left Jerusalem about 600 BC carrying the brass plates, so the same covenant language that shaped Hosea and Joel runs through the Book of Mormon. Each card below pairs two passages that teach the same doctrine."),
    parallel_cards([
        dict(k_ref="[[Hosea 2:14–20]]",
             k="The Lord woos back His unfaithful bride and betroths her “for ever” in lovingkindness and mercies.",
             b_ref="[[3 Nephi 22:5–8]]",
             b="The risen Christ quotes Isaiah to the Nephites: “thy maker, thy husband, the Lord of Hosts is his name.” He called her “as a woman forsaken,” and “with great mercies will I gather thee.”",
             teaches="The covenant is a love relationship, and the Lord is the faithful partner who takes us back."),
        dict(k_ref="[[Hosea 11:8]]",
             k="“How shall I give thee up, Ephraim?… mine heart is turned within me.” God agonizes over giving up a wayward child.",
             b_ref="[[Jacob 5:41]]",
             b="In Zenos’s allegory, “the Lord of the vineyard wept,” and asked, “What could I have done more for my vineyard?”",
             teaches="God doesn’t give up on His people easily. He grieves, keeps working, and tries again."),
        dict(k_ref="[[Hosea 1:10]]; [[Hosea 2:23|2:23]]",
             k="Those called “not my people” will be called “the sons of the living God.”",
             b_ref="[[Mosiah 5:7]]",
             b="Because of their covenant, King Benjamin’s people “shall be called the children of Christ, his sons, and his daughters.”",
             teaches="Making a covenant gives us a new family name. We become His (this is one of the week’s Scripture Helps questions)."),
        dict(k_ref="[[Hosea 14:1–4]]",
             k="“O Israel, return unto the Lord… I will heal their backsliding.”",
             b_ref="[[3 Nephi 9:13–14]]",
             b="After the destruction, the Savior’s voice asks: “will ye not now return unto me… that I may heal you?” and “mine arm of mercy is extended towards you.”",
             teaches="The invitation to return always comes with a promise to heal, not just to forgive."),
        dict(k_ref="[[Hosea 6:6]]; [[Joel 2:13]]",
             k="Mercy, not sacrifice. Rend your heart, not your garments.",
             b_ref="[[3 Nephi 9:19–20]]",
             b="Animal sacrifices are done away, and the Lord now asks for “a broken heart and a contrite spirit.”",
             teaches="God has always wanted the inside, not just the outward act. Ritual without the heart misses the point."),
        dict(k_ref="[[Hosea 13:6]]; [[Hosea 10:1|10:1]]",
             k="“They were filled, and their heart was exalted; therefore have they forgotten me.” The richer the vine, the more altars to idols.",
             b_ref="[[Helaman 12:2]]",
             b="Mormon: “at the very time when he doth prosper his people… then is the time that they do harden their hearts, and do forget the Lord.”",
             teaches="This is the pride cycle. Prosperity is a test, and gratitude is how we pass it."),
        dict(k_ref="[[Hosea 10:12]]",
             k="“Sow to yourselves in righteousness, reap in mercy.”",
             b_ref="[[Alma 41:14–15]]",
             b="Alma to Corianton: be merciful, and “ye shall have mercy restored unto you again… For that which ye do send out shall return unto you.”",
             teaches="We reap what we sow, and the harvest of showing mercy is receiving it."),
        dict(k_ref="[[Hosea 13:4]]",
             k="“Thou shalt know no god but me: for there is no saviour beside me.”",
             b_ref="[[Mosiah 3:17]]",
             b="The angel to King Benjamin: there is “no other name given nor any other way nor means whereby salvation can come… only in and through the name of Christ.”",
             teaches="Assyria, Egypt, Baal, money: none of them can save. Only Jesus Christ can."),
        dict(k_ref="[[Hosea 13:14]]",
             k="“I will ransom them from the power of the grave… O death, I will be thy plagues; O grave, I will be thy destruction.”",
             b_ref="[[Mosiah 16:7–8]]",
             b="Abinadi: “there is a resurrection, therefore the grave hath no victory, and the sting of death is swallowed up in Christ.”",
             teaches="Hosea’s promise is fulfilled in the Resurrection of Jesus Christ, and it covers everyone."),
        dict(k_ref="[[Joel 2:28–29]]",
             k="The Spirit poured out on all flesh: sons and daughters, old and young, servants and handmaids.",
             b_ref="[[Alma 32:23]]",
             b="God “imparteth his word by angels unto men, yea, not only men but women also… little children do have words given unto them many times.”",
             teaches="Revelation isn’t only for prophets or adults. A 12-year-old can receive it too."),
    ]),
]

# ---------------------------------------------------------------- 4. TIE TO COME, FOLLOW ME
CFM = [
    p("This week’s outline is titled **“I Will Love Them Freely”** (November 16–22; Hosea 1–6; 10–14; Joel). Its introduction says Israel’s covenant with the Lord was so deep that He compared it to a **marriage**: eternal commitment, shared experiences, building a life together, exclusive loyalty, and above all wholehearted love. Israel wasn’t faithful, but the Lord’s message was not “I will reject you forever.” It was “I will invite you back” ([[Hosea 2:14–15]]; [[Hosea 2:19]]; [[Hosea 14:4]]). Joel’s message is the same: the Lord “is gracious and merciful, slow to anger” ([[Joel 2:13]]). The outline invites us to think about how His faithfulness to us inspires us to be faithful to Him, and points to “Hosea, or Hoshea” and “Joel” in the Bible Dictionary."),
    h3("The outline’s principles"),
    points([
        ("“The Lord always invites me to return to Him.” ([[Hosea 1]]–3; [[Hosea 14]])",
         "Gomer’s unfaithfulness is used to show how the Lord feels about His covenant people. Questions: How is making a covenant with the Lord like entering into a marriage? How is failing to keep it like being unfaithful to a spouse ([[Hosea 2:5–7, 13]])? What does [[Hosea 2:14–23]] teach about the Lord’s love and mercy? How do you show Him your love and loyalty? In Hosea 14, look for the promises to those who return. What does “love them freely” mean to you ([[Hosea 14:4]])? What do the plant metaphors in [[Hosea 14:5–8]] teach about the Lord’s blessings, including the blessings of repentance? Suggested hymn: “Come unto Jesus” (*Hymns*, no. 117). Picture: *Gomer Rescued*, by Deb Minnard."),
        ("“Devotion to God must be felt inwardly, not just expressed outwardly.” ([[Hosea 6:4–7]]; [[Joel 2:12–13]])",
         "Israel offered sacrifices while breaking more important commandments. Questions: What does it mean that the Lord “desired mercy, and not sacrifice; and the knowledge of God more than burnt offerings” ([[Hosea 6:6]])? What does it mean for righteousness to be like a cloud or like dew ([[Hosea 6:4]])? What should our righteousness be like ([[Isaiah 48:18]]; [[1 Nephi 2:9–10]])? Read [[Matthew 9:10–13]] and [[Matthew 12:1–8]] to see how the Savior used Hosea 6:6. Tearing your clothes was an outward sign of mourning, so how is rending your heart different?"),
        ("“I will pour out my spirit upon all flesh.” ([[Joel 2]]). This principle carries the seminary icon.",
         "Questions: What similarities do you see between our day and the day Joel foresaw ([[Joel 2:1–2, 11, 18–32]])? What impresses you about the blessings in verses 18–32, and why might they be especially valuable today? What did Moroni say about Joel 2 in 1823 ([[Joseph Smith—History 1:41]])? How are [[Joel 2:28–32]] being fulfilled today (see also [[Acts 2:1–21]])? What does it mean that the Lord would pour out His Spirit “upon all flesh”? The outline quotes President Russell M. Nelson, who taught that in coming days we won’t survive spiritually without the constant influence of the Holy Ghost (“Revelation for the Church, Revelation for Our Lives,” April 2018). It lists people who received an outpouring of the Spirit and asks what they did: [[Mosiah 4:1–3, 19–20]]; [[Mosiah 18:7–11]]; [[Helaman 6:34–36]]; [[Doctrine and Covenants 19:37–41]]. It also quotes Elder David A. Bednar (an evening with a General Authority, Feb. 7, 2020): we often treat revelation as rare when it is meant to be constant, and it usually comes “still and small and incremental over time.” See also Gary E. Stevenson, “Promptings of the Spirit” (October 2023), and the video “Enemy Territory.”"),
    ]),
    p("**Teaching tip in the outline:** “Create a spiritual environment.” Ask what helps and what hurts the feeling in your classroom, and how to invite the Spirit there (*Teaching in the Savior’s Way*, 7)."),
    p("**From the children’s section** (it adapts well for this age): “I can faithfully keep my covenants” ([[Hosea 2:19–20]]); “It is time to seek the Lord” ([[Hosea 10:12]]), with a clock activity and the song “Anytime, Anywhere” (*Hymns for Home and Church*); “Jesus Christ is my Savior and Redeemer” ([[Hosea 13:4, 14]]), finding Him in the Guide to the Scriptures; and “The Holy Ghost can guide me” ([[Joel 2:28–29]]), pouring water versus a drip, with [[John 14:16]], [[Moroni 10:5]], and [[Doctrine and Covenants 42:17]]."),
    h3("Scripture Helps questions this week"),
    helps([
        ("Who were the “minor prophets”? (shown on the weekly outline)", "the last 12 Old Testament books, called “minor” because they are shorter, not less important. Hosea preached to the north in the mid-700s BC, and Joel’s date is uncertain. See Section 1"),
        ("What does it mean that the children of Israel will be called the sons and daughters of God? (shown on the weekly outline)", "see the Mosiah 5:7 card in Section 3"),
        ("What do we know about the Lord’s command for Hosea to marry “a wife of whoredoms”?", "literal or symbolic is debated; see the honest note in Section 1 and the hard questions in Section 2"),
        ("What is significant about the names of Hosea and Gomer’s children?", "see Section 2, steps 1 and 3"),
        ("Why did the Lord say Israel would call Him “Ishi” rather than “Baali”?", "both can mean “husband,” but Baali echoes the false god Baal. See Section 2, step 3"),
        ("What does it mean that Israel would be betrothed to the Lord forever?", "betrothal was legally binding, and the Lord promises an eternal covenant. See the hesed card in Section 2"),
        ("Why did the Lord desire “mercy, and not sacrifice”?", "see Section 2, step 6, and Section 5"),
        ("Why did Joel exhort the people to rend their hearts instead of their garments?", "see Section 2, step 11"),
        ("What does it mean that the Lord will “pour out [His] spirit upon all flesh”?", "see the hard questions in Section 2 and the timeline below"),
    ]),
    p("**Scripture Helps “Learn More”:** Patrick Kearon, “God’s Intent Is to Bring You Home” (April 2024); Russell M. Nelson, “Revelation for the Church, Revelation for Our Lives” (April 2018). **Music:** “Come unto Jesus” (*Hymns*, no. 117) and “The Spirit of God” (*Hymns*, no. 2). Scripture Helps also quotes President Henry B. Eyring calling Hosea “a love story, … a story of a marriage covenant bound by love, by steadfast love,” and President Gordon B. Hinckley on the “cascade of enlightenment” poured out since the First Vision as a fulfillment of Joel."),
    card("Latter-day connections",
         "**[[Joseph Smith—History 1:41]]:** on September 21, 1823, Moroni quoted [[Joel 2:28–32]] to 17-year-old Joseph Smith and said it “was not yet fulfilled, but was soon to be.”",
         "**[[Doctrine and Covenants 109:36–37]]:** at the Kirtland Temple dedication (March 27, 1836), the prayer asked that it be “fulfilled upon them, as upon those on the day of Pentecost,” with the gift of tongues “poured out” and the house filled “as with a rushing mighty wind.” Joel’s solemn assembly at the house of the Lord ([[Joel 1:14]]; [[Joel 2:15–16]]) has a latter-day echo too: the Lord commanded the Saints to “call a solemn assembly” ([[Doctrine and Covenants 88:70]]; [[Doctrine and Covenants 109:6]]).",
         "**Signs of the Second Coming:** Joel’s sun turned to darkness and moon into blood ([[Joel 2:31]]) is repeated in modern revelation ([[Doctrine and Covenants 29:14]]; [[Doctrine and Covenants 45:42]]). Joel’s “The Lord also shall roar out of Zion” ([[Joel 3:16]]) echoes in [[Doctrine and Covenants 133:21]].",
         "**Temple covenants:** Hosea’s picture of a covenant as a marriage “for ever” ([[Hosea 2:19]]) is part of why the house of the Lord, where covenants and eternal marriages are made, matters so much. The Bible Dictionary sums up Hosea’s “fundamental idea” as “the love of God for His people.”"),
    h3("Joel’s promise in the Restoration"),
    resto([
        ("c. AD 30s", "Pentecost", "Peter: “this is that which was spoken by the prophet Joel” ([[Acts 2:16–21]])."),
        ("1823", "Moroni’s visit", "Joel 2:28–32 “was not yet fulfilled, but was soon to be” ([[Joseph Smith—History 1:41]])."),
        ("1836", "Kirtland Temple", "The dedication prayer asks for a Pentecost-like outpouring on the Saints ([[Doctrine and Covenants 109:36–37]])."),
        ("Today", "Your sons and your daughters", "Personal revelation for every covenant member: the Spirit “upon all flesh” ([[Joel 2:28]])."),
    ]),
    h3("Teaching ideas for ages 12–13"),
    ideas([
        ("Erase the “Lo-.”", "Write the children’s names on the board: LO-RUHAMAH (“not pitied”) and LO-AMMI (“not my people”). Ask what it would feel like to carry those names. Read [[Hosea 2:1]] and [[Hosea 2:23]], then let a student erase “LO-” from each name. Ask: What labels do people think God has given up on? What new name does the Lord give us when we make covenants ([[Mosiah 5:7]])?"),
        ("Morning dew.", "Before class, mist a dark plate or mirror with a spray bottle and set it in a warm or sunny spot. Read [[Hosea 6:4]] and check the plate: the dew is fading. Compare Lehi’s wish for his son to be like a river and a valley, “firm and steadfast” ([[1 Nephi 2:9–10]]). In small groups, list habits that keep Sunday-morning goodness from evaporating by Monday."),
        ("Rend your heart, not your clothes.", "Give each student a paper cut-out shirt. Explain that tearing your clothes was the ancient way to show sorrow ([[Joel 2:12–13]]). Have students write one outward thing people do to look religious on the shirt, and one inward thing God actually wants on the back. Then read [[Matthew 9:10–13]]: what did Jesus mean by “I will have mercy, and not sacrifice”?"),
        ("Pour versus drip.", "Pour a pitcher of water into a bowl, then use an eyedropper. Read [[Joel 2:28–29]]. Share Elder Bednar’s point that the Spirit usually comes “still and small and incremental over time.” Assign small groups [[Mosiah 4:1–3]], [[Mosiah 18:7–11]], [[Helaman 6:34–36]], and [[Doctrine and Covenants 19:37–41]], and have them report what those people did before the Spirit was poured out on them."),
        ("Grow like a lily.", "Split [[Hosea 14:5–8]] and [[Hosea 10:12]] among groups. Each group sketches one image: dew, lily, roots, olive tree, vine, fir tree, or a plowed field. Then they write one sentence on what it teaches about the blessings of repentance. Sing or play “Come unto Jesus” (*Hymns*, no. 117) as they finish."),
        ("“It is time to seek the Lord.”", "Draw a clock on the board ([[Hosea 10:12]]). Students suggest ways to seek the Lord at different times of day: a morning prayer, a verse at lunch, a hymn on the bus, a quiet thank-you at night. **Invitation:** each student picks one specific time and one way, writes it on a sticky note for their phone or mirror, and seeks the Lord at that time every day this week. Report next Sunday on what they noticed."),
    ]),
]

# ---------------------------------------------------------------- 5. TIE TO JESUS CHRIST
CHRIST = [
    christ([
        ("[[Hosea 2:19–20]] · [[Matthew 9:15]]",
         "He is the faithful Bridegroom",
         "The Lord of the Old Testament calls Himself Israel’s husband. In the New Testament, Jesus calls Himself “the bridegroom” ([[Matthew 9:15]]). The covenant Hosea describes, in righteousness, lovingkindness, mercies, and faithfulness, is the covenant Jesus Christ keeps with us. He is never the unfaithful one."),
        ("[[Hosea 3:1–2]] · [[1 Peter 1:18–19]]",
         "He buys us back (a type)",
         "Hosea paid a price to bring home a wife who had sold herself away. That makes him a **type**, or foreshadowing, of the Redeemer. “Redeem” literally means to buy back. Peter says we were redeemed “not… with corruptible things, as silver and gold… But with the precious blood of Christ.” Hosea paid in silver and barley, and Jesus paid with His own life."),
        ("[[Hosea 11:1]] · [[Matthew 2:15]]",
         "“Out of Egypt have I called my son”",
         "Hosea was remembering the Exodus, when God called His “son” Israel out of slavery. Matthew saw the same words fulfilled when the child Jesus came back from Egypt. In Matthew’s telling, Jesus relives Israel’s story and does it faithfully: where Israel failed, the Son kept every promise."),
        ("[[Hosea 6:1–2]] · [[Luke 24:46]]",
         "“In the third day he will raise us up”",
         "In context, these verses are Israel’s hope that God would revive the nation. Many Christians since early times have also read them as a foreshadowing of Christ, who rose “the third day.” Treat this as an **interpretation**, not something the text spells out. Either way, the promise that God heals and raises what has been torn down is fulfilled in Him."),
        ("[[Hosea 13:14]] · [[1 Corinthians 15:54–55]]",
         "He swallows up death",
         "Paul builds his great Resurrection chapter on Hosea’s words: “O death, where is thy sting? O grave, where is thy victory?” Abinadi taught the same truth: “the sting of death is swallowed up in Christ” ([[Mosiah 16:8]]). Because Jesus rose, “there is no saviour beside me” ([[Hosea 13:4]]) is good news, not a threat."),
        ("[[Joel 2:28–32]] · [[Acts 2:32–33]]; [[Romans 10:13]]",
         "He pours out the Spirit",
         "At Pentecost, Peter explained that the risen Jesus, “having received of the Father the promise of the Holy Ghost, he hath shed forth this, which ye now see and hear.” Paul applies Joel’s “whosoever shall call on the name of the Lord” to calling on Jesus. The outpouring Joel saw comes through Christ, and it reaches every sincere seeker, sons and daughters alike."),
    ]),
]

LESSON = dict(
    year=2026, week=47, volume="Old Testament", slug="hosea-joel",
    dates="November 16–22", start="2026-11-16",
    scripture_block="Hosea 1–6; 10–14; Joel",
    outline_title="I Will Love Them Freely",
    title="Hosea & Joel — I Will Love Them Freely — Lesson Handout",
    week_hub="lessons/2026 - Old Testament/November/november-16-22-hosea-1-6-10-14-joel",
    palette_note="dawn over the valley of Achor and dew on the lily (Hosea 2:15; 14:5): pre-dawn plum, dawn rose, morning gold, olive green",
    tokens={
        "night": "#2b1f3a", "night-2": "#1b1326",
        "accent": "#d65a78", "accent-soft": "#f4a0b2",
        "gold": "#f2c46d", "gold-soft": "#fbf0d9",
        "parch": "#f8f4f1", "parch-2": "#f3ecef",
        "ink": "#2a2430", "ink-soft": "#5c5363",
        "echo": "#3f7d6e", "echo-soft": "#e3efe9",
        "line": "#e0d3da",
    },
    hero=dict(
        h1="Hosea & Joel",
        kicker="A Broken Covenant · A Door of Hope · Locusts · The Spirit Poured Out",
        hook="A prophet whose own marriage became the sermon, and a God who keeps calling His people home: “I will heal their backsliding, I will love them freely.”",
        svg=HERO_SVG,
    ),
    band=dict(label="Israel’s last decades", events=[
        ("c. 841 BC", "Jehu’s coup at Jezreel (Hosea 1:4)"),
        ("c. 786–746 BC", "Jeroboam II; Hosea begins (1:1)"),
        ("745 BC", "Tiglath-pileser III rules Assyria"),
        ("c. 732 BC", "Hoshea, Israel’s last king"),
        ("722/721 BC", "Samaria falls; Israel exiled"),
    ]),
    sections=[HISTORY, SUMMARY, PARALLELS, CFM, CHRIST],
    sources=("Come, Follow Me—For Home and Church: Old Testament 2026, Nov. 16–22; Scripture Helps: Old Testament, "
             "“Hosea 1–6; 10–14; Joel”; Bible Dictionary, “Hosea, or Hoshea” and “Joel”; King James Version, Book of Mormon, "
             "Doctrine and Covenants, and Pearl of Great Price (brief quotations); encyclopedia articles on the Black Obelisk of "
             "Shalmaneser III, the Samaria Ostraca, Kuntillet ʿAjrud, Jeroboam II, Hoshea, Sargon II, and the Book of Joel; "
             "Rebecca Denova, “Hosea,” World History Encyclopedia; Biblical Archaeology Society on Samaria’s personal names; "
             "John D. Whiting, “Jerusalem’s Locust Plague,” National Geographic, Dec. 1915."),
)
