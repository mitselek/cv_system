---
docID: CLOUDFLARE-OVERVIEW
version: 1.0
date: 2025-12-11
author: Mihkel Putrinš
company: Eesti Raudtee AS
purpose: Eesti Raudtee tech stack (Cloudflare D1, Workers, Pages)
---

# Cloudflare Developer Platform: Kiire Ülevaade

## Mis on Cloudflare?

**Cloudflare Developer Platform** on serverless edge computing platvorm, mis võimaldab ehitada ja deployida rakendusi 330+ globaalses asukohas ilma serveri haldamiseta.

**Peamine väärtus:** Zero operational overhead + globaalne performance + scalability

---

## Põhitooted Eesti Raudtee Kontekstis

### 1. Cloudflare Workers (Serverless Compute)

**Mis see on:**

- JavaScript/TypeScript kood, mis töötab "edge'il" (globaalses võrgus)
- Sarnane AWS Lambda'le, aga kiirem (ei ole cold start'e)
- Automaatselt deployed kõigis 330+ lokatsioonis

**Kasutusjuhtumid:**

- API endpoints (nagu Express.js serveris)
- Backend logic
- Authentication/authorization
- Data validation
- Middleware

**Näide:**

```javascript
export default {
  async fetch(request) {
    return new Response("Hello from Cloudflare Workers!");
  },
};
```

**Võrdlus:**

- **AWS Lambda:** Cold start, piirkonnaspetsiifiline
- **Cloudflare Workers:** Instant start, globaalne

---

### 2. Cloudflare D1 (SQL Database)

**Mis see on:**

- SQLite-based distributed SQL database
- Töötab edge'il (kiire access globaalselt)
- SQL queries nagu PostgreSQL/MySQL

**Eesti Raudtee kontekst:**

- Job posting mainitakse: "PostgreSQL, Oracle, **Cloudflare D1**"
- D1 on täiendav/alternatiivne DB edge use case'ide jaoks

**Näide:**

```javascript
const { results } = await env.DB.prepare("SELECT * FROM users WHERE id = ?")
  .bind(userId)
  .all();
```

**Võrdlus teiste DB'dega:**

| Database | Asukoht | Latency | Use Case |
|----------|---------|---------|----------|
| PostgreSQL | Keskne server | Kõrgem | Core business data |
| Cloudflare D1 | Edge (global) | Väga madal | Session data, cache, user prefs |
| Oracle | Keskne server | Kõrgem | Legacy enterprise data |

**Millal kasutada D1:**

- Kiire read access (session data, user settings)
- Global distributed data
- Caching layer
- Mitte: Complex transactions, large writes

---

### 3. Cloudflare Pages (Frontend Hosting)

**Mis see on:**

- Static site hosting + serverless functions
- Sarnane Netlify, Vercel'ile
- Automaatne deploy Git'ist
- **Ideaalne SvelteKit'ile!**

**Kasutusjuhtumid:**

- SvelteKit rakenduse hosting
- Static assets (HTML, CSS, JS, images)
- Serverless API routes (Pages Functions)

**Eesti Raudtee kontekst:**

- SvelteKit frontend → Cloudflare Pages
- Automaatne CDN (content delivery network)
- HTTPS by default

**Workflow:**

```text
Git push → Cloudflare build → Deploy globally → Live in seconds
```

---

## Cloudflare vs Traditsiooniline Stack

### Traditsiooniline (Eesti Raudtee legacy):

```text
Frontend (Svelte) → Nginx → Backend (Java Spring Boot) → PostgreSQL/Oracle
                                      ↓
                              Hosted on VM/server
```

### Cloudflare approach:

```text
Frontend (SvelteKit on Pages) → Workers (API/logic) → D1 + PostgreSQL
              ↓                         ↓                    ↓
        Global CDN              Global edge          Central DB
```

**Hybrid approach (tõenäoline Eesti Raudteel):**

- **Cloudflare Pages:** SvelteKit frontend
- **Cloudflare Workers:** API gateway, authentication, caching
- **Spring Boot:** Core business logic (existing)
- **PostgreSQL/Oracle:** Master data
- **Cloudflare D1:** Edge cache, session data

---

## Peamised Mõisted

### Edge Computing

- Kood töötab "edge'il" (lähedal kasutajale), mitte keskses serveris
- Väiksem latency, kiirem vastus
- Cloudflare network: 330+ cities globally

### Serverless

- Ei pea haldama servereid
- Auto-scaling (zero → millions requests)
- Maksad ainult kasutuse eest

### Workers vs Pages vs Functions

| Toode               | Mis                           | Kasutusjuhtum                  |
| ------------------- | ----------------------------- | ------------------------------ |
| **Workers**         | Pure serverless functions     | API, middleware, backend logic |
| **Pages**           | Static hosting + functions    | SvelteKit apps, websites       |
| **Pages Functions** | Serverless functions Pages'is | API routes SvelteKit'is        |

---

## SvelteKit + Cloudflare Integratsioon

**SvelteKit toetab Cloudflare natiively:**

```bash
npm create cloudflare@latest my-app -- --framework=svelte
```

**Adapter:**

```javascript
// svelte.config.js
import adapter from "@sveltejs/adapter-cloudflare";

export default {
  kit: {
    adapter: adapter(),
  },
};
```

**API routes SvelteKit'is → Cloudflare Workers:**

```javascript
// src/routes/api/data/+server.js
export async function GET({ platform }) {
  const { results } = await platform.env.DB.prepare("SELECT * FROM data").all();

  return json(results);
}
```

**Deployment:**

- Git push → automatic build → global deploy
- Environment variables Cloudflare dashboard'is
- Rollback one-click

---

## Õppimisressursid

### 1. Cloudflare Workers Tutorial (alusta siit)

**URL:** https://developers.cloudflare.com/workers/get-started/guide/

**Mida õpid:**

- Workers fundamentals
- Request/Response handling
- Environment variables
- Deploy workflow

**Aeg:** 30 min

### 2. Cloudflare D1 Tutorial

**URL:** https://developers.cloudflare.com/d1/get-started/

**Mida õpid:**

- D1 database creation
- SQL queries Workers'is
- Migrations
- Local development

**Aeg:** 30 min

### 3. SvelteKit + Cloudflare

**URL:** https://developers.cloudflare.com/pages/framework-guides/deploy-a-svelte-site/

**Mida õpid:**

- SvelteKit deployment Cloudflare Pages'is
- Adapter configuration
- Environment bindings
- API routes

**Aeg:** 45 min

### 4. Full-Stack SvelteKit Reference Architecture

**URL:** https://developers.cloudflare.com/reference-architecture/diagrams/serverless/fullstack-application/

**Mida õpid:**

- Complete architecture patterns
- Best practices
- Integration examples

**Aeg:** 1 tund

---

## Kiire Start Plaan (Eesti Raudtee kontekstis)

### Päev 1: Workers Basics (2-3 tundi)

1. ✅ Cloudflare account (free tier)
2. ✅ Workers "Hello World"
3. ✅ Deploy first worker
4. ✅ Environment variables
5. ✅ Request/response handling

### Päev 2: D1 Database (2-3 tundi)

1. ✅ Create D1 database
2. ✅ Run SQL queries from Workers
3. ✅ Migrations
4. ✅ CRUD operations

### Päev 3: SvelteKit + Pages (3-4 tundi)

1. ✅ SvelteKit app with Cloudflare adapter
2. ✅ Deploy to Pages
3. ✅ API routes (Pages Functions)
4. ✅ Connect to D1 from SvelteKit

### Päev 4: Integration Patterns (2-3 tundi)

1. ✅ Workers kui API gateway
2. ✅ Caching strategies
3. ✅ Authentication flow
4. ✅ Connect to external APIs (Spring Boot backend)

**Kokku:** ~10-13 tundi praktikaga kurssi viimiseks

---

## Võrdlus Teiste Platvormidega

| Feature               | AWS (Lambda + API Gateway + RDS) | Vercel        | Cloudflare                    |
| --------------------- | -------------------------------- | ------------- | ----------------------------- |
| **Cold Start**        | 100-500ms                        | 50-200ms      | <1ms                          |
| **Global Network**    | Piirkonnaspetsiifiline           | CDN edge      | 330+ cities                   |
| **SQL Database**      | RDS (regional)                   | Neon/Supabase | D1 (edge)                     |
| **Pricing**           | Complex (Lambda + Gateway + RDS) | Simpler       | Simplest (generous free tier) |
| **SvelteKit Support** | Adapter available                | Native (best) | Native (good)                 |
| **Learning Curve**    | Steep                            | Medium        | Low                           |

**Cloudflare eelised:**

- ✅ Fastest performance (no cold starts)
- ✅ Simplest pricing
- ✅ Generous free tier (Workers: 100k requests/day, Pages: unlimited)
- ✅ Excellent SvelteKit integration

**Cloudflare piirangud:**

- ❌ D1 on veel beetas (actively developed)
- ❌ Workers CPU time limit (50ms free tier, 30s paid)
- ❌ Vähem mature kui AWS (aga kasvav)

---

## Praktiline Näide: Eesti Raudtee Use Case

**Stsenaarium:** Vedude jälgimise dashboard

**Arhitektuur:**

```text
User Browser
     ↓
SvelteKit Frontend (Cloudflare Pages)
     ↓
Cloudflare Workers (API Gateway + Auth)
     ↓                              ↓
D1 (Session/Cache)          Spring Boot (Core logic)
                                    ↓
                            PostgreSQL (Master data)
```

**Flow:**

1. User visits dashboard → SvelteKit (Cloudflare Pages)
2. Dashboard loads session from D1 (fast, edge)
3. Real-time updates via Workers (WebSocket/SSE)
4. Heavy queries → Spring Boot → PostgreSQL
5. Workers caches frequent queries in D1

**Miks see töötab:**

- Fast initial load (SvelteKit SSR on edge)
- Low latency for frequent operations (D1)
- Existing business logic intact (Spring Boot)
- Scalable (serverless auto-scales)

---

## Kokkuvõte: Mida Pead Teadma

### Minimaalne Teadmine (1. töönädal)

1. ✅ **Workers basics** - kuidas kirjutada ja deployida
2. ✅ **Pages deployment** - SvelteKit app Cloudflare'is
3. ✅ **Environment variables** - konfiguratsioon

### Keskmine Teadmine (1. kuu)

1. ✅ **D1 integration** - SQL queries Workers'is
2. ✅ **API routes** - SvelteKit + Workers
3. ✅ **Caching strategies** - millal D1, millal PostgreSQL

### Sügav Teadmine (3 kuud)

1. ✅ **Architecture patterns** - millal Workers, millal Spring Boot
2. ✅ **Performance optimization** - edge caching, query optimization
3. ✅ **Security** - authentication, authorization, rate limiting

---

## Intervjuu Järelkontroll

**Kui küsitakse Cloudflare kogemuse kohta:**

> "Mul ei ole veel Cloudflare kogemust, aga olen tutvunud platvormi põhimõtetega. Cloudflare Workers on serverless edge computing - sarnane AWS Lambda'le, aga kiirem (ei ole cold start'e) ja globaalselt deployed. D1 on SQLite-based edge database, mis sobib hästi cache'imiseks ja session data jaoks. SvelteKit toetab Cloudflare natiively läbi adapter'i. Olen valmis esimesel nädalal Workers ja D1 tutorialid läbi tegema ning praktiliselt katsetama."

**Rõhuta:**

- ✅ Mõistad edge computing kontseptsiooni
- ✅ Näed arhitektuurset pilti (millal edge, millal central)
- ✅ Tead SvelteKit + Cloudflare integratsiooni
- ✅ Valmis kiiresti õppima (10-13h plaan)

---

**Edukat õppimist! Cloudflare on intuitiivne ja hästi dokumenteeritud - õppimine on kiire.**
