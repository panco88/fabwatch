// 2026-11-20 여러 페이지 구조: 예전 한 페이지 주소(#demo 등)로 들어오면 새 페이지로 보낸다
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
function getLang() {
  try { var l = localStorage.getItem('fabwatch-lang'); return (l === 'ko' || l === 'ja' || l === 'en') ? l : 'en'; } catch(e) { return 'en'; }
}
function setLang(lang) {
  document.documentElement.setAttribute('data-lang', lang);
  try { localStorage.setItem('fabwatch-lang', lang); } catch(e) {}
  document.documentElement.lang = lang;
  var sel = document.querySelector('.lang-toggle');
  if (sel) sel.value = lang;
}
function toggleLang() {
  var order = ['en', 'ko', 'ja'];
  setLang(order[(order.indexOf(getLang()) + 1) % order.length]);
}
setLang(getLang());

// Waitlist modal
function openModal() {
  document.getElementById('waitlist-form').style.display = '';
  document.getElementById('waitlist-success').style.display = 'none';
  document.getElementById('loginModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('loginModal').classList.remove('open');
  document.body.style.overflow = '';
}
var WAITLIST_URL = 'https://script.google.com/macros/s/AKfycbxqExA94KdQwRJBnT20o1j9mbK7FeC2hDL_E3tSj-GvfCqC1ob65leTB8K6kfGu9ucL7A/exec';
function submitWaitlist(e) {
  e.preventDefault();
  var name = document.getElementById('wl-name').value.trim();
  var email = document.getElementById('wl-email').value.trim();
  var role = document.getElementById('wl-role').value;
  var company = document.getElementById('wl-company').value.trim();
  if (!name || !email) {
    alert(({ko:'이름과 이메일을 입력해주세요.', ja:'お名前とメールアドレスを入力してください。'})[getLang()] || 'Please enter your name and email.');
    return;
  }
  var btn = document.querySelector('#waitlist-form .form-submit');
  btn.disabled = true;
  btn.style.opacity = '0.6';
  btn.innerHTML = ({ko:'등록 중...', ja:'登録中...'})[getLang()] || 'Submitting...';
  if (WAITLIST_URL.indexOf('%%') === -1) {
    fetch(WAITLIST_URL, {
      method: 'POST', mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, email: email, role: role, company: company })
    }).then(function() {
      showWaitlistSuccess();
    }).catch(function() {
      showWaitlistSuccess();
    });
  } else {
    setTimeout(showWaitlistSuccess, 600);
  }
}
function showWaitlistSuccess() {
  document.getElementById('waitlist-form').style.display = 'none';
  document.getElementById('waitlist-success').style.display = '';
}
document.getElementById('loginModal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

function openLegal(id) {
  document.getElementById(id).classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLegal(id) {
  document.getElementById(id).classList.remove('open');
  document.body.style.overflow = '';
}
document.getElementById('privacyModal').addEventListener('click', function(e) {
  if (e.target === this) closeLegal('privacyModal');
});
document.getElementById('termsModal').addEventListener('click', function(e) {
  if (e.target === this) closeLegal('termsModal');
});

// Pricing member tabs
function switchMember(type) {
  document.getElementById('tab-individual').classList.toggle('active', type === 'individual');
  document.getElementById('tab-corporate').classList.toggle('active', type === 'corporate');
  document.getElementById('note-individual').style.display = type === 'individual' ? '' : 'none';
  document.getElementById('note-corporate').style.display = type === 'corporate' ? '' : 'none';
}

// FAQ accordion
function toggleFaq(btn) {
  var item = btn.closest('.faq-item');
  var wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(function(el) { el.classList.remove('open'); });
  if (!wasOpen) item.classList.add('open');
}

// Demo tab switching
function switchDemoTab(el, tab) {
  document.querySelectorAll('.demo-nav-item').forEach(function(n) { n.classList.remove('active'); });
  el.classList.add('active');
  document.querySelectorAll('.demo-view').forEach(function(v) { v.classList.remove('active'); });
  var target = document.getElementById('demo-' + tab);
  if (target) target.classList.add('active');
}

// Fab list filter (data-driven)
function filterFabs(btn, country) {
  document.querySelectorAll('.demo-filter-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  renderFabList(country);
}

// Newsletter
function handleNewsletter() {
  var email = document.getElementById('nl-email').value.trim();
  if (!email || email.indexOf('@') < 1) {
    alert(({ko:'이메일을 입력해주세요.', ja:'メールアドレスを入力してください。'})[getLang()] || 'Please enter a valid email.');
    return;
  }
  var btn = document.querySelector('.nl-btn');
  btn.disabled = true;
  btn.style.opacity = '0.6';
  if (WAITLIST_URL.indexOf('%%') === -1) {
    fetch(WAITLIST_URL, {
      method: 'POST', mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'newsletter', email: email })
    }).then(function() {
      document.getElementById('nl-success').classList.add('show');
      document.getElementById('nl-email').value = '';
      btn.disabled = false; btn.style.opacity = '';
    }).catch(function() {
      document.getElementById('nl-success').classList.add('show');
      document.getElementById('nl-email').value = '';
      btn.disabled = false; btn.style.opacity = '';
    });
  } else {
    document.getElementById('nl-success').classList.add('show');
    document.getElementById('nl-email').value = '';
    btn.disabled = false; btn.style.opacity = '';
  }
}

// Scroll reveal animation
(function() {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });
})();

// ── FabWatch Demo Data (24 fabs × 6 channels, from GEE pipeline simulation) ──
var FABS = [
{id:"samsung-pyeongtaek",name:"Samsung Pyeongtaek P1-P4",company:"Samsung",country:"kr",status:"operating",score:74.2,nl:[57.3,62.0,63.2,69.5,68.4,69.0,58.5,59.5,53.8,54.5,57.2,54.0],sar:-10.9,thermal:32.9,no2:7.9,ndvi:0.126,nlChange:-5.8},
{id:"samsung-hwaseong",name:"Samsung Hwaseong",company:"Samsung",country:"kr",status:"operating",score:74.1,nl:[67.8,69.6,65.5,64.0,66.8,64.7,61.9,66.9,64.1,57.6,60.9,59.7],sar:-7.2,thermal:30.5,no2:6.9,ndvi:0.121,nlChange:-11.9},
{id:"samsung-giheung",name:"Samsung Giheung",company:"Samsung",country:"kr",status:"operating",score:75.5,nl:[33.1,35.4,37.0,34.9,33.0,36.0,33.9,27.3,27.1,24.3,27.3,28.6],sar:-11.5,thermal:34.0,no2:7.5,ndvi:0.117,nlChange:-13.6},
{id:"sk-icheon",name:"SK hynix Icheon M16",company:"SK hynix",country:"kr",status:"operating",score:76.3,nl:[51.8,52.9,54.4,61.3,56.5,58.6,53.6,47.0,52.5,50.1,51.2,52.2],sar:-8.0,thermal:32.4,no2:8.3,ndvi:0.131,nlChange:0.8},
{id:"sk-cheongju",name:"SK hynix Cheongju M15",company:"SK hynix",country:"kr",status:"operating",score:74.6,nl:[33.4,38.9,40.8,36.0,36.4,35.2,36.7,33.8,31.6,28.1,27.2,31.7],sar:-8.5,thermal:31.7,no2:4.1,ndvi:0.132,nlChange:-5.1},
{id:"tsmc-fab18",name:"TSMC Fab 18 Tainan",company:"TSMC",country:"tw",status:"operating",score:80.2,nl:[73.1,78.1,74.1,84.6,83.3,83.1,78.6,76.9,65.1,71.9,67.5,75.5],sar:-8.1,thermal:37.4,no2:4.5,ndvi:0.121,nlChange:3.3},
{id:"tsmc-fab15",name:"TSMC Fab 15 Taichung",company:"TSMC",country:"tw",status:"operating",score:77.1,nl:[48.2,49.8,48.3,49.1,49.5,47.9,44.9,41.3,41.4,43.7,42.1,44.9],sar:-9.1,thermal:33.8,no2:5.3,ndvi:0.129,nlChange:-6.8},
{id:"tsmc-fab12",name:"TSMC Fab 12 Hsinchu",company:"TSMC",country:"tw",status:"operating",score:77.9,nl:[80.6,87.7,88.8,85.9,86.9,82.5,84.3,78.2,80.4,77.4,74.3,72.9],sar:-10.6,thermal:37.5,no2:7.2,ndvi:0.127,nlChange:-9.6},
{id:"tsmc-kaohsiung",name:"TSMC Fab 2 Kaohsiung",company:"TSMC",country:"tw",status:"construction",score:73.8,nl:[3.3,3.3,3.8,3.9,4.4,4.5,4.9,5.6,5.5,6.2,6.6,6.3],sar:-11.1,thermal:26.2,no2:3.6,ndvi:0.209,nlChange:90.9},
{id:"tsmc-arizona",name:"TSMC Fab 21 Arizona",company:"TSMC",country:"us",status:"construction",score:66.9,nl:[9.2,9.3,9.2,10.0,10.7,9.8,11.0,10.9,11.1,11.3,12.2,11.6],sar:-8.6,thermal:23.6,no2:4.1,ndvi:0.13,nlChange:26.1},
{id:"samsung-austin",name:"Samsung Austin",company:"Samsung",country:"us",status:"operating",score:77.6,nl:[41.3,44.3,46.2,46.6,44.9,47.4,43.2,45.6,40.7,40.5,37.0,43.0],sar:-9.6,thermal:34.2,no2:5.6,ndvi:0.132,nlChange:4.1},
{id:"intel-d1x",name:"Intel D1X Hillsboro",company:"Intel",country:"us",status:"operating",score:74.4,nl:[62.8,68.1,64.7,66.7,67.3,68.4,65.2,55.4,54.4,54.6,58.7,58.4],sar:-10.3,thermal:31.4,no2:5.1,ndvi:0.123,nlChange:-7.0},
{id:"intel-ohio",name:"Intel Ohio Fab",company:"Intel",country:"us",status:"construction",score:67.4,nl:[4.6,5.2,5.4,5.8,5.6,6.2,6.9,6.7,7.3,6.9,8.3,8.1],sar:-10.8,thermal:22.8,no2:3.8,ndvi:0.18,nlChange:76.1},
{id:"micron-hiroshima",name:"Micron Hiroshima",company:"Micron",country:"jp",status:"operating",score:76.7,nl:[66.4,70.6,67.3,63.1,67.8,67.1,67.7,65.1,58.8,58.5,58.0,61.8],sar:-9.8,thermal:33.8,no2:7.6,ndvi:0.135,nlChange:-6.9},
{id:"tsmc-jasm",name:"TSMC JASM Kumamoto",company:"TSMC",country:"jp",status:"ramping",score:83.4,nl:[27.0,31.8,34.7,39.6,43.5,45.5,47.6,56.0,53.8,58.9,63.4,64.2],sar:-9.1,thermal:43.6,no2:9.9,ndvi:0.167,nlChange:137.8},
{id:"smic-shanghai",name:"SMIC Shanghai",company:"SMIC",country:"cn",status:"operating",score:77.5,nl:[82.8,83.6,88.9,89.5,86.9,79.6,82.7,70.6,75.0,72.9,75.6,76.9],sar:-9.3,thermal:35.2,no2:9.3,ndvi:0.129,nlChange:-7.1},
{id:"smic-beijing",name:"SMIC Beijing",company:"SMIC",country:"cn",status:"operating",score:75.3,nl:[63.0,59.5,69.3,64.3,62.6,65.8,58.5,62.9,55.6,54.6,60.7,57.0],sar:-11.1,thermal:33.2,no2:3.7,ndvi:0.115,nlChange:-9.5},
{id:"ymtc-wuhan",name:"YMTC Wuhan",company:"YMTC",country:"cn",status:"operating",score:76.0,nl:[68.8,69.1,72.3,72.5,66.5,67.5,62.9,61.7,60.9,59.4,56.4,60.8],sar:-8.7,thermal:33.2,no2:7.3,ndvi:0.123,nlChange:-11.6},
{id:"cxmt-hefei",name:"CXMT Hefei",company:"CXMT",country:"cn",status:"operating",score:73.3,nl:[37.9,36.5,42.9,40.2,41.1,39.1,37.0,36.6,34.8,32.5,30.1,31.2],sar:-11.3,thermal:32.0,no2:8.1,ndvi:0.115,nlChange:-17.7},
{id:"infineon-dresden",name:"Infineon Dresden",company:"Infineon",country:"eu",status:"operating",score:74.6,nl:[69.3,75.7,76.7,75.9,74.4,73.3,71.0,66.7,68.6,63.2,67.5,73.2],sar:-10.2,thermal:28.1,no2:5.3,ndvi:0.115,nlChange:5.6},
{id:"globalfoundries-malta",name:"GlobalFoundries Malta",company:"GlobalFoundries",country:"us",status:"operating",score:75.2,nl:[73.1,80.0,79.2,75.8,76.3,77.2,74.9,73.5,67.3,68.6,67.7,70.4],sar:-10.2,thermal:31.8,no2:7.1,ndvi:0.116,nlChange:-3.7},
{id:"stmicro-crolles",name:"STMicroelectronics Crolles",company:"STMicro",country:"eu",status:"operating",score:74.0,nl:[46.2,54.0,55.3,56.5,50.5,51.3,48.8,48.4,43.2,43.6,42.5,47.1],sar:-9.8,thermal:29.2,no2:7.2,ndvi:0.116,nlChange:1.9},
{id:"umc-tainan",name:"UMC Fab 12A Tainan",company:"UMC",country:"tw",status:"operating",score:76.7,nl:[64.7,62.3,64.8,67.5,73.6,68.8,68.4,63.8,57.7,58.3,58.6,57.3],sar:-9.8,thermal:36.1,no2:9.3,ndvi:0.117,nlChange:-11.4},
{id:"micron-singapore",name:"Micron Singapore Fab 10N",company:"Micron",country:"sg",status:"operating",score:69.3,nl:[34.3,34.6,39.1,37.3,35.2,36.5,31.2,29.6,29.6,28.8,26.6,26.9],sar:-9.9,thermal:27.4,no2:7.6,ndvi:0.122,nlChange:-21.6}
];

var MONTHS = ['Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov'];
var selectedFabIdx = 0;
var currentChannel = 0;
var channelTimer = null;
var CHANNELS = [
  {key:'nl', labelEn:'Nightlight Index', labelKo:'야간조명 지수', labelJa:'夜間光指数', color:'var(--accent)', unit:'nW/cm²/sr'},
  {key:'sarArr', labelEn:'SAR Backscatter', labelKo:'SAR 백스캐터', labelJa:'SAR 後方散乱', color:'var(--accent-warm)', unit:'dB'},
  {key:'thermalArr', labelEn:'Thermal IR', labelKo:'열적외선 온도', labelJa:'熱赤外 温度', color:'#EF4444', unit:'°C'},
  {key:'no2Arr', labelEn:'NO₂ Emissions', labelKo:'NO₂ 배출량', labelJa:'NO₂ 排出量', color:'#A78BFA', unit:'×10⁻⁵'},
  {key:'ndviArr', labelEn:'NDVI Vegetation', labelKo:'NDVI 식생지수', labelJa:'NDVI 植生指数', color:'#4ADE80', unit:''}
];

function renderDemoData() {
  renderStats();
  renderChart(selectedFabIdx, currentChannel);
  var activeBtn = document.querySelector('.demo-filter-btn.active');
  var activeCountry = 'all';
  if (activeBtn) {
    var m = (activeBtn.getAttribute('onclick')||'').match(/'(\w+)'/);
    if (m) activeCountry = m[1];
  }
  renderFabList(activeCountry);
  renderSignals(selectedFabIdx);
  renderAlerts();
  startChannelRotation();
}

function startChannelRotation() {
  if (channelTimer) clearInterval(channelTimer);
  channelTimer = setInterval(function() {
    currentChannel = (currentChannel + 1) % CHANNELS.length;
    renderChart(selectedFabIdx, currentChannel);
    updateChannelIndicator();
    var activeBtn = document.querySelector('.demo-filter-btn.active');
    var activeCountry = 'all';
    if (activeBtn) {
      var m = (activeBtn.getAttribute('onclick')||'').match(/'(\w+)'/);
      if (m) activeCountry = m[1];
    }
    renderFabList(activeCountry, currentChannel);
  }, 4000);
}

function updateChannelIndicator() {
  var el = document.getElementById('demo-channel-dots');
  if (!el) return;
  var html = '';
  CHANNELS.forEach(function(ch, i) {
    var active = i === currentChannel;
    html += '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 3px;cursor:pointer;transition:all 0.3s;' +
      'background:' + (active ? ch.color : 'var(--fg-muted)') + ';opacity:' + (active ? '1' : '0.3') + ';" onclick="switchChannel(' + i + ')"></span>';
  });
  el.innerHTML = html;
}

function renderStats() {
  var op = FABS.filter(function(f){return f.status==='operating';}).length;
  var con = FABS.filter(function(f){return f.status==='construction';}).length;
  var ramp = FABS.filter(function(f){return f.status==='ramping';}).length;
  var alerts = FABS.filter(function(f){return f.nlChange<-10||f.nlChange>30;}).length;
  var critical = FABS.filter(function(f){return f.nlChange<-15;}).length;
  document.getElementById('demo-stats-row').innerHTML =
    '<div class="demo-stat-card">' +
      '<div class="demo-stat-label"><span class="en">Active Fabs</span><span class="ko">가동 중</span><span class="ja">稼働中</span></div>' +
      '<div class="demo-stat-val">' + op + '</div>' +
      '<div class="demo-stat-delta" style="color:var(--accent-green);"><span class="en">+' + ramp + ' ramping</span><span class="ko">' + ramp + '곳 램프업</span><span class="ja">' + ramp + 'か所ランプアップ</span></div>' +
    '</div>' +
    '<div class="demo-stat-card">' +
      '<div class="demo-stat-label"><span class="en">Under Construction</span><span class="ko">건설 중</span><span class="ja">建設中</span></div>' +
      '<div class="demo-stat-val">' + con + '</div>' +
      '<div class="demo-stat-delta" style="color:var(--accent-warm);"><span class="en">' + con + ' new fabs</span><span class="ko">' + con + '곳 신규</span><span class="ja">' + con + 'か所新規</span></div>' +
    '</div>' +
    '<div class="demo-stat-card">' +
      '<div class="demo-stat-label"><span class="en">Alerts (7d)</span><span class="ko">알림 (7일)</span><span class="ja">アラート（7日）</span></div>' +
      '<div class="demo-stat-val" style="color:var(--accent-warm);">' + alerts + '</div>' +
      '<div class="demo-stat-delta" style="color:var(--accent-red);"><span class="en">' + critical + ' critical</span><span class="ko">' + critical + '건 주의</span><span class="ja">' + critical + '件 要注意</span></div>' +
    '</div>';
}

function switchChannel(idx) {
  currentChannel = idx;
  renderChart(selectedFabIdx, currentChannel);
  updateChannelIndicator();
  var activeBtn = document.querySelector('.demo-filter-btn.active');
  var activeCountry = 'all';
  if (activeBtn) {
    var m = (activeBtn.getAttribute('onclick')||'').match(/'(\w+)'/);
    if (m) activeCountry = m[1];
  }
  renderFabList(activeCountry, currentChannel);
  startChannelRotation();
}

function renderChart(idx, chIdx) {
  if (chIdx === undefined) chIdx = currentChannel;
  var fab = FABS[idx];
  var ch = CHANNELS[chIdx];
  var vals = fab[ch.key] || [];
  if (vals.length === 0) {
    for (var ci = 0; ci < CHANNELS.length; ci++) {
      vals = fab[CHANNELS[ci].key] || [];
      if (vals.length > 0) { ch = CHANNELS[ci]; break; }
    }
  }
  if (vals.length === 0) return;
  var maxVal = Math.max.apply(null, vals.map(function(v){return Math.abs(v);}));
  if (maxVal === 0) maxVal = 1;
  var titleEl = document.getElementById('demo-chart-title');
  if (titleEl) {
    titleEl.innerHTML = '<span class="en">' + ch.labelEn + ' — ' + fab.name + '</span><span class="ko">' + ch.labelKo + ' — ' + fab.name + '</span><span class="ja">' + ch.labelJa + ' — ' + fab.name + '</span>';
  }
  var barsEl = document.getElementById('demo-chart-bars');
  var html = '';
  var hasNeg = vals.some(function(v){return v < 0;});
  vals.forEach(function(val, i) {
    var absVal = Math.abs(val);
    var h = Math.max(5, (absVal / maxVal) * 95);
    var op = (0.4 + (absVal / maxVal) * 0.6).toFixed(1);
    var label = i < MONTHS.length ? MONTHS[i] : '';
    var dispVal = hasNeg ? val.toFixed(1) : val;
    html += '<div class="demo-bar" style="height:' + h.toFixed(0) + '%;background:' + ch.color + ';opacity:' + op + ';" data-val="' + val + '"><span class="demo-bar-tooltip">' + label + ': ' + dispVal + (ch.unit ? ' ' + ch.unit : '') + '</span></div>';
  });
  barsEl.innerHTML = html;
  animateChartBars();
}

function animateChartBars() {
  var bars = document.getElementById('demo-chart-bars');
  if (!bars) return;
  var children = bars.querySelectorAll('.demo-bar');
  children.forEach(function(bar, i) {
    var h = bar.style.height;
    bar.style.height = '0%';
    bar.style.transition = 'height 0.5s ease ' + (i * 0.04) + 's';
    requestAnimationFrame(function() {
      requestAnimationFrame(function() { bar.style.height = h; });
    });
  });
}

function getChannelVal(fab, chIdx) {
  var ch = CHANNELS[chIdx];
  var arr = fab[ch.key] || [];
  if (arr.length === 0) return {val: 0, change: 0};
  var latest = arr[arr.length - 1];
  var prev = arr.length >= 2 ? arr[arr.length - 2] : latest;
  var change = (prev !== 0 && arr.length >= 2) ? Math.round((latest - prev) / Math.abs(prev) * 1000) / 10 : 0;
  return {val: Math.round(latest * 100) / 100, change: change};
}

function renderFabList(country, chIdx) {
  if (chIdx === undefined) chIdx = currentChannel;
  var el = document.getElementById('demo-fab-table');
  var ch = CHANNELS[chIdx];
  var headerHTML = '<div class="demo-fab-header">' +
    '<span><span class="en">Fab</span><span class="ko">팹</span><span class="ja">ファブ</span></span>' +
    '<span><span class="en">Status</span><span class="ko">상태</span><span class="ja">ステータス</span></span>' +
    '<span><span class="en">' + ch.labelEn.split(' ')[0] + '</span><span class="ko">' + ch.labelKo.split(' ')[0] + '</span><span class="ja">' + ch.labelJa.split(' ')[0] + '</span></span>' +
    '<span><span class="en">MoM</span><span class="ko">전월비</span><span class="ja">前月比</span></span>' +
  '</div>';
  var fabs = country === 'all' ? FABS : FABS.filter(function(f){return f.country===country;});
  var html = headerHTML;
  fabs.forEach(function(fab) {
    var statusColor, statusEn, statusKo, statusJa;
    if (fab.status === 'operating') { statusColor='var(--accent-green)'; statusEn='Operating'; statusKo='가동 중'; statusJa='稼働中'; }
    else if (fab.status === 'construction') { statusColor='var(--accent-warm)'; statusEn='Building'; statusKo='건설 중'; statusJa='建設中'; }
    else { statusColor='var(--accent)'; statusEn='Ramping'; statusKo='램프업'; statusJa='ランプアップ'; }
    var cv = getChannelVal(fab, chIdx);
    var valColor = ch.color;
    var chgColor = cv.change > 5 ? 'var(--accent-green)' : cv.change < -5 ? 'var(--accent-red)' : 'var(--fg-muted)';
    var chgStr = (cv.change > 0 ? '+' : '') + cv.change + '%';
    var idx = FABS.indexOf(fab);
    html += '<div class="demo-fab-row" data-country="' + fab.country + '" onclick="selectFab(' + idx + ')" style="cursor:pointer;">' +
      '<span>' + fab.name + '</span>' +
      '<span class="demo-status"><span class="dot" style="background:' + statusColor + ';"></span> <span class="en">' + statusEn + '</span><span class="ko">' + statusKo + '</span><span class="ja">' + statusJa + '</span></span>' +
      '<span style="color:' + valColor + ';">' + cv.val + '</span>' +
      '<span style="color:' + chgColor + ';">' + chgStr + '</span>' +
    '</div>';
  });
  el.innerHTML = html;
}

function selectFab(idx) {
  selectedFabIdx = idx;
  currentChannel = 0;
  renderChart(idx, 0);
  renderSignals(idx);
  updateChannelIndicator();
  startChannelRotation();
}

function renderSignals(idx) {
  var fab = FABS[idx];
  var nlVal = fab.nl.length > 0 ? fab.nl[fab.nl.length - 1] : 0;
  var nlChg = fab.nlChange;
  var nlChgStr = (nlChg > 0 ? '+' : '') + nlChg + '%';
  var nlChgColor = nlChg > 0 ? 'var(--accent-green)' : 'var(--accent-red)';
  document.getElementById('demo-signals').innerHTML =
    '<div style="font-size:13px;color:var(--fg-muted);margin-bottom:12px;font-weight:600;">' + fab.name + '</div>' +
    '<div class="demo-stat-card" style="margin-bottom:12px;">' +
      '<div class="demo-stat-label">VIIRS NIGHTLIGHT</div>' +
      '<div class="demo-stat-val" style="color:var(--accent);">' + nlVal + ' <span style="font-size:14px;color:' + nlChgColor + ';">' + nlChgStr + '</span></div>' +
    '</div>' +
    '<div class="demo-stat-card" style="margin-bottom:12px;">' +
      '<div class="demo-stat-label">SAR BACKSCATTER</div>' +
      '<div class="demo-stat-val" style="color:var(--accent-warm);">' + fab.sar + ' dB</div>' +
    '</div>' +
    '<div class="demo-stat-card" style="margin-bottom:12px;">' +
      '<div class="demo-stat-label">THERMAL IR</div>' +
      '<div class="demo-stat-val" style="color:#EF4444;">' + fab.thermal + '°C</div>' +
    '</div>' +
    '<div class="demo-stat-card" style="margin-bottom:12px;">' +
      '<div class="demo-stat-label">NO₂ EMISSIONS</div>' +
      '<div class="demo-stat-val" style="color:#A78BFA;">' + fab.no2 + '×10⁻⁵ mol/m²</div>' +
    '</div>' +
    '<div class="demo-stat-card">' +
      '<div class="demo-stat-label">NDVI VEGETATION</div>' +
      '<div class="demo-stat-val" style="color:#4ADE80;">' + fab.ndvi + '</div>' +
    '</div>';
}

function renderAlerts() {
  var el = document.getElementById('demo-alerts');
  if (!el) return;
  var alerts = [];
  FABS.forEach(function(fab) {
    if (fab.status === 'ramping' && fab.nlChange > 30) {
      alerts.push({fab:fab, type:'milestone', icon:'📊', color:'#38BDF8', bgColor:'rgba(56,189,248,0.08)', borderColor:'rgba(56,189,248,0.2)',
        en:'Ramp-up +' + fab.nlChange + '%', ko:'램프업 +' + fab.nlChange + '%',
        detailEn:'Strong ramp-up signal', detailKo:'강한 램프업 신호', ja:'ランプアップ +' + fab.nlChange + '%', detailJa:'強いランプアップのシグナル'});
    } else if (fab.nlChange < -15) {
      alerts.push({fab:fab, type:'critical', icon:'⚠', color:'#EF4444', bgColor:'rgba(239,68,68,0.08)', borderColor:'rgba(239,68,68,0.2)',
        en:'Nightlight drop ' + fab.nlChange + '%', ko:'야간조명 ' + fab.nlChange + '% 하락',
        detailEn:'Possible utilization cut', detailKo:'가동률 하락 가능성', ja:'夜間光 ' + fab.nlChange + '% 低下', detailJa:'稼働率低下の可能性'});
    } else if (fab.status === 'construction' && fab.nlChange > 25) {
      alerts.push({fab:fab, type:'progress', icon:'⚡', color:'#FBBF24', bgColor:'rgba(245,158,11,0.08)', borderColor:'rgba(245,158,11,0.2)',
        en:'Construction +' + fab.nlChange + '%', ko:'건설 진척 +' + fab.nlChange + '%',
        detailEn:'Ahead of schedule', detailKo:'일정 앞섬', ja:'建設進捗 +' + fab.nlChange + '%', detailJa:'予定より前倒し'});
    }
  });
  var stableFabs = FABS.filter(function(f){return Math.abs(f.nlChange)<3 && f.status==='operating';});
  if (stableFabs.length > 0) {
    var sf = stableFabs[0];
    alerts.push({fab:sf, type:'stable', icon:'✓', color:'#4ADE80', bgColor:'rgba(34,197,94,0.08)', borderColor:'rgba(34,197,94,0.2)',
      en:'Stable at ' + (sf.nl.length > 0 ? sf.nl[sf.nl.length-1] : 0).toFixed(0), ko:(sf.nl.length > 0 ? sf.nl[sf.nl.length-1] : 0).toFixed(0) + ' 안정 가동',
      detailEn:'No change', detailKo:'변동 없음', ja:(sf.nl.length > 0 ? sf.nl[sf.nl.length-1] : 0).toFixed(0) + 'で安定稼働', detailJa:'変化なし'});
  }
  // 2026-11-20: 데모 알림은 모의 수치라 실명 대신 익명 예시로 표시
  var CN = {kr:['Korea','한국','韓国'], tw:['Taiwan','대만','台湾'], us:['USA','미국','米国'], cn:['China','중국','中国'], jp:['Japan','일본','日本'], eu:['EU','EU','EU'], sg:['Singapore','싱가포르','シンガポール']};
  var html = '<div style="display:flex;flex-direction:column;gap:8px;">';
  alerts.slice(0, 5).forEach(function(a, ai) {
    var c = CN[a.fab.country] || ['', '', ''], L = String.fromCharCode(65 + ai);
    var anon = '<span class="en">[Example] Fab ' + L + (c[0] ? ' (' + c[0] + ')' : '') + '</span><span class="ko">[예시] 팹 ' + L + (c[1] ? ' (' + c[1] + ')' : '') + '</span><span class="ja">［例］ファブ' + L + (c[2] ? '（' + c[2] + '）' : '') + '</span>';
    html += '<div style="padding:10px 12px;background:' + a.bgColor + ';border:1px solid ' + a.borderColor + ';border-radius:8px;font-size:13px;">' +
      '<div style="color:' + a.color + ';font-weight:600;margin-bottom:2px;">' + a.icon + ' ' + anon + ' — <span class="en">' + a.en + '</span><span class="ko">' + a.ko + '</span><span class="ja">' + a.ja + '</span></div>' +
      '<div style="color:#94A3B8;font-size:11px;">2026-11 · <span class="en">' + a.detailEn + '</span><span class="ko">' + a.detailKo + '</span><span class="ja">' + a.detailJa + '</span></div>' +
    '</div>';
  });
  html += '</div>';
  el.innerHTML = html;
}

// ── Live data fetch (GitHub Pages 배포 시 GEE 파이프라인 JSON 연동) ──
var LIVE_DATA_URL = '/fabwatch_data.json';

function applyLiveData(data) {
  if (!data || !data.fabs || data.fabs.length === 0) return false;
  FABS = data.fabs.map(function(f) {
    var nl = [], nlChange = 0;
    var ch = f.channels || {};
    if (ch.nightlight && ch.nightlight.length > 0) {
      nl = ch.nightlight.map(function(p) {
        var v = p.properties ? p.properties.value : p.value;
        return v != null ? Math.round(v * 10) / 10 : 0;
      });
      if (nl.length >= 2 && nl[0] > 0) {
        var nlPrev = nl.length >= 2 ? nl[nl.length - 2] : nl[0];
        nlChange = nlPrev !== 0 ? Math.round((nl[nl.length - 1] - nlPrev) / Math.abs(nlPrev) * 1000) / 10 : 0;
      }
    }
    var sarVals = (ch.sar || []).map(function(p) {
      return p.properties ? p.properties.value : p.value;
    }).filter(function(v) { return v != null; });
    var thermalVals = (ch.thermal || []).map(function(p) {
      return p.properties ? p.properties.value : p.value;
    }).filter(function(v) { return v != null; });
    var no2Vals = (ch.no2 || []).map(function(p) {
      return p.properties ? p.properties.value : p.value;
    }).filter(function(v) { return v != null; });
    var ndviVals = (ch.ndvi || []).map(function(p) {
      return p.properties ? p.properties.value : p.value;
    }).filter(function(v) { return v != null; });
    var sarArr = (ch.sar || []).map(function(p) {
      var v = p.properties ? p.properties.value : p.value;
      return v != null ? Math.round(v * 10) / 10 : null;
    }).filter(function(v) { return v != null; });
    var thermalArr = (function() {
      var raw = (ch.thermal || []).map(function(p) {
        var props = p.properties || p;
        return {date: (props.date || '').substring(0, 7), value: props.value};
      }).filter(function(r) { return r.value != null && r.date; });
      var byMonth = {};
      raw.forEach(function(r) {
        if (!byMonth[r.date]) byMonth[r.date] = [];
        byMonth[r.date].push(r.value);
      });
      var months = Object.keys(byMonth).sort();
      return months.map(function(m) {
        var vals = byMonth[m];
        return Math.round(vals.reduce(function(a,b){return a+b;},0) / vals.length * 10) / 10;
      });
    })();
    var no2Arr = (ch.no2 || []).map(function(p) {
      var v = p.properties ? p.properties.value : p.value;
      return v != null ? Math.round(v * 1e7) / 100 : null;
    }).filter(function(v) { return v != null; });
    var ndviArr = (ch.ndvi || []).map(function(p) {
      var v = p.properties ? p.properties.value : p.value;
      return v != null ? Math.round(v * 1000) / 1000 : null;
    }).filter(function(v) { return v != null; });
    return {
      id: f.id, name: f.name, company: f.company, country: f.country.toLowerCase(),
      status: f.status, score: f.composite_score || 0,
      nl: nl,
      sarArr: sarArr, thermalArr: thermalArr, no2Arr: no2Arr, ndviArr: ndviArr,
      sar: sarVals.length > 0 ? Math.round(sarVals[sarVals.length - 1] * 10) / 10 : 0,
      thermal: thermalVals.length > 0 ? Math.round(thermalVals[thermalVals.length - 1] * 10) / 10 : 0,
      no2: no2Vals.length > 0 ? Math.round(no2Vals[no2Vals.length - 1] * 100000) / 10 : 0,
      ndvi: ndviVals.length > 0 ? Math.round(ndviVals[ndviVals.length - 1] * 1000) / 1000 : 0,
      nlChange: nlChange
    };
  });
  console.log('[FabWatch] Live data loaded:', FABS.length, 'fabs from GEE pipeline');
  if (data.datacenters && data.datacenters.length > 0) {
    console.log('[FabWatch] DC data available:', data.datacenters.length, 'sites');
  }
  return true;
}

function initDemoData() {
  fetch(LIVE_DATA_URL).then(function(r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function(data) {
    applyLiveData(data);
    renderDemoData();
  }).catch(function() {
    console.log('[FabWatch] Live data not available, using embedded sample data');
    renderDemoData();
  });
}

// Chart bar animation on scroll
(function() {
  var bars = document.getElementById('demo-chart-bars');
  if (!bars) return;
  var observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
      initDemoData();
      observer.disconnect();
    }
  }, { threshold: 0.3 });
  observer.observe(bars);
})();
