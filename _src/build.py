"""FabWatch 사이트 페이지 조립 (2026-11-20부터 여러 페이지 구조).
문구 수정은 _src/parts/*.html, 디자인은 assets/site.css, 동작은 assets/site.js에서 한다.
실행: python -I _src/build.py  → index.html, monitoring/, reports/, pricing/, about/ 의 index.html
(_src 폴더는 GitHub Pages가 공개하지 않는다 — 밑줄로 시작하는 폴더)
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = f'{R}/_src/parts'
def part(n): return open(f'{P}/{n}.html', encoding='utf-8').read()
def T(en, ko, ja): return f'<span class="en">{en}</span><span class="ko">{ko}</span><span class="ja">{ja}</span>'

def intro(label, title, desc):
    """하위 페이지 맨 위의 짧은 머리말 (첫 화면과 같은 어두운 띠)"""
    return f'''
<!-- PAGE INTRO -->
<section class="hero" style="padding-block:56px 44px;">
  <div class="inner">
    <div class="section-label" style="color:var(--accent);">{label}</div>
    <h1 style="font-family:var(--font-display);font-size:clamp(28px,4vw,40px);font-weight:800;line-height:1.2;margin:8px 0 12px;">{title}</h1>
    <p style="max-width:640px;color:#94A3B8;font-size:16px;line-height:1.7;margin:0;">{desc}</p>
  </div>
</section>
'''

PAGES = {
 '': ('FabWatch — Satellite Intelligence for Semiconductor Fabs & AI Data Centers',
      ['hero', 'trust', 'services', 'why', 'faq', 'cta']),
 'monitoring': ('Monitoring Dashboard — FabWatch',
      [intro(T('PRODUCT 1 · PLATFORM', '상품 1 · 플랫폼', '商品1 · プラットフォーム'),
             T('Monitoring Dashboard', '모니터링 대시보드', 'モニタリング・ダッシュボード'),
             T('24 fabs and 9 AI data centers, tracked with 6 satellite channels. Try the live demo below, then see coverage and how the signals are built.',
               '24개 팹과 9개 AI 데이터센터를 6개 위성 채널로 추적합니다. 아래 데모를 직접 써 보고, 커버리지와 신호를 만드는 방법을 확인하세요.',
               '24のファブと9つのAIデータセンターを6つの衛星チャネルで追跡します。下のデモを実際に操作し、カバレッジとシグナルの作り方をご確認ください。')),
       'demo', 'map', 'scope', 'channels', 'pipeline', 'lifecycle', 'cta']),
 'reports': ('Sample Reports — FabWatch',
      [intro(T('PRODUCT 2 · REPORTS', '상품 2 · 리포트', '商品2 · レポート'),
             T('Analysis Reports', '분석 리포트', '分析レポート'),
             T('Satellite records checked against company filings, broker estimates and news. Download the samples in English, Korean or Japanese.',
               '위성 기록을 기업 공시·증권사 추정·언론 보도와 맞대어 봅니다. 샘플은 영어·한국어·일본어 PDF로 받아 보실 수 있습니다.',
               '衛星の記録を企業の開示・証券会社の推定・報道と突き合わせます。サンプルは英語・韓国語・日本語のPDFでご覧いただけます。')),
       'insights', 'cta']),
 'pricing': ('Pricing — FabWatch',
      [intro(T('PRICING', '요금제', '料金'),
             T('Plans for the dashboard and reports', '대시보드와 리포트 요금제', 'ダッシュボードとレポートの料金'),
             T('Start free with the monthly highlight report. Pro and Enterprise add the full dashboard, alerts and premium reports.',
               '월간 하이라이트 리포트는 무료입니다. Pro와 Enterprise는 전체 대시보드, 알림, 프리미엄 리포트를 더합니다.',
               '月次ハイライトレポートは無料です。ProとEnterpriseでは、ダッシュボード全体・アラート・プレミアムレポートが加わります。')),
       'pricing', 'cta']),
 'about': ('About — FabWatch',
      [intro(T('ABOUT', '회사 소개', '会社概要'),
             T('Why satellites, and who we are', '왜 위성인가, 그리고 우리는 누구인가', 'なぜ衛星なのか、そして私たちについて'),
             T('The gap in today\'s semiconductor intelligence, where satellite data fills it, who uses it, and the team behind FabWatch.',
               '지금의 반도체 정보가 놓치는 부분, 위성이 그 빈틈을 채우는 곳, 활용하는 사람들, 그리고 FabWatch를 만드는 팀을 소개합니다.',
               '今の半導体情報が見落とす部分、衛星がその隙間を埋める場所、活用する人々、そしてFabWatchをつくるチームをご紹介します。')),
       'problem', 'where', 'compare', 'usecases', 'team', 'cta']),
}

head, nav, modals, footer = part('head'), part('nav'), part('modals'), part('footer')
for slug, (title, blocks) in PAGES.items():
    path = f'/{slug}/' if slug else ''
    body = ''.join(b if b.lstrip().startswith('<') else part(b) for b in blocks)
    html = (head.replace('{TITLE}', title).replace('{PATH}', path) + '</head>\n<body>\n' + nav + body + modals + footer
            + '<script src="/assets/site.js"></script>\n</body>\n</html>\n')
    d = f'{R}/{slug}' if slug else R; os.makedirs(d, exist_ok=True)
    open(f'{d}/index.html', 'w', encoding='utf-8', newline='\n').write(html)
    print(f'/{slug}', len(html) // 1024, 'KB')
