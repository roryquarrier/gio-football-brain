import json,base64,os,time,urllib.request,sys
from concurrent.futures import ThreadPoolExecutor
KEY=[l.split("=",1)[1].strip() for l in open(os.path.expanduser("~/.hermes/.env")) if l.startswith("OPENAI_API_KEY=")][0]
STYLE=" Style: polished modern flat-vector illustration with bold shapes, rich green pitch, warm floodlight glow, clean and sharp, NO text, NO letters, NO numbers, NO logos anywhere in the image."
P={
"hero":"Wide cinematic illustration of a football stadium at dusk, floodlights on, a lone football resting on the centre spot of a perfect striped pitch, a glowing tactical-board pattern of arrows and dots faintly drawn over the grass, sense of anticipation.",
"offside":"Top-down tactical diagram on a striped football pitch: a straight bright yellow line across the pitch at the position of the second-last defender (blue team), one red attacker standing slightly beyond the line, another red attacker level with the line, a passer in red with the ball further back, dotted arrow showing the pass. Clear and diagrammatic, like a coach's whiteboard.",
"formations":"Top-down tactics-board view of HALF a football pitch with the goal at the bottom. Exactly ELEVEN red dots in a 4-3-3 formation: 1 goalkeeper dot in the goal, a row of exactly 4 defenders, a row of exactly 3 midfielders, a row of exactly 3 forwards (one centre, two wide). Thin white lines connect each row. Only red dots, no opponents. Count carefully: 1-4-3-3.",
"press":"Dynamic illustration of a football high press: a group of red players swarming a blue defender who has the ball near his own penalty area, red players cutting off passing lanes shown as glowing dashed lines, blue goalkeeper looking worried, tension and speed.",
"xg":"Top-down view of a football penalty area with a heat-map of shot quality: bright red hot zone right in front of goal fading to cool blue far from goal and at tight angles, several shot dots of different sizes scattered, analytical data-visualisation look but no text.",
"korea":"Joyful crowd of football fans in a stadium wearing red shirts and waving red scarves and flags, night, confetti, a sea of red, a young Asian boy in a red shirt on a dad's shoulders cheering, vibrant celebration.",
"final":"Heroic illustration of a golden football trophy on a pitch at sunrise, beams of light, a clipboard with a tactics board resting beside it, confetti, feeling of mastery and victory.",
"quiz-offside":"Top-down football pitch diagram, snapshot of the moment a pass is played: blue defenders in a line with the last defender's line drawn in yellow, the goalkeeper in the goal, a red attacker clearly BEHIND the yellow line (closer to the halfway line) running forward, another red attacker clearly beyond the line. Mark attackers with different bright glowing rings: one ring white, one ring orange. Coach's whiteboard look.",
"quiz-shots":"Top-down view of a football penalty area with three distinct shots marked as glowing dots and arrows toward goal: one shot from very close in the middle (big gold dot), one from the edge of the box (medium silver dot), one from a very tight angle near the byline (small bronze dot). Dot sizes clearly different. Clean diagram.",
"quiz-shape":"Top-down tactics-board view of HALF a football pitch with the goal at the bottom. Exactly ELEVEN red dots in a 3-5-2 formation: 1 goalkeeper dot in the goal, a row of exactly 3 centre-backs, a row of exactly 5 midfield dots where the two outermost dots are very wide on the touchlines (wing-backs) and 3 in the centre, then a row of exactly 2 strikers. Thin white lines connect the rows. Only red dots. Count carefully: 1-3-5-2.",
}
def gen(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","prompt":P[k]+STYLE,"size":"1536x1024","quality":"high","n":1}).encode()
    for a in range(2):
        try:
            req=urllib.request.Request("https://api.openai.com/v1/images/generations",data=body,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
            r=json.load(urllib.request.urlopen(req,timeout=290))
            open(f"assets/raw/{k}.png","wb").write(base64.b64decode(r["data"][0]["b64_json"]))
            return k,"OK"
        except urllib.error.HTTPError as e:
            msg=e.read()[:200]
            if e.code==429: return k,"429 STOP "+str(msg)
            last=f"HTTP {e.code} {msg}"
        except Exception as e: last=str(e)[:150]
    return k,"FAIL "+last
keys=sys.argv[1:] or list(P)
with ThreadPoolExecutor(4) as ex:
    for k,s in ex.map(gen,keys): print(k,s,flush=True)
