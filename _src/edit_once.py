"""한 번만 실행: 나눈 조각을 여러 페이지 구조에 맞게 고친다 (2026-11-20)."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = f'{R}/_src/parts'
def rd(n): return open(f'{P}/{n}.html', encoding='utf-8').read()
def wr(n, s): open(f'{P}/{n}.html', 'w', encoding='utf-8').write(s)
def rep(s, a, b, cnt=1):
    assert s.count(a) == cnt, (a[:60], s.count(a)); return s.replace(a, b)
def T(en, ko, ja): return f'<span class="en">{en}</span><span class="ko">{ko}</span><span class="ja">{ja}</span>'

# head: 페이지별 제목·주소 자리표시 + 공통 CSS
s = rd('head')
s = rep(s, '<title>FabWatch</title>', '<title>{TITLE}</title>')
s = rep(s, '<link rel="canonical" href="https://fabwatch.co.kr">', '<link rel="canonical" href="https://fabwatch.co.kr{PATH}">')
s = rep(s, '<meta property="og:url" content="https://fabwatch.co.kr">', '<meta property="og:url" content="https://fabwatch.co.kr{PATH}">')
s = s.rstrip('\n') + '\n<link rel="stylesheet" href="/assets/site.css">\n'
wr('head', s)

# nav: 상품 2개 + 요금제 + 회사 소개
s = rd('nav')
s = rep(s, '<a href="#" class="logo">', '<a href="/" class="logo">')
a = s.index('      <li><a href="#services"'); b = s.index('      <li><select class="lang-toggle"')
links = (f'      <li><a href="/monitoring/" class="hide-xs" data-nav="monitoring">{T("Monitoring", "모니터링", "モニタリング")}</a></li>\n'
         f'      <li><a href="/reports/" class="hide-xs" data-nav="reports">{T("Reports", "리포트", "レポート")}</a></li>\n'
         f'      <li><a href="/pricing/" class="hide-mobile" data-nav="pricing">{T("Pricing", "요금제", "料金")}</a></li>\n'
         f'      <li><a href="/about/" class="hide-mobile" data-nav="about">{T("About", "회사 소개", "会社概要")}</a></li>\n')
s = s[:a] + links + s[b:]
wr('nav', s)

# hero: 버튼 → 두 상품
s = rd('hero')
s = rep(s, '<a href="#demo" class="btn btn-outline">', '<a href="/monitoring/" class="btn btn-outline">')
i = s.index('    <div class="stats-bar">'); j = s.rindex('    </div>\n', 0, i)
btn = ('      <a href="/reports/" class="btn btn-outline">\n'
       '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>\n'
       f'        {T("Sample Reports", "샘플 리포트 보기", "サンプルレポートを見る")}\n      </a>\n')
s = s[:j] + btn + s[j:]
wr('hero', s)

# services: 카드마다 상품 페이지로 가는 버튼
s = rd('services')
go = 'display:inline-flex;align-items:center;gap:6px;margin-top:14px;font-size:14px;font-weight:600;color:var(--accent);text-decoration:none;'
s = rep(s, '<span class="ko">Pro / Enterprise 요금제에 포함</span><span class="ja">Pro／Enterpriseプランに含まれます</span>\n        </div>',
        '<span class="ko">Pro / Enterprise 요금제에 포함</span><span class="ja">Pro／Enterpriseプランに含まれます</span>\n        </div>\n'
        f'        <a href="/monitoring/" style="{go}">{T("Open the live demo →", "대시보드 데모 보기 →", "ダッシュボードのデモを見る →")}</a>')
s = rep(s, '<span class="ja">月次無料レポートを全会員に提供 — プレミアムレポートは別途販売</span>\n        </div>',
        '<span class="ja">月次無料レポートを全会員に提供 — プレミアムレポートは別途販売</span>\n        </div>\n'
        f'        <a href="/reports/" style="{go.replace("var(--accent)", "var(--accent-warm)")}">{T("Read sample reports →", "샘플 리포트 보기 →", "サンプルレポートを読む →")}</a>')
s = rep(s, '</div>\n  </div>\n</section>', f'</div>\n    <p style="text-align:center;margin-top:24px;font-size:14px;"><a href="/pricing/" style="color:var(--fg-muted);">{T("Compare plans and pricing", "요금제 비교 보기", "料金プランを比較する")}</a></p>\n  </div>\n</section>')
wr('services', s)

# insights: PDF 경로를 절대 경로로
s = rd('insights'); s = s.replace('href="reports/', 'href="/reports/'); wr('insights', s)

# problem: 근거를 확인하지 못한 숫자 3개(90일·30%·$4K~11K) 삭제
s = rd('problem')
a = s.index('    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:32px;">')
b = s.index('  </div>\n</section>')
s = s[:a] + s[b:]
wr('problem', s)

# footer 링크
s = rd('footer')
for a_, b_ in [('<a href="#services"><span class="en">Dashboard', '<a href="/monitoring/"><span class="en">Dashboard'),
               ('<a href="#services"><span class="en">Reports', '<a href="/reports/"><span class="en">Reports'),
               ('<a href="#pricing">', '<a href="/pricing/">'), ('<a href="#demo">', '<a href="/monitoring/#demo">'),
               ('<a href="#team">', '<a href="/about/#team">'), ('<a href="#insights">', '<a href="/reports/">'),
               ('<a href="#usecases">', '<a href="/about/#usecases">'), ('<a href="#faq">', '<a href="/#faq">')]:
    s = rep(s, a_, b_)
s = s.replace('<span class="ko">블로그</span>', '<span class="ko">샘플 리포트</span>').replace('<span class="en">Blog</span>', '<span class="en">Sample Reports</span>').replace('<span class="ja">ブログ</span>', '<span class="ja">サンプルレポート</span>')
wr('footer', s)

# script: 데이터 경로, 예전 주소 이동, 현재 메뉴 표시
j = open(f'{R}/assets/site.js', encoding='utf-8').read()
j = rep(j, "var LIVE_DATA_URL = 'fabwatch_data.json';", "var LIVE_DATA_URL = '/fabwatch_data.json';")
pre = """// 2026-11-20 여러 페이지 구조: 예전 한 페이지 주소(#demo 등)로 들어오면 새 페이지로 보낸다
(function() {
  var p = location.pathname, h = location.hash;
  if ((p === '/' || p === '/index.html') && h) {
    var M = {'#demo': '/monitoring/#demo', '#map': '/monitoring/#map', '#how-it-works': '/monitoring/#how-it-works',
             '#coverage': '/monitoring/#coverage', '#pricing': '/pricing/', '#insights': '/reports/',
             '#team': '/about/#team', '#usecases': '/about/#usecases'};
    if (M[h]) location.replace(M[h]);
  }
  document.addEventListener('DOMContentLoaded', function() {
    var seg = p.split('/')[1];
    document.querySelectorAll('[data-nav]').forEach(function(a) {
      if (a.getAttribute('data-nav') === seg) { a.style.color = '#FFFFFF'; a.setAttribute('aria-current', 'page'); }
    });
  });
})();
"""
open(f'{R}/assets/site.js', 'w', encoding='utf-8').write(pre + j)
print('done')
