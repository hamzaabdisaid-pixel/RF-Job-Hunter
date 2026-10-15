#!/usr/bin/env python3
"""Discover publicly indexed RF job announcements from Google News RSS.
No scraping or authentication of LinkedIn/Apec/Hellowork/Indeed.
Results are candidate links, not verified live vacancies.
"""
import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SITES={"LinkedIn":"linkedin.com/jobs/view","Apec":"apec.fr","Hellowork":"hellowork.com/fr-fr/emplois","Indeed":"fr.indeed.com/viewjob"}
KEYWORDS=['"ingénieur RF"','"ingénieur radiofréquence"','"ingénieur hyperfréquence"','"ingénieur antennes"','"ingénieur CEM"','"RF test engineer"','"microwave engineer"']
BLOCK=re.compile(r"\b(défense|defense|militaire|military|armement|missile|radar militaire|naval group|thales dms|mbda|dassault aviation)\b",re.I)
RELEVANT=re.compile(r"\b(rf|radiofréquence|radiofrequence|hyperfréquence|hyperfrequence|microwave|antenne|cem|électromagnétique|electromagnetique)\b",re.I)
YEAR=re.compile(r"(\d+)\s*(?:à|a|[-–])\s*(\d+)\s*ans|(?:minimum|mini|au moins)\s*(\d+)\s*ans",re.I)
OUT=Path("data/jobs.json")
def load():
    try:return json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError,ValueError):return {"jobs":[]}
def fetch(q):
    url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":q+" when:14d","hl":"fr","gl":"FR","ceid":"FR:fr"})
    req=urllib.request.Request(url,headers={"User-Agent":"RFJobHunter/1.0"})
    with urllib.request.urlopen(req,timeout=15) as response:return ET.fromstring(response.read())
def main():
    existing=load().get("jobs",[])
    seen={x["id"] for x in existing if "id" in x}
    fresh=[]
    for site,domain in SITES.items():
        for keyword in KEYWORDS:
            try:root=fetch(keyword+" site:"+domain)
            except Exception as exc:
                print("Source temporarily unavailable:",site,type(exc).__name__)
                continue
            for item in root.findall(".//item"):
                title=(item.findtext("title") or "").strip()
                link=(item.findtext("link") or "").strip()
                desc=re.sub("<[^>]*>"," ",item.findtext("description") or "")
                body=title+" "+desc
                if not RELEVANT.search(body) or BLOCK.search(body) or not link:continue
                uid=urllib.parse.quote(title.casefold()+"|"+site,safe="")[:350]
                if uid in seen:continue
                seen.add(uid)
                m=YEAR.search(body)
                years=int(m.group(1) or m.group(3)) if m else None
                if years is not None and (years<1 or years>3):group="other"
                elif years is None:group="unknown"
                else:group="priority"
                fresh.append({"id":uid,"title":title,"company":"À confirmer","city":"France — ville à confirmer","source":site,"url":link,"published":item.findtext("pubDate") or "Date non disponible","experience":(m.group(0) if m else "Non précisée"),"group":group,"review":"À vérifier : secteur civil et annonce active","discovered_at":datetime.now(timezone.utc).isoformat()})
    merged=(fresh+existing)[:400]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"updated_at":datetime.now(timezone.utc).isoformat(),"jobs":merged},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"New indexed candidate results: {len(fresh)}; stored: {len(merged)}")
if __name__=="__main__":main()
