"""한 번만 실행: 기존 단일 index.html을 조각으로 나눈다 (2026-11-20).
결과: assets/site.css, assets/site.js, _src/parts/*.html
이후에는 parts를 고치고 build.py로 페이지를 만든다.
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = open(f'{R}/index.html', encoding='utf-8').read().split('\n')
def seg(a, b):  # 1-based inclusive
    return '\n'.join(L[a - 1:b]) + '\n'
os.makedirs(f'{R}/assets', exist_ok=True); P = f'{R}/_src/parts'; os.makedirs(P, exist_ok=True)
assert L[22].strip() == '<style>' and L[1090].strip() == '</style>' and L[2889].strip() == '<script>' and L[3436].strip() == '</script>'
open(f'{R}/assets/site.css', 'w', encoding='utf-8').write(seg(24, 1090))
open(f'{R}/assets/site.js', 'w', encoding='utf-8').write(seg(2891, 3436))
open(f'{P}/head.html', 'w', encoding='utf-8').write(seg(1, 22))
cuts = [('nav', 1092, 1112), ('hero', 1113, 1231), ('trust', 1232, 1250), ('problem', 1251, 1288), ('why', 1289, 1335),
        ('scope', 1336, 1382), ('where', 1383, 1420), ('compare', 1421, 1465), ('channels', 1466, 1561), ('pipeline', 1562, 1613),
        ('lifecycle', 1614, 1672), ('services', 1673, 1735), ('pricing', 1736, 1818), ('demo', 1819, 2007), ('map', 2008, 2191),
        ('insights', 2192, 2280), ('faq', 2281, 2353), ('usecases', 2354, 2402), ('team', 2403, 2443), ('cta', 2444, 2476),
        ('modals', 2477, 2831), ('footer', 2832, 2889)]
for n, a, b in cuts:
    open(f'{P}/{n}.html', 'w', encoding='utf-8').write(seg(a, b))
# 검증: 조각을 다시 이으면 원본과 같아야 한다
whole = seg(1, 22) + '<style>\n' + seg(24, 1090) + '</style>\n' + ''.join(seg(a, b) for _, a, b in cuts) + '<script>\n' + seg(2891, 3436) + '</script>\n' + ''.join(x + '\n' for x in L[3437:])
print('roundtrip', whole.rstrip('\n') == '\n'.join(L).rstrip('\n'))
