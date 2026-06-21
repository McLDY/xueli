#!/usr/bin/env python3
"""Compile data.json + dynamics.json → obfuscated-HTMReady index.html"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEPLOY = os.path.join(ROOT, '_deploy')

C = {
    'header':'a','logo':'b','nav':'c','hero':'d','card':'e','stats':'f',
    'stat':'g','tl-wrap':'h','tl-col':'i','tl-list':'j','tl-node':'k',
    'tl-date':'l','tl-box':'m','tl-empty':'n','footer':'o',
    'mob-tl':'p','mob-tl-item':'q','mob-tl-date':'r','mob-tl-box':'s',
    'mob-tl-empty':'t','fans-bar':'u','bottom-nav':'v','section':'w',
    'search':'x','icon':'y','title':'z','subtitle':'A','btn':'B',
    'desktop-layout':'C','mobile-layout':'D','stat-label':'E',
}

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def cl(s):
    return C.get(s, s)

def dyn_html(items, mob):
    if not items:
        return f'<div class="{cl("mob-tl-empty") if mob else cl("tl-empty")}">\u6682\u65e0\u52a8\u6001</div>'
    nc = cl('mob-tl-item') if mob else cl('tl-node')
    dc = cl('mob-tl-date') if mob else cl('tl-date')
    bc = cl('mob-tl-box') if mob else cl('tl-box')
    ps = []
    for it in items:
        t = it.get('content', '')
        v = it.get('video', {})
        if v and v.get('title'):
            t += '<br>\u25b6\ufe0f <b>' + esc(v['title']) + '</b>'
            if v.get('bvid'):
                t += '<br><a href="https://www.bilibili.com/video/' + esc(v['bvid']) + '" target="_blank">\u89c2\u770b</a>'
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', t)
        t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
        ps.append(f'<div class="{nc}"><div class="{dc}">{esc(it.get("date",""))}</div><div class="{bc}">{t}</div></div>')
    return ''.join(ps)

def build():
    try:
        with open(os.path.join(ROOT, 'data.json')) as f:
            data = json.load(f)
        with open(os.path.join(ROOT, 'dynamics.json')) as f:
            dynamics = json.load(f)
    except FileNotFoundError as e:
        print(f'Error: {e}', file=sys.stderr)
        return False

    fans = data.get('fans', 0)
    works = data.get('works', 0)
    dcnt = data.get('dynamics', 0)
    live_s = data.get('live_status', 0)
    live_t = data.get('live_title', '') or '\u865a\u62df\u4e3b\u64ad'
    name = data.get('name', '\u96ea\u68a8')
    live_text = '\u76f4\u64ad\u4e2d' if live_s == 1 else '\u79bb\u7ebf'
    cnt = len(dynamics)
    dv = json.dumps(dynamics, ensure_ascii=False)
    dyn_d = dyn_html(dynamics, False)
    dyn_m = dyn_html(dynamics, True)

    css = (
        '*{margin:0;padding:0;box-sizing:border-box}'
        'body{font-family:"Microsoft YaHei",sans-serif;background:#050816;color:#fff}'
        f'.{cl("C")},.{cl("D")}{{display:none}}body.C .{cl("C")}{{display:block}}body.D .{cl("D")}{{display:block}}'
        f'.{cl("C")} .{cl("a")}{{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:15px 30px;background:#0a1025;border-bottom:1px solid #00d9ff55}}'
        f'.{cl("C")} .{cl("b")}{{font-size:28px;color:#00d9ff;font-weight:bold}}'
        f'.{cl("C")} .{cl("c")}{{display:flex;gap:10px;flex-wrap:wrap}}.{cl("C")} .{cl("c")} a{{color:white;text-decoration:none;padding:8px 14px;border-radius:8px}}.{cl("C")} .{cl("c")} a:hover{{background:#00d9ff22}}'
        f'.{cl("C")} .{cl("x")} input{{padding:10px 15px;border:none;border-radius:8px;background:#111b3a;color:white;width:240px;outline:none}}'
        f'.{cl("C")} .{cl("d")}{{display:flex;gap:40px;padding:50px 30px;justify-content:center;align-items:center}}'
        f'.{cl("C")} .{cl("e")}{{flex:1;min-height:320px;background:#0c1430;border:1px solid #00d9ff44;border-radius:18px;padding:30px}}.{cl("C")} .{cl("e")} h1{{margin-bottom:15px;font-size:24px}}'
        f'.{cl("C")} .{cl("f")}{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-top:20px}}'
        f'.{cl("C")} .{cl("g")}{{background:#121d40;padding:15px;border-radius:12px;text-align:center;white-space:nowrap}}.{cl("C")} .{cl("g")} b{{display:block;font-size:24px;color:#00d9ff}}'
        f'.{cl("C")} .{cl("E")}{{font-size:13px;color:#fff;display:block;margin-top:2px}}'
        f'.{cl("C")} .{cl("h")}{{padding:20px 30px 60px}}'
        f'.{cl("C")} .{cl("i")}{{background:#0c1430;border-radius:18px;padding:25px;border:1px solid #00d9ff44}}.{cl("C")} .{cl("i")} h2{{margin-bottom:20px;color:#00d9ff}}'
        f'.{cl("C")} .{cl("j")}{{position:relative;padding-left:20px}}.{cl("C")} .{cl("j")}::before{{content:"";position:absolute;left:6px;top:8px;bottom:8px;width:2px;background:linear-gradient(to bottom,#0df6,#d86fff66);border-radius:1px}}'
        f'.{cl("C")} .{cl("k")}{{position:relative;margin-bottom:28px;padding-left:8px}}.{cl("C")} .{cl("k")}::before{{content:"";position:absolute;left:-16px;top:5px;width:12px;height:12px;border-radius:50%;background:linear-gradient(135deg,#0df,#d86fff);border:2px solid #0c1430;box-shadow:0 0 8px rgba(0,217,255,.4)}}'
        f'.{cl("C")} .{cl("l")}{{font-size:13px;color:#0df;font-weight:bold;margin-bottom:6px}}'
        f'.{cl("C")} .{cl("m")}{{background:#0a1025;border:1px solid #0df3;border-radius:10px;padding:12px 16px;font-size:14px;line-height:1.7;color:#ddd}}.{cl("C")} .{cl("m")} b{{color:#fff}}'
        f'.{cl("C")} .{cl("n")}{{color:#666;padding:20px;text-align:center}}'
        f'.{cl("C")} .{cl("o")}{{text-align:center;padding:20px;border-top:1px solid #0df3;color:#999;font-size:13px}}'
        f'.{cl("D")}{{padding-bottom:80px}}'
        f'.{cl("D")} .{cl("a")}{{position:sticky;top:0;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:15px;background:#08101f;border-bottom:1px solid rgba(0,229,255,.3)}}'
        f'.{cl("D")} .{cl("b")}{{font-size:22px;font-weight:bold;color:#00E5FF}}.{cl("D")} .{cl("y")}{{font-size:24px}}'
        f'.{cl("D")} .{cl("d")}{{text-align:center;padding:30px 20px}}'
        f'.{cl("D")} .{cl("z")}{{font-size:32px;margin-top:20px;background:linear-gradient(135deg,#00E5FF,#D86FFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}'
        f'.{cl("D")} .{cl("A")}{{color:#bdbdbd;margin-top:10px}}'
        f'.{cl("D")} .{cl("w")}{{padding:20px}}'
        f'.{cl("D")} .{cl("e")}{{background:#0d1328;border:1px solid rgba(0,229,255,.2);border-radius:16px;padding:18px;margin-bottom:15px}}.{cl("D")} .{cl("e")} h3{{margin-bottom:10px;color:#00E5FF}}'
        f'.{cl("D")} .{cl("u")}{{text-align:center;padding:10px 20px;font-size:18px;color:#00E5FF;background:#0d1328;margin:0 20px;border-radius:12px}}'
        f'.{cl("D")} .{cl("p")}{{position:relative;padding-left:16px}}.{cl("D")} .{cl("p")}::before{{content:"";position:absolute;left:4px;top:8px;bottom:8px;width:2px;background:linear-gradient(to bottom,#0df6,#d86fff66);border-radius:1px}}'
        f'.{cl("D")} .{cl("q")}{{position:relative;margin-bottom:20px;padding-left:6px}}.{cl("D")} .{cl("q")}::before{{content:"";position:absolute;left:-14px;top:4px;width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#0df,#d86fff);border:2px solid #0d1328;box-shadow:0 0 6px rgba(0,217,255,.4)}}'
        f'.{cl("D")} .{cl("r")}{{font-size:12px;color:#0df;font-weight:bold;margin-bottom:4px}}'
        f'.{cl("D")} .{cl("s")}{{background:#0a1025;border:1px solid #0df3;border-radius:8px;padding:10px 12px;font-size:13px;line-height:1.6;color:#ccc}}.{cl("D")} .{cl("s")} b{{color:#fff}}'
        f'.{cl("D")} .{cl("t")}{{color:#666;padding:10px;text-align:center;font-size:13px}}'
        f'.{cl("D")} .{cl("v")}{{position:fixed;bottom:0;left:0;width:100%;height:65px;background:#08101f;border-top:1px solid rgba(0,229,255,.3);display:flex;justify-content:space-around;align-items:center}}.{cl("D")} .{cl("v")} a{{color:white;text-decoration:none;font-size:13px;text-align:center}}.{cl("D")} .{cl("v")} span{{display:block;font-size:22px}}'
        '.sb{display:flex;gap:8px;margin-bottom:12px}.sb input{flex:1;padding:10px 14px;border:none;border-radius:8px;background:#111b3a;color:white;font-size:14px;outline:none}.sb input:focus{outline:2px solid #0df}.sb button{background:#333;border:none;color:#999;border-radius:8px;padding:0 14px;cursor:pointer}.scnt{font-size:12px;color:#666;margin:-8px 0 10px}'
    )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>My World</title>
<style>{css}</style>
</head>
<body>
<div class="C">
<a class="a"><div class="b">My World</div><nav class="c"><a href="#">首页</a><a href="#">介绍</a><a href="#">直播</a><a href="https://space.bilibili.com/394065596" target="_blank">雪梨B站</a></nav><div class="x"><input type="text" id="q" placeholder="搜索动态..." oninput="_F()"></div></a>
<section class="d"><div class="e"><h1>Hello, I am Myself</h1><p>个人主页</p><div class="f"><div class="g"><b>0</b>项目</div><div class="g"><b>0</b>文章</div><div class="g"><b>{fans}</b>粉丝</div><div class="g"><b>{dcnt}</b>动态</div></div></div><div class="e"><h1>{esc(name)}</h1><p>{esc(live_t)}</p><div class="f"><div class="g"><b>{live_text}</b><span class="E">直播</span></div><div class="g"><b>{fans}</b>粉丝</div><div class="g"><b>{works}</b>作品</div><div class="g"><b>{dcnt}</b>动态</div></div></div></section>
<section class="h"><div class="i"><h2>动态</h2><div class="sb"><input type="text" id="q2" placeholder="搜索动态..." oninput="_F()"><button onclick="_C()">✕</button></div><div class="scnt" id="sc">共 {cnt} 条</div><div class="j" id="tl">{dyn_d}</div></div></section>
<footer class="o">&copy; 2026 My World &middot; By Mcldy</footer>
</div>
<div class="D">
<a class="a"><div class="y">☰</div><div class="b">My World</div><div class="y">🔍</div></a>
<section class="d"><h1 class="z">Welcome To My World</h1><p class="A">Connecting Two Worlds</p></section>
<div class="u"><span id="nn">{esc(name)}</span> 粉丝 <b>{fans}</b> &middot; 直播: <b>{live_text}</b> &middot; 作品: <b>{works}</b> &middot; 动态: <b>{dcnt}</b></div>
<section class="w"><div class="e"><h3>动态</h3><div class="sb"><input type="text" id="q3" placeholder="搜索..." oninput="_F()"><button onclick="_C()">✕</button></div><div class="scnt" id="sc2">共 {cnt} 条</div><div class="p" id="tml">{dyn_m}</div></div></section>
<nav class="v"><a href="#"><span>🏠</span>首页</a><a href="#"><span>📜</span>动态</a><a href="https://space.bilibili.com/394065596" target="_blank"><span>🌸</span>B站</a></nav>
</div>
<script>
var D = {dv};
function _S() {{ var a=document.getElementById('q'), b=document.getElementById('q2'), c=document.getElementById('q3'); return (a?a.value:'') || (b?b.value:'') || (c?c.value:''); }}
function _F() {{ var k=_S().toLowerCase(), t=document.getElementById('tl'), m=document.getElementById('tml'), sc=document.getElementById('sc'), sc2=document.getElementById('sc2'), c=0; D.forEach(function(d,i){{ var txt=(d.content+' '+(d.video&&d.video.title||'')+' '+d.date).toLowerCase(); if(t&&t.children[i]) t.children[i].style.display=(k&&!txt.includes(k))?'none':''; if(m&&m.children[i]) m.children[i].style.display=(k&&!txt.includes(k))?'none':''; if(!t||!t.children[i]||t.children[i].style.display!='none') c++; }}); if(sc) sc.textContent='共 '+c+' 条'; if(sc2) sc2.textContent='共 '+c+' 条'; }}
function _C() {{ var a=document.getElementById('q'), b=document.getElementById('q2'), c=document.getElementById('q3'); if(a) a.value=''; if(b) b.value=''; if(c) c.value=''; _F(); }}
(function(){{ var _M=/Mobi|Android|iPhone|iP(ad|od)/i.test(navigator.userAgent)||window.innerWidth<768; document.body.className=_M?'D':'C'; }})();
</script>
</body>
</html>'''

    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r'^\s+|\s+$', '', html, flags=re.MULTILINE)
    html = re.sub(r'\n{2,}', '\n', html)

    os.makedirs(DEPLOY, exist_ok=True)
    with open(os.path.join(DEPLOY, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    size = len(html.encode('utf-8'))
    print(f'Built: index.html ({size:,} bytes, {cnt} dynamics)')
    return True

if __name__ == '__main__':
    build()
