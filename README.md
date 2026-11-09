# FabWatch — Satellite Intelligence for Semiconductor Fabs

FabWatch monitors **66 semiconductor fabs** across **7 countries** using **6 satellite channels** to track utilization, construction progress, and supply chain risks in near real-time.

## What This Is

A concept homepage and interactive demo dashboard for the FabWatch satellite monitoring platform. The dashboard visualizes multi-channel satellite signals (nightlight, SAR, thermal IR, NO2, NDVI, optical) for 24 representative fabs.

> **Note:** The dashboard currently uses **simulated demo data**, not live satellite measurements. The data patterns are modeled after realistic satellite signal behaviors for each fab status (operating, construction, ramping).

## Satellite Channels

| Channel | Source | What It Measures |
|---|---|---|
| VIIRS Nightlight | Suomi NPP | Fab utilization via light output |
| Sentinel-1 SAR | ESA Copernicus | Construction activity / structural changes |
| Landsat Thermal IR | NASA/USGS | Heat emissions from active fabs |
| Sentinel-5P NO2 | ESA Copernicus | Industrial activity indicator |
| Sentinel-2 NDVI | ESA Copernicus | Land use change / greenfield conversion |
| Sentinel-2 Optical | ESA Copernicus | Visual confirmation |

## Coverage

- **Countries:** South Korea, Taiwan, China, USA, Japan, EU, Singapore
- **Companies:** TSMC, Intel, SK hynix, Samsung, Micron, SMIC, YMTC, CXMT, Infineon, GlobalFoundries, STMicro, UMC

## Tech Stack

- Single-page static HTML (no framework, no build step)
- Google Fonts (Noto Sans KR, Outfit, IBM Plex Sans/Mono)
- Bilingual: English / Korean toggle
- Google Earth Engine pipeline planned for production data

## Feedback Welcome

This project is in its early concept stage. If you work in:
- Semiconductor supply chain analysis
- Satellite remote sensing / Earth observation
- Investment research (semiconductor sector)
- Geopolitical risk assessment

I'd love to hear your thoughts. Please open an [Issue](../../issues) to share ideas, suggestions, or potential use cases.

## License

All rights reserved. This repository is shared for review and feedback purposes.
