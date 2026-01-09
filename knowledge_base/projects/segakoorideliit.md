---
type: project
id: segakoorideliit-ee
title: "Eesti Segakooride Liit (esl)"
url: https://segakoorideliit.ee
repository: https://github.com/aivotoots/esl
organization: "Eesti Segakooride Liit"
organizationEt: "Eesti Segakooride Liit"
description: "Co-developed the official web platform for the Estonian Mixed Choirs Union. A static site generated from Strapi CMS content, facilitating event calendars, member registries, and secure document management for choir conductors nationwide."
descriptionEt: "Kaasarendasin Eesti Segakooride Liidu ametliku veebiplatvormi. Tegemist on Strapi CMS-i põhiselt genereeritud staatilise lehega, mis haldab sündmuste kalendrit, liikmeregistrit ja dokumentide turvalist jagamist koorijuhtidele."
dates:
  start: 2019
  end: present
  status: active
roles:
  - title: "Architect & Technical Contributor"
    dates: "2019-present"
    description: "Bootstrapped the initial system architecture and SSG pipeline. Currently serving as an occasional contributor to ensure continuity when the lead developer is unavailable."
context:
  - "Collaborative project to modernize the digital presence of the Estonian Mixed Choirs Union"
  - "Built to replace legacy systems with a maintainable, high-performance static site"
technologies:
  - "Pug (66.7%)"
  - "JavaScript (14.4%)"
  - "Stylus (12.2%)"
  - "Strapi CMS"
  - "Entu SSG"
  - "GitHub Actions"
features:
  - "Event Calendar (Tulevased kontserdid)"
  - "Document Registry (Dokumendid)"
  - "Member Registry (Liikmed)"
  - "Multilingual support (EST/ENG)"
tags:
  - "web-development"
  - "static-site-generator"
  - "cultural-organization"
  - "mentorship"
  - "open-source"
  - "pug"
  - "stylus"
skills:
  - "system-architecture"
  - "frontend-development"
  - "technical-mentoring"
  - "cms-integration"
repo_stats:
  contributors: 2
  languages: ["Pug", "JavaScript", "Stylus"]
---

## Overview

The official website for **Eesti Segakooride Liit (ESL)** serves as the central information hub for mixed choirs across Estonia. It manages crucial operational data including the annual event calendar, choir registry, and distribution of sheet music and guidelines for conductors.

**My Role:**
I bootstrapped the initial system architecture and established the static site generation pipeline using Entu/Strapi. Currently, I contribute occasionally to support the lead developer (Aivo Toots), stepping in to handle updates or maintenance when he is unavailable.

## Technical Architecture

The project utilizes a JAMstack approach for reliability, security, and performance:

-   **Content Source:** Strapi CMS (headless) managing dynamic content like events and news.
-   **Build Process:** Static site generation (Entu SSG) transforming CMS data into static files.
-   **Templating:** Pug for concise, readable HTML structure.
-   **Styling:** Stylus for modular and maintainable CSS.
-   **Deployment:** GitHub Actions pipeline automatig builds and deployment.

**Key Contributions:**
-   Designed the initial project structure and build workflow.
-   Implemented the integration logic between the headless CMS and the static generator.
-   Provided ongoing code reviews and technical problem-solving support.

## Related Projects

[[kgs21]] — Similar backend architecture and consultation role.
[[saal-ee]] — Experience with cultural organization web platforms.
