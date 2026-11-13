"""
FabWatch 데모 데이터 생성기
===========================
GEE 인증 없이 현실적인 시뮬레이션 데이터를 생성하여
홈페이지 연동 테스트에 사용.

각 팹의 status에 따라 다른 위성 시그널 패턴을 생성:
  - operating: 높은 야간조명, 안정적 열방출, 낮은 NDVI
  - construction: 낮은 야간조명, SAR 변화 큼, NDVI 급감
  - ramping: 야간조명 상승 추세, 열방출 증가
"""

import json
import os
import math
import random
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FAB_FILE = os.path.join(SCRIPT_DIR, "fab_coordinates.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fabwatch_data.json")

random.seed(42)

def load_fabs():
    with open(FAB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["fabs"]

def month_range(n=12):
    """최근 12개월 YYYY-MM 리스트."""
    now = datetime.now()
    months = []
    for i in range(n - 1, -1, -1):
        y = now.year
        m = now.month - i
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y:04d}-{m:02d}")
    return months

def add_noise(base, pct=0.08):
    return base * (1 + random.uniform(-pct, pct))

def generate_channels(fab, months):
    """팹 status에 따라 6채널 시뮬레이션 데이터 생성."""
    status = fab["status"]
    lat = fab["lat"]
    channels = {}

    # 위도 기반 기본 열 보정 (적도 가까울수록 높음)
    lat_factor = 1.0 - abs(lat - 25) / 50

    # ── Ch1: VIIRS 야간조명 (nW/cm2/sr) ──
    if status == "operating":
        base = random.uniform(30, 80)
        nl = [{"properties": {"date": m, "value": round(add_noise(base + 5 * math.sin(i * 0.5)), 2)}} for i, m in enumerate(months)]
    elif status == "construction":
        base = random.uniform(3, 12)
        nl = [{"properties": {"date": m, "value": round(add_noise(base + i * 0.3), 2)}} for i, m in enumerate(months)]
    elif status == "ramping":
        base = random.uniform(15, 35)
        nl = [{"properties": {"date": m, "value": round(add_noise(base + i * 3.5), 2)}} for i, m in enumerate(months)]
    else:
        base = random.uniform(20, 50)
        nl = [{"properties": {"date": m, "value": round(add_noise(base), 2)}} for i, m in enumerate(months)]
    channels["nightlight"] = nl

    # ── Ch2: SAR VV (dB) ──
    if status == "construction":
        base = random.uniform(-14, -10)
        sar = [{"properties": {"date": m, "value": round(add_noise(base + i * 0.2, 0.05), 2)}} for i, m in enumerate(months)]
    else:
        base = random.uniform(-12, -7)
        sar = [{"properties": {"date": m, "value": round(add_noise(base, 0.03), 2)}} for i, m in enumerate(months)]
    channels["sar"] = sar

    # ── Ch3: 열적외선 (°C) ──
    if status == "operating":
        base_temp = 28 + lat_factor * 15
        thermal = [{"properties": {"date": m, "value": round(add_noise(base_temp + 8 * math.sin((i - 3) * math.pi / 6), 0.06), 1)}} for i, m in enumerate(months)]
    elif status == "construction":
        base_temp = 20 + lat_factor * 10
        thermal = [{"properties": {"date": m, "value": round(add_noise(base_temp + 6 * math.sin((i - 3) * math.pi / 6), 0.08), 1)}} for i, m in enumerate(months)]
    else:
        base_temp = 24 + lat_factor * 12
        thermal = [{"properties": {"date": m, "value": round(add_noise(base_temp + i * 0.8, 0.06), 1)}} for i, m in enumerate(months)]
    channels["thermal"] = thermal

    # ── Ch4: NO2 (mol/m2, ×10^-5) ──
    if status == "operating":
        base_no2 = random.uniform(4.0, 9.0)
        no2 = [{"properties": {"date": m, "value": round(add_noise(base_no2 + math.sin(i * 0.3) * 1.2, 0.1) * 1e-5, 8)}} for i, m in enumerate(months)]
    elif status == "construction":
        base_no2 = random.uniform(1.5, 3.0)
        no2 = [{"properties": {"date": m, "value": round(add_noise(base_no2 + i * 0.15, 0.12) * 1e-5, 8)}} for i, m in enumerate(months)]
    else:
        base_no2 = random.uniform(3.0, 6.0)
        no2 = [{"properties": {"date": m, "value": round(add_noise(base_no2 + i * 0.3, 0.1) * 1e-5, 8)}} for i, m in enumerate(months)]
    channels["no2"] = no2

    # ── Ch5: NDVI ──
    if status == "operating":
        ndvi = [{"properties": {"date": m, "value": round(add_noise(0.15 + 0.05 * math.sin(i * math.pi / 6), 0.1), 3)}} for i, m in enumerate(months)]
    elif status == "construction":
        base_ndvi = random.uniform(0.35, 0.55)
        ndvi = [{"properties": {"date": m, "value": round(max(0.05, add_noise(base_ndvi - i * 0.025, 0.08)), 3)}} for i, m in enumerate(months)]
    else:
        ndvi = [{"properties": {"date": m, "value": round(add_noise(0.18, 0.1), 3)}} for i, m in enumerate(months)]
    channels["ndvi"] = ndvi

    # ── Ch6: 광학 (썸네일 URL 대신 마지막 촬영일) ──
    channels["optical"] = {"date": months[-1] + "-15", "thumbnail_url": None}

    return channels

def compute_score(channels, status):
    """간이 복합 스코어 (0-100)."""
    scores = []

    # 야간조명 안정도 → 가동 점수
    nl_vals = [f["properties"]["value"] for f in channels["nightlight"]]
    if nl_vals:
        latest = nl_vals[-1]
        avg = sum(nl_vals) / len(nl_vals)
        if avg > 0:
            stability = min(100, (latest / avg) * 65 + 15)
            scores.append(stability)

    # SAR 안정도 (건설 중이면 변동 클수록 진행 중)
    sar_vals = [f["properties"]["value"] for f in channels["sar"]]
    if len(sar_vals) >= 2:
        sar_range = max(sar_vals) - min(sar_vals)
        if status == "construction":
            scores.append(min(100, sar_range * 15 + 40))
        else:
            scores.append(max(0, 90 - sar_range * 10))

    # 열 활성도
    th_vals = [f["properties"]["value"] for f in channels["thermal"]]
    if th_vals:
        latest_th = th_vals[-1]
        if status == "operating":
            scores.append(min(100, latest_th * 2))
        else:
            scores.append(min(100, latest_th * 1.5))

    if scores:
        return round(sum(scores) / len(scores), 1)
    return 50.0

def load_datacenters():
    with open(FAB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("datacenters", [])


def main():
    fabs = load_fabs()
    datacenters = load_datacenters()
    months = month_range(12)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = {
        "generated": datetime.now().isoformat(),
        "period": {"start": months[0] + "-01", "end": months[-1] + "-28"},
        "source": "simulation",
        "note": "Demo data generated from realistic satellite signal patterns. Replace with GEE fetch for production.",
        "fabs": [],
        "datacenters": []
    }

    print("=== Semiconductor Fabs ===")
    for fab in fabs:
        channels = generate_channels(fab, months)
        score = compute_score(channels, fab["status"])
        results["fabs"].append({
            "id": fab["id"], "name": fab["name"], "company": fab["company"],
            "country": fab["country"], "lat": fab["lat"], "lng": fab["lng"],
            "status": fab["status"], "composite_score": score, "channels": channels
        })
        print(f"  {fab['name']:40s} score={score:5.1f}  status={fab['status']}")

    print("\n=== AI Data Centers ===")
    for dc in datacenters:
        channels = generate_channels(dc, months)
        score = compute_score(channels, dc["status"])
        entry = {
            "id": dc["id"], "name": dc["name"], "company": dc["company"],
            "country": dc["country"], "lat": dc["lat"], "lng": dc["lng"],
            "status": dc["status"], "composite_score": score, "channels": channels
        }
        if "power_mw" in dc:
            entry["power_mw"] = dc["power_mw"]
        if "capex_b" in dc:
            entry["capex_b"] = dc["capex_b"]
        results["datacenters"].append(entry)
        print(f"  {dc['name']:40s} score={score:5.1f}  status={dc['status']}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    fab_count = len(results["fabs"])
    dc_count = len(results["datacenters"])
    print(f"\n[DONE] {OUTPUT_FILE}")
    print(f"       {fab_count}개 팹 + {dc_count}개 DC × 6채널 × 12개월 데모 데이터 생성 완료")

if __name__ == "__main__":
    main()
