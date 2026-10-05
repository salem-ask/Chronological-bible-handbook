"""Chronological reading order used for the 365-day plan.

Each period is (period title, [readings]). A reading is (book, first, last)
for a run of chapters, or ("Psalms", [list]) for psalms read out of order.

Principles (also explained in the plan's introduction):
- Narrative books give the backbone; parallel accounts (Samuel/Kings and
  Chronicles) are read side by side.
- Prophets are placed with the reigns or events named in their opening
  verses, following the approximate dates used in the Handbook's timeline.
- Psalms whose titles name an event in David's life are read with that event.
  Psalms that clearly refer to the destruction of Jerusalem or the return from
  exile are read in those periods. The remaining psalms are read in Bible
  order during the time of David and Solomon.
- The Gospels are read side by side, period by period.
- Paul's letters are read at the points in Acts where they were most probably
  written. Several placements (Job, some psalms, James, Galatians, Hebrews)
  are debated; dates are approximate.
"""

# Psalms read at a specific point in the story
PLACED_PSALMS = {90, 59, 56, 34, 52, 142, 57, 54, 96, 105, 106, 60, 51, 3, 18,
                 72, 127, 74, 79, 137, 126}


def psalms(first, last):
    return ("Psalms", [n for n in range(first, last + 1) if n not in PLACED_PSALMS])


ORDER = [
    ("Creation and the early world", [
        ("Genesis", 1, 11),
    ]),
    ("The time of the patriarchs", [
        ("Job", 1, 42),
        ("Genesis", 12, 50),
    ]),
    ("The Exodus and the wilderness", [
        ("Exodus", 1, 40),
        ("Leviticus", 1, 27),
        ("Numbers", 1, 36),
        ("Deuteronomy", 1, 34),
        ("Psalms", [90]),                       # "A Prayer of Moses"
    ]),
    ("The conquest and the Judges", [
        ("Joshua", 1, 24),
        ("Judges", 1, 21),
        ("Ruth", 1, 4),
    ]),
    ("Samuel, Saul and David", [
        ("1 Samuel", 1, 19), ("Psalms", [59]),  # 1 Sam 19:11
        ("1 Samuel", 20, 21), ("Psalms", [56, 34]),  # 1 Sam 21:10-15
        ("1 Samuel", 22, 22), ("Psalms", [52, 142, 57]),  # Doeg; the cave
        ("1 Samuel", 23, 23), ("Psalms", [54]),  # the Ziphites
        ("1 Samuel", 24, 31),
        ("1 Chronicles", 1, 10),
    ]),
    ("The reign of David", [
        ("2 Samuel", 1, 5),
        ("1 Chronicles", 11, 12),
        ("2 Samuel", 6, 6),
        ("1 Chronicles", 13, 16), ("Psalms", [96, 105, 106]),  # sung in 1 Chr 16
        ("2 Samuel", 7, 7),
        ("1 Chronicles", 17, 17),
        psalms(1, 41),
        ("2 Samuel", 8, 9),
        ("1 Chronicles", 18, 18), ("Psalms", [60]),  # 2 Sam 8:13
        ("2 Samuel", 10, 10),
        ("1 Chronicles", 19, 19),
        ("2 Samuel", 11, 12),
        ("1 Chronicles", 20, 20), ("Psalms", [51]),  # after Nathan's visit
        psalms(42, 71),
        ("2 Samuel", 13, 15), ("Psalms", [3]),   # fleeing from Absalom
        ("2 Samuel", 16, 22), ("Psalms", [18]),  # 2 Sam 22 = Psalm 18
        ("2 Samuel", 23, 24),
        ("1 Chronicles", 21, 25),
        psalms(73, 89),                          # Asaph, Korah, Heman, Ethan
        ("1 Chronicles", 26, 29),
        psalms(91, 150),
    ]),
    ("The reign of Solomon", [
        ("1 Kings", 1, 2), ("Psalms", [72]),     # "A Psalm for Solomon"
        ("1 Kings", 3, 4),
        ("2 Chronicles", 1, 1),
        ("Proverbs", 1, 31),
        ("Song of Solomon", 1, 8),
        ("1 Kings", 5, 8),
        ("2 Chronicles", 2, 7), ("Psalms", [127]),  # "A Song of degrees for Solomon"
        ("1 Kings", 9, 11),
        ("2 Chronicles", 8, 9),
        ("Ecclesiastes", 1, 12),
    ]),
    ("The divided kingdom", [
        ("1 Kings", 12, 14),
        ("2 Chronicles", 10, 12),
        ("1 Kings", 15, 16),
        ("2 Chronicles", 13, 16),
        ("1 Kings", 17, 22),
        ("2 Chronicles", 17, 20),
        ("2 Kings", 1, 8),
        ("2 Chronicles", 21, 21),
        ("Obadiah", 1, 1),
        ("2 Kings", 9, 11),
        ("2 Chronicles", 22, 23),
        ("2 Kings", 12, 12),
        ("2 Chronicles", 24, 24),
        ("Joel", 1, 3),
        ("2 Kings", 13, 14),
        ("2 Chronicles", 25, 25),
        ("Jonah", 1, 4),                         # 2 Kings 14:25
        ("2 Chronicles", 26, 26),
        ("Amos", 1, 9),
        ("Hosea", 1, 14),
        ("2 Kings", 15, 16),
        ("2 Chronicles", 27, 28),
        ("Micah", 1, 7),
        ("2 Kings", 17, 17),                     # fall of Samaria
    ]),
    ("Judah alone", [
        ("2 Kings", 18, 20),
        ("2 Chronicles", 29, 32),
        ("Isaiah", 1, 66),
        ("2 Kings", 21, 21),
        ("2 Chronicles", 33, 33),
        ("Nahum", 1, 3),
        ("2 Kings", 22, 23),
        ("2 Chronicles", 34, 35),
        ("Zephaniah", 1, 3),
        ("Habakkuk", 1, 3),
        ("Jeremiah", 1, 29),
        ("2 Kings", 24, 24),
        ("Ezekiel", 1, 24),
        ("Jeremiah", 30, 39),
    ]),
    ("The fall of Jerusalem and the exile", [
        ("2 Kings", 25, 25),
        ("2 Chronicles", 36, 36),
        ("Jeremiah", 40, 52),
        ("Lamentations", 1, 5),
        ("Psalms", [74, 79, 137]),
        ("Ezekiel", 25, 48),
        ("Daniel", 1, 12),
    ]),
    ("The return from exile", [
        ("Ezra", 1, 6), ("Psalms", [126]),
        ("Haggai", 1, 2),
        ("Zechariah", 1, 14),
        ("Esther", 1, 10),
        ("Ezra", 7, 10),
        ("Nehemiah", 1, 13),
        ("Malachi", 1, 4),
    ]),
    ("The birth and early years of Jesus", [
        ("Luke", 1, 1), ("Matthew", 1, 1), ("Luke", 2, 2), ("Matthew", 2, 2),
        ("John", 1, 1),
    ]),
    ("The ministry of Jesus", [
        ("Mark", 1, 1), ("Matthew", 3, 4), ("Luke", 3, 4), ("John", 2, 4),
        ("Mark", 2, 6), ("Matthew", 5, 14), ("Luke", 5, 9), ("John", 5, 6),
        ("Mark", 7, 10), ("Matthew", 15, 20), ("Luke", 10, 19), ("John", 7, 11),
    ]),
    ("The last week, the cross and the resurrection", [
        ("Mark", 11, 13), ("Matthew", 21, 25), ("Luke", 20, 21), ("John", 12, 12),
        ("Mark", 14, 15), ("Matthew", 26, 27), ("Luke", 22, 23), ("John", 13, 19),
        ("Mark", 16, 16), ("Matthew", 28, 28), ("Luke", 24, 24), ("John", 20, 21),
    ]),
    ("The early Church", [
        ("Acts", 1, 12),
        ("James", 1, 5),
    ]),
    ("Paul's journeys and letters", [
        ("Acts", 13, 14),
        ("Galatians", 1, 6),
        ("Acts", 15, 18),
        ("1 Thessalonians", 1, 5),
        ("2 Thessalonians", 1, 3),
        ("Acts", 19, 19),
        ("1 Corinthians", 1, 16),
        ("Acts", 20, 20),
        ("2 Corinthians", 1, 13),
        ("Romans", 1, 16),
        ("Acts", 21, 28),
        ("Ephesians", 1, 6),
        ("Philippians", 1, 4),
        ("Colossians", 1, 4),
        ("Philemon", 1, 1),
    ]),
    ("The last letters and Revelation", [
        ("1 Timothy", 1, 6),
        ("Titus", 1, 3),
        ("1 Peter", 1, 5),
        ("2 Timothy", 1, 4),
        ("2 Peter", 1, 3),
        ("Hebrews", 1, 13),
        ("Jude", 1, 1),
        ("1 John", 1, 5),
        ("2 John", 1, 1),
        ("3 John", 1, 1),
        ("Revelation", 1, 22),
    ]),
]
