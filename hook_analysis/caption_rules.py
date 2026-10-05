"""First-pass rules for videos with no transcript: classify the caption (Description) opening.
Order follows the tie-break rules in tiktok_hook_types.md."""
import re
R = [
 ("S", r"\d+ ?(x|%)|\d+%|sold out|reviews?|\b\d{2,}[,k]? (people|moms|parents|sold)|everyone|viral|went from|results?|lost \d|tiktok made me|best.?seller|#1|rated|\bdentist[- ]approved|recommended by"),
 ("O", r"\bdeals?\b|\bsale\b|% ?off|\boff\b|coupon|discount|limited|ends? (today|tonight|soon)|hurry|flash|last (chance|day)|free (ship|gift)|almost gone|price (drop|cut)|going fast|sell(ing)? out|don'?t miss|clearance|\$\d|bogo|promo|oferta|descuento|rebaja"),
 ("P", r"tired of|sick of|struggl|\bhate|battle|fight|cavit|meltdown|tears|refus|chore|nightmare|stress|lazy|plaque|yellow|bad breath|gingivitis|frustrat|wrestl|bedtime (is|was)|pulling teeth|without me demanding|biggest fight|your breath stinks|nightly negotiation|sufre|odia|batall|cansad|llor"),
 ("C", r"secret|nobody|you won'?t believe|wait (for|till|until)|here'?s (why|what)|the reason|you (need|have) to see|trust me|found out|what happens|didn'?t know|if you know|this is why|plot twist|wish i (found|knew)|what did i find|you'?ll never guess"),
 ("B", r"stop |don'?t buy|scam|wrong|worst|never |always |game.?chang|life.?chang|obsessed|forget |throw away|ditch|better than|only toothbrush|best |insane|crazy|unreal|obsessed|cheating|too good|illegal|banned"),
 ("Q", r"\?|^(do|does|did|why|how|what|who|is|are|have|has|can|would|should|want|ever|anyone|quieres|tienes|sabías|por qu)\b"),
 ("V", r"^(i|my|we|our|so|me|pov|storytime|when i|mi|yo|nos|ayer)\b|\bpov\b|storytime|my (son|daughter|kid|toddler|baby|husband|wife)|honest(ly)? (opinion|review)"),
]
BOILER = re.compile(r"(prices?, discounts?.*|final price.*|disclaimer.*|los precios.*|this video was partially.*)$", re.I)

def clean(d):
    """Caption minus hashtags/mentions/disclaimers."""
    d = re.sub(r"https?://\S+|www\.\S+|#\S+|@\S+", " ", d)
    return " ".join(BOILER.sub(" ", d).split())

def classify(c):
    t = clean(c).lower()
    for code, pat in R:
        if re.search(pat, t): return code
    return "X"
