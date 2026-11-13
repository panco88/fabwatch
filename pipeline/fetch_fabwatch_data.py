"""
FabWatch Data Pipeline — GEE 기반 6채널 위성 데이터 수집 프로토타입
=================================================================
6개 위성 채널에서 팹 좌표별 시계열 데이터를 수집하여 JSON으로 출력.
홈페이지 대시보드가 이 JSON을 fetch하여 라이브 데이터로 렌더링.

사용법:
  1. pip install earthengine-api
  2. earthengine authenticate  (최초 1회)
  3. python fetch_fabwatch_data.py

출력: output/fabwatch_data.json
"""

import ee
import json
import os
import sys
from datetime import datetime, timedelta

# ── 설정 ──────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FAB_FILE = os.path.join(SCRIPT_DIR, "fab_coordinates.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fabwatch_data.json")

# 최근 12개월 기간
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365)
DATE_FMT = "%Y-%m-%d"

# 팹 주변 버퍼 크기 (미터)
BUFFER_M = 500


def init_gee():
    """GEE 초기화. 인증이 안 되어 있으면 안내 메시지 출력."""
    try:
        ee.Initialize(opt_url="https://earthengine-highvolume.googleapis.com")
        print("[OK] GEE 초기화 성공")
    except Exception as e:
        print(f"[!] GEE 초기화 실패: {e}")
        print("    먼저 'earthengine authenticate'를 실행하세요.")
        sys.exit(1)


def load_fabs():
    """팹 좌표 JSON 로드."""
    with open(FAB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[OK] {len(data['fabs'])}개 팹 좌표 로드")
    return data["fabs"]


def load_datacenters():
    """데이터센터 좌표 JSON 로드."""
    with open(FAB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    dcs = data.get("datacenters", [])
    print(f"[OK] {len(dcs)}개 데이터센터 좌표 로드")
    return dcs


def make_region(lat, lng, buffer_m=BUFFER_M):
    """팹 좌표를 중심으로 정사각형 버퍼 영역 생성."""
    point = ee.Geometry.Point([lng, lat])
    return point.buffer(buffer_m).bounds()


# ── 채널별 데이터 추출 함수 ──────────────────────────────────

def fetch_nightlight(region, start, end):
    """Ch1: VIIRS DNB 야간조명 (월별 평균 radiance)."""
    col = (ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")
           .filterDate(start, end)
           .select("avg_rad"))

    def extract(img):
        val = img.reduceRegion(ee.Reducer.mean(), region, 500)
        return ee.Feature(None, {
            "date": img.date().format("YYYY-MM"),
            "value": val.get("avg_rad")
        })

    return col.map(extract).getInfo()["features"]


def fetch_sar(region, start, end):
    """Ch2: Sentinel-1 SAR VV 백스캐터 (월별 평균 dB)."""
    col = (ee.ImageCollection("COPERNICUS/S1_GRD")
           .filterBounds(region)
           .filterDate(start, end)
           .filter(ee.Filter.eq("instrumentMode", "IW"))
           .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
           .select("VV"))

    months = ee.List.sequence(0, 11)
    start_date = ee.Date(start)

    def monthly_mean(m):
        m = ee.Number(m)
        s = start_date.advance(m, "month")
        e = s.advance(1, "month")
        monthly = col.filterDate(s, e).mean()
        val = monthly.reduceRegion(ee.Reducer.mean(), region, 10)
        return ee.Feature(None, {
            "date": s.format("YYYY-MM"),
            "value": val.get("VV")
        })

    return months.map(monthly_mean).getInfo()


def fetch_thermal(region, start, end):
    """Ch3: Landsat 8/9 열적외선 표면온도 (°C)."""
    col = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
           .merge(ee.ImageCollection("LANDSAT/LC09/C02/T1_L2"))
           .filterBounds(region)
           .filterDate(start, end)
           .select("ST_B10"))

    def to_celsius(img):
        temp = img.select("ST_B10").multiply(0.00341802).add(149.0).subtract(273.15)
        val = temp.reduceRegion(ee.Reducer.mean(), region, 30)
        return ee.Feature(None, {
            "date": img.date().format("YYYY-MM-dd"),
            "value": val.get("ST_B10")
        })

    return col.map(to_celsius).getInfo()["features"]


def fetch_no2(region, start, end):
    """Ch4: Sentinel-5P TROPOMI NO2 (월별 평균, mol/m2)."""
    col = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
           .filterBounds(region)
           .filterDate(start, end)
           .select("tropospheric_NO2_column_number_density"))

    months = ee.List.sequence(0, 11)
    start_date = ee.Date(start)

    def monthly_mean(m):
        m = ee.Number(m)
        s = start_date.advance(m, "month")
        e = s.advance(1, "month")
        monthly = col.filterDate(s, e).mean()
        val = monthly.reduceRegion(ee.Reducer.mean(), region, 1000)
        return ee.Feature(None, {
            "date": s.format("YYYY-MM"),
            "value": val.get("tropospheric_NO2_column_number_density")
        })

    return months.map(monthly_mean).getInfo()


def fetch_ndvi(region, start, end):
    """Ch5: Sentinel-2 NDVI 식생지수 (월별 평균)."""
    col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
           .filterBounds(region)
           .filterDate(start, end)
           .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30)))

    months = ee.List.sequence(0, 11)
    start_date = ee.Date(start)

    def monthly_ndvi(m):
        m = ee.Number(m)
        s = start_date.advance(m, "month")
        e = s.advance(1, "month")
        monthly = col.filterDate(s, e)
        ndvi = monthly.map(lambda img: img.normalizedDifference(["B8", "B4"]).rename("ndvi")).mean()
        val = ndvi.reduceRegion(ee.Reducer.mean(), region, 10)
        return ee.Feature(None, {
            "date": s.format("YYYY-MM"),
            "value": val.get("ndvi")
        })

    return months.map(monthly_ndvi).getInfo()


def fetch_optical_latest(region, end):
    """Ch6: Sentinel-2 최신 RGB 썸네일 URL (확인용)."""
    img = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
           .filterBounds(region)
           .filterDate(ee.Date(end).advance(-30, "day"), end)
           .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
           .sort("CLOUDY_PIXEL_PERCENTAGE")
           .first())

    if img is None:
        return None

    url = img.select(["B4", "B3", "B2"]).getThumbURL({
        "region": region,
        "dimensions": "256x256",
        "min": 0, "max": 3000
    })
    date = img.date().format("YYYY-MM-dd").getInfo()
    return {"date": date, "thumbnail_url": url}


# ── 복합 스코어 계산 ────────────────────────────────────────

def compute_composite_score(channels):
    """6채널 데이터를 0-100 복합 점수로 변환 (간이 버전)."""
    scores = {}

    # 야간조명: 높을수록 가동률 높음
    nl = channels.get("nightlight", [])
    if nl:
        vals = [f["properties"]["value"] for f in nl if f["properties"]["value"] is not None]
        if vals:
            latest = vals[-1] if vals else 0
            avg = sum(vals) / len(vals) if vals else 0
            scores["nightlight"] = min(100, (latest / max(avg, 0.01)) * 70)

    # SAR: 변화량 (건설 중이면 높음)
    sar = channels.get("sar", [])
    if sar and isinstance(sar, list):
        vals = [f.get("value") or f.get("properties", {}).get("value") for f in sar if isinstance(f, dict)]
        vals = [v for v in vals if v is not None]
        if len(vals) >= 2:
            change = abs(vals[-1] - vals[0])
            scores["sar"] = min(100, change * 10 + 50)

    # 전체 복합 점수 (가중 평균)
    if scores:
        return round(sum(scores.values()) / len(scores), 1)
    return None


# ── 메인 실행 ────────────────────────────────────────────────

def collect_site(site, start, end, label="팹"):
    """팹 또는 데이터센터 1개의 6채널 데이터를 수집하여 dict 반환."""
    region = make_region(site["lat"], site["lng"])
    channels = {}

    for ch_name, ch_func, ch_label in [
        ("nightlight", fetch_nightlight, "VIIRS 야간조명"),
        ("sar", fetch_sar, "SAR 백스캐터"),
        ("thermal", fetch_thermal, "열적외선"),
        ("no2", fetch_no2, "NO2"),
        ("ndvi", fetch_ndvi, "NDVI"),
    ]:
        try:
            print(f"  {ch_label}...", end=" ", flush=True)
            channels[ch_name] = ch_func(region, start, end)
            n = len(channels[ch_name]) if isinstance(channels[ch_name], list) else 0
            print(f"OK ({n} pts)")
        except Exception as e:
            print(f"FAIL ({e})")
            channels[ch_name] = []

    try:
        print("  광학 썸네일...", end=" ", flush=True)
        channels["optical"] = fetch_optical_latest(region, end)
        print("OK" if channels["optical"] else "SKIP")
    except Exception as e:
        print(f"FAIL ({e})")
        channels["optical"] = None

    score = compute_composite_score(channels)
    print(f"  → 복합 스코어: {score}")

    result = {
        "id": site["id"],
        "name": site["name"],
        "company": site["company"],
        "country": site["country"],
        "lat": site["lat"],
        "lng": site["lng"],
        "status": site["status"],
        "composite_score": score,
        "channels": channels
    }
    if "power_mw" in site:
        result["power_mw"] = site["power_mw"]
    if "capex_b" in site:
        result["capex_b"] = site["capex_b"]
    return result


def main():
    init_gee()
    fabs = load_fabs()
    datacenters = load_datacenters()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    start = START_DATE.strftime(DATE_FMT)
    end = END_DATE.strftime(DATE_FMT)

    results = {
        "generated": datetime.now().isoformat(),
        "period": {"start": start, "end": end},
        "fabs": [],
        "datacenters": []
    }

    # 데모용: 처음 5개만 처리 (전체는 --all 플래그로)
    process_all = "--all" in sys.argv
    target_fabs = fabs if process_all else fabs[:5]
    target_dcs = datacenters if process_all else datacenters[:3]

    print(f"\n=== 반도체 팹 ({len(target_fabs)}개) ===")
    for i, fab in enumerate(target_fabs):
        print(f"\n[FAB {i+1}/{len(target_fabs)}] {fab['name']} ({fab['country']})")
        results["fabs"].append(collect_site(fab, start, end, "팹"))

    print(f"\n=== AI 데이터센터 ({len(target_dcs)}개) ===")
    for i, dc in enumerate(target_dcs):
        print(f"\n[DC {i+1}/{len(target_dcs)}] {dc['name']} ({dc.get('state', dc['country'])})")
        results["datacenters"].append(collect_site(dc, start, end, "DC"))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    fab_count = len(results["fabs"])
    dc_count = len(results["datacenters"])
    print(f"\n[DONE] {OUTPUT_FILE} 저장 완료 ({fab_count}개 팹 + {dc_count}개 DC)")
    print(f"       홈페이지에서 이 JSON을 fetch하면 라이브 데이터 대시보드 완성")


if __name__ == "__main__":
    main()
