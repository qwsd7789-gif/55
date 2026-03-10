import requests,itertools
base='https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/aweme/'
params_keys=['board_type','type','hotword_type','detail_list']
vals=['0','1','2','3','4','5','6','7','8','9']
for k in params_keys:
    for v in vals:
        try:
            r=requests.get(base,params={k:v},timeout=12,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.douyin.com/hot'})
            j=r.json()
            n=len(j.get('aweme_list',[]) or []) if isinstance(j,dict) else -1
            if n>0:
                print('HIT',k,v,n)
                print(str(j)[:300])
                raise SystemExit
        except Exception:
            pass
print('no hit')
