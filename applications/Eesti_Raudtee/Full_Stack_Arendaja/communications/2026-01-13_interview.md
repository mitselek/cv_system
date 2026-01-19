# Communication: Interview

**Date:** 2026-01-13
**From:** Kristi Rand <kristi.rand@evr.ee>
**Subject:** Kandideerimine AS-i Eesti Raudtee

---

Tere Mihkel-Mikelis

Täname meeldiva vestluse eest! Konkursi järgmiseks etapiks on testülesande lahendamine, mille kirjeldus on allpool. Vastust ootan hiljemalt pühapäeva, 18 jaanuari õhtuks.

**Testülesanne: Mock Microsoft Graph Mail Service**

**Eesmärk**

Luua **Cloudflare platformil** töötav rakendus, mis imiteerib Microsoft Graphi POST /v1.0/me/sendMail API-t, salvestab saadetud e-kirjad ning võimaldab neid UI kaudu vaadata ja API-t testida.

Arendaja vastutab **arhitektuuri, struktuuri ja tehniliste otsuste** eest.

**Kasutatav tehniline stack**

- Cloudflare (Workers, D1, R2, jne – **valikuline vastavalt lahendusele**)
- SvelteKit
- TypeScript
- Tailwind CSS
- GitHub
- Testimine (TDD või test-first eelistatud)
- Valmidus pair programming sessiooniks

**Funktsionaalsed nõuded**

**1. Mock API**

- Implementeeri endpoint, mis käitub sarnaselt Microsoft Graphi POST /v1.0/me/sendMail API-le
- Request ja response struktuur võib olla **lihtsustatud**, kuid peab olema dokumenteeritud
- Edukas päring peab:
  - valideerima sisendi
  - salvestama e-kirja
  - tagastama korrektse HTTP vastuse

**2. Andmete talletamine**

- Saadetud e-kirjad peavad olema püsivalt salvestatud
- Andmemudel ja salvestusviis on arendaja otsustada
- Andmete struktuur peab olema põhjendatud

**3. UI: saadetud kirjade vaatamine**

- Loo kasutajaliides, kus:
  - on võimalik vaadata saadetud e-kirju
  - on võimalik avada ühe kirja detailid
- Disain ei ole fookus, **selgus ja struktuur on**

**4. API testimise kasutajaliides**

- Loo kasutajaliides, millega saab:
  - koostada ja saata päringu mock API-le
  - näha API vastust
- Kuidas ja kus see UI töötab, on arendaja otsustada

**Dokumentatsioon**

Lisa README, kus on kirjeldatud:

- kuidas lahendust käivitada
- arhitektuursed otsused ja nende põhjendus
- võimalikud kitsaskohad
- ideed edasiseks arenduseks

Kui tekib küsimusi, siis palun pöördu meie tehnoloogiajuhi Valeri Kuzmini poole +37253407716, valeri.kuzmin@evr.ee.

Edu soovides!
