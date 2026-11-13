# FabWatch — Satellite Intelligence for Semiconductor Fabs & AI Data Centers

FabWatch monitors **24 semiconductor fabs** and **9 AI data centers** across **7 countries** using **6 satellite channels** to track utilization, construction progress, and supply chain risks in near real-time.

**Live Demo:** [https://panco88.github.io/fabwatch/](https://panco88.github.io/fabwatch/)

## What This Is

An interactive dashboard for the FabWatch satellite monitoring platform. The dashboard visualizes multi-channel satellite signals (nightlight, SAR, thermal IR, NO2, NDVI, optical) collected via Google Earth Engine.

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
- **AI Data Centers:** Meta, OpenAI/SoftBank, Microsoft, Google, xAI, Amazon, CoreWeave

## Tech Stack

- Single-page static HTML (no framework, no build step)
- Google Earth Engine satellite data pipeline
- Bilingual: English / Korean toggle

## License

All rights reserved. This repository is shared for review and feedback purposes.

---
*DS Planet Inc.*
