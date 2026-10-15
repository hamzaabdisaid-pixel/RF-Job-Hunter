import os,json,re,urllib.request,urllib.parse,datetime,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/"jobs.json"
KEY=os.getenv("ADZUNA_APP_KEY")
ID=os.getenv("ADZUNA_APP_ID")
if not KEY or not ID:
    raise SystemExit("ADZUNA_APP_ID and ADZUNA_APP_KEY are required; existing data preserved.")
terms=["ingénieur radiofréquence","ingénieur RF","ingénieur hyperfréquence","ingénieur test RF","ingénieur antennes","ingénieur CEM","ingénieur télécommunications RF"]
defense=re.compile(r"\b(défense|defense|militaire|armement|missile|radar militaire|naval group|dga|armée|armee|thales six|mbda|safran electronics & defense)\b",re.I)
def years(text):
    t=text.lower()
    m=re.search(r"(\d+)\s*(?:à|a|[-–])\s*(\d+)\s*ans",t)
    if m:return int(m.group(1))
    m=re.search(r"(?:minimum|min\.?|au moins|dès|de)\s*(\d+)\s*ans",t)
    if m:return int(m.group(1))
    m=re.search(r"(\d+)\s*ans?\s*(?:d.experience|d.expérience|minimum)",t)
    if m:return int(m.group(1))
    return None
found={}
for term in terms:
    query=urllib.parse.urlencode({"app_id":ID,"app_key":KEY,"what":term,"results_per_page":50,"sort_by":"date","content-type":"application/json"})
    url="https://api.adzuna.com/v1/api/jobs/fr/search/1?"+query
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"RFJobHunter/1.0"})
        with urllib.request.urlopen(req,timeout=30) as response:data=json.load(response)
    except Exception as e:
        print("Source unavailable:",term,str(e))
        continue
    for item in data.get("results",[]):
        title=item.get("title","")
        description=item.get("description","")
        company=(item.get("company") or {}).get("display_name","")
        content=" ".join([title,description,company])
        if defense.search(content):continue
        link=item.get("redirect_url")
        if not link:continue
        jid=str(item.get("id") or link)
        found[jid]={"id":jid,"title":title,"company":company,"city":(item.get("location") or {}).get("display_name","France"),"description":description[:1200],"experience_years":years(content),"posted":item.get("created",""),"source":"Adzuna (agrégateur)","url":link,"review":"Le caractère civil et les exigences d'expérience doivent être vérifiés dans l'annonce originale."}
if not found:
    raise SystemExit("No new data returned; existing data preserved.")
previous={}
if OUT.exists():
    try:previous={j["id"]:j for j in json.loads(OUT.read_text()).get("jobs",[])}
    except (ValueError,KeyError):pass
new_ids=set(found)-set(previous)
ordered=sorted(found.values(),key=lambda j:j.get("posted",""),reverse=True)
OUT.write_text(json.dumps({"updated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source":"Adzuna API — not direct LinkedIn/Apec/Hellowork/Indeed access","new_count":len(new_ids),"jobs":ordered},ensure_ascii=False,indent=2)+"\n")
print(f"Collected {len(ordered)} real listings; {len(new_ids)} new.")
