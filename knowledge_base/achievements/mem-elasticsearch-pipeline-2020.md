Last updated: 2025-12-01T00:00:00+02:00

---
id: mem-elasticsearch-pipeline-2020
aliases: ["Elasticsearch real-time data pipeline for memoriaal.ee and wwii-refugees.ee"]
type: achievement
parent_experience: eesti-malu-instituut-2017-2024
title:
  et: Elasticsearch reaalajas andmepublikatsiooni süsteemi loomine
  en: Elasticsearch real-time data publication system
description:
  et: Disainisin ja implementeerisin reaalajas andmepublikatsiooni süsteemi Elasticsearch'i baasil, võimaldades memoriaal.ee ja wwii-refugees.ee veebilehtedel pakkuda ajaloolisi andmeid viie minuti viivitusega. Süsteem hõlmas isoleeritud töökeskkondi ja teenindas 100 000+ kirjet.
  en: Designed and implemented a real-time data publication system based on Elasticsearch, enabling memoriaal.ee and wwii-refugees.ee websites to serve historical data with 5-minute latency. System included isolated work environments and served 100,000+ records.
tags: [data-pipeline, elasticsearch, docker, python, architecture, devops, real-time-systems]
technologies: [Elasticsearch, Docker, Python, JavaScript, DigitalOcean]
date: '2020'
status: verified
last_verified: '2025-12-01'
---

## et

### Väljakutse

Eesti Mälu Instituudis oli vaja tagada, et ajaloolised andmed oleksid veebilehtedel memoriaal.ee ja wwii-refugees.ee kättesaadavad võimalikult kiiresti pärast nende uuendamist. Samuti oli oluline eraldada töökeskkonnad, et tagada andmete kvaliteet ja turvaline arendusprotsess.

### Lahendus

Disainisin ja implementeerisin täieliku andmepublikatsiooni torujuhtme (data pipeline):

- **Andmebaas:** Elasticsearch
- **Deployment:** Docker konteinerid DigitalOcean'is
- **Andmete üleslaadimine:** Kohandatud Python skriptid
- **Andmete kuvamine:** JavaScript-põhine lugemine veebilehtedel
- **Uuendussagedus:** Reaalajas publikatsioon iga 5 minuti järel
- **Isoleeritud keskkonnad:** Eraldi arendus-, test- ja tootmiskeskkonnad

### Tulemus

- **100 000+ kirjet** pidevalt kättesaadavad
- **Reaalajas publikatsioon:** Andmete uuendused veebis nähtavad 5 minuti jooksul
- **Isoleeritud töökeskkonnad:** Turvaline ja kontrollitud arendusprotsess
- **Skaleeritav arhitektuur:** Docker-põhine lahendus võimaldab lihtsat skaleerimist

## en

### Challenge

At the Estonian Memory Institute, we needed to ensure that historical data on memoriaal.ee and wwii-refugees.ee websites would be available as quickly as possible after updates. It was also important to isolate work environments to ensure data quality and secure development processes.

### Solution

I designed and implemented a complete data publication pipeline:

- **Database:** Elasticsearch
- **Deployment:** Docker containers on DigitalOcean
- **Data Upload:** Custom Python scripts
- **Data Display:** JavaScript-based read-only access from web pages
- **Update Frequency:** Real-time publication every 5 minutes
- **Isolated Environments:** Separate development, testing, and production environments

### Result

- **100,000+ records** continuously available
- **Real-time publication:** Data updates visible on websites within 5 minutes
- **Isolated work environments:** Secure and controlled development process
- **Scalable architecture:** Docker-based solution enables easy scaling

---

## Connections

- **Parent Experience:** [[eesti-malu-instituut-2017-2024]]
- **Skills:** [[python]], [[database-management]], [[system-architecture]]
- **Technologies:** Elasticsearch, Docker, Python, JavaScript, DigitalOcean
