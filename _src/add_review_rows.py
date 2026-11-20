"""2026-11-20 사이트 개편으로 새로 생긴 문구를 일본어 검수표에 추가하고, 삭제된 문구에 메모를 단다."""
import sys, copy, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
F = sys.argv[1]
wb = openpyxl.load_workbook(F); ws = wb['일본어 검수']
NEW = [  # (위치, 한국어, 영어, 일본어)
 ('상단 메뉴', '모니터링', 'Monitoring', 'モニタリング'),
 ('상단 메뉴', '리포트', 'Reports', 'レポート'),
 ('상단 메뉴', '회사 소개', 'About', '会社概要'),
 ('첫 화면 버튼', '샘플 리포트 보기', 'Sample Reports', 'サンプルレポートを見る'),
 ('홈 상품 카드', '대시보드 데모 보기 →', 'Open the live demo →', 'ダッシュボードのデモを見る →'),
 ('홈 상품 카드', '샘플 리포트 보기 →', 'Read sample reports →', 'サンプルレポートを読む →'),
 ('홈 상품 카드 아래', '요금제 비교 보기', 'Compare plans and pricing', '料金プランを比較する'),
 ('/monitoring 머리말', '상품 1 · 플랫폼', 'PRODUCT 1 · PLATFORM', '商品1 · プラットフォーム'),
 ('/monitoring 머리말', '모니터링 대시보드', 'Monitoring Dashboard', 'モニタリング・ダッシュボード'),
 ('/monitoring 머리말', '24개 팹과 9개 AI 데이터센터를 6개 위성 채널로 추적합니다. 아래 데모를 직접 써 보고, 커버리지와 신호를 만드는 방법을 확인하세요.',
  '24 fabs and 9 AI data centers, tracked with 6 satellite channels. Try the live demo below, then see coverage and how the signals are built.',
  '24のファブと9つのAIデータセンターを6つの衛星チャネルで追跡します。下のデモを実際に操作し、カバレッジとシグナルの作り方をご確認ください。'),
 ('/reports 머리말', '상품 2 · 리포트', 'PRODUCT 2 · REPORTS', '商品2 · レポート'),
 ('/reports 머리말', '분석 리포트', 'Analysis Reports', '分析レポート'),
 ('/reports 머리말', '위성 기록을 기업 공시·증권사 추정·언론 보도와 맞대어 봅니다. 샘플은 영어·한국어·일본어 PDF로 받아 보실 수 있습니다.',
  'Satellite records checked against company filings, broker estimates and news. Download the samples in English, Korean or Japanese.',
  '衛星の記録を企業の開示・証券会社の推定・報道と突き合わせます。サンプルは英語・韓国語・日本語のPDFでご覧いただけます。'),
 ('/pricing 머리말', '요금제', 'PRICING', '料金'),
 ('/pricing 머리말', '대시보드와 리포트 요금제', 'Plans for the dashboard and reports', 'ダッシュボードとレポートの料金'),
 ('/pricing 머리말', '월간 하이라이트 리포트는 무료입니다. Pro와 Enterprise는 전체 대시보드, 알림, 프리미엄 리포트를 더합니다.',
  'Start free with the monthly highlight report. Pro and Enterprise add the full dashboard, alerts and premium reports.',
  '月次ハイライトレポートは無料です。ProとEnterpriseでは、ダッシュボード全体・アラート・プレミアムレポートが加わります。'),
 ('/about 머리말', '회사 소개', 'ABOUT', '会社概要'),
 ('/about 머리말', '왜 위성인가, 그리고 우리는 누구인가', 'Why satellites, and who we are', 'なぜ衛星なのか、そして私たちについて'),
 ('/about 머리말', '지금의 반도체 정보가 놓치는 부분, 위성이 그 빈틈을 채우는 곳, 활용하는 사람들, 그리고 FabWatch를 만드는 팀을 소개합니다.',
  "The gap in today's semiconductor intelligence, where satellite data fills it, who uses it, and the team behind FabWatch.",
  '今の半導体情報が見落とす部分、衛星がその隙間を埋める場所、活用する人々、そしてFabWatchをつくるチームをご紹介します。'),
 ('하단 메뉴 (블로그 → 바뀜)', '샘플 리포트', 'Sample Reports', 'サンプルレポート'),
]
last = ws.max_row; n0 = int(ws.cell(last, 1).value)
for k, (where, ko, en, ja) in enumerate(NEW, 1):
    r = last + k
    for c, v in enumerate([n0 + k, ko, en, ja, None, f'2026-11-20 개편 추가 · {where}'], 1):
        cell = ws.cell(r, c, v); src = ws.cell(last, c)
        cell.font = copy.copy(src.font); cell.fill = copy.copy(src.fill); cell.border = copy.copy(src.border); cell.alignment = copy.copy(src.alignment)
# 사이트에서 빠진 문구: 메모만 단다 (행은 지우지 않음)
GONE = {'90 days': '2026-11-20 사이트에서 삭제(근거 미확인) — 검수 불필요', '30%': '2026-11-20 사이트에서 삭제(근거 미확인) — 검수 불필요',
        '$4K': '2026-11-20 사이트에서 삭제(근거 미확인) — 검수 불필요', '블로그': '2026-11-20 하단 메뉴에서 "샘플 리포트"로 바뀜 — 검수 불필요',
        '대기 등록': None}
marked = []
for r in range(2, last + 1):
    ko = str(ws.cell(r, 2).value or ''); en = str(ws.cell(r, 3).value or '')
    for key, memo in GONE.items():
        if memo and (ko.strip() == key or en.startswith(key) or ko.startswith(key)):
            old = ws.cell(r, 6).value
            ws.cell(r, 6).value = memo if not old else f'{old} / {memo}'; marked.append((r, ko[:30]))
wb.save(F)
print('added', len(NEW), 'rows from', last + 1, 'to', ws.max_row); print('marked', marked)
