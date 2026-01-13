# MCP Tool Verification Results

**Date:** 2026-01-13  
**Method:** Systematic testing of all 35 MCP tools

## Test Data

UUIDs obtained from EdgeDB:

- Skill: `915d8bc2-f053-11f0-a267-f35dabef99f0` (project-management)
- Certification: `9eefaf3e-f019-11f0-905b-17b36f6dc68e` (mtcna-2025)
- Education: `c84f012c-f082-11f0-8893-7bf667e66719` (university-studies-1990-2002)
- Achievement: `9c30734a-f088-11f0-afb1-8f2fc16b1937` (mcp-test-achievement-2026-01-13)
- Experience: `f420cbca-f053-11f0-a267-5fd1df86972d` (auma-expo-1992-1993)
- Project: `cef57094-f017-11f0-8b39-ff1c10170e28` (cv-system)
- Project (test): `f34b113e-f089-11f0-8055-2b04d2c95a55` (mcp-test-project-2026-01-13)
- Hobby: `8231942e-f01a-11f0-95bd-cfdeefcf5d26` (3d-modeling-printing)
- Language: `a9aa1ce6-f089-11f0-8055-5769e50bd137` (mcp-test-language-2026-01-13)
- Education (test): `f37701fe-f089-11f0-8055-0b6def026149` (mcp-test-education-2026-01-13)

---

## Results

| Tool Name             | Tested UTC           | Status      | Error/Result                                                                               |
| --------------------- | -------------------- | ----------- | ------------------------------------------------------------------------------------------ |
| add_achievement       | 2026-01-13T14:03:17Z | WORKS       | Created 9c30734a-f088-11f0-afb1-8f2fc16b1937 (mcp-test-achievement-2026-01-13)             |
| add_certification     | 2026-01-13T13:20:00Z | WORKS       | Correctly rejects duplicate external_id (exclusive constraint)                             |
| add_education         | 2026-01-13T13:21:39Z | WORKS       | Re-added after delete; c84f012c-f082-11f0-8893-7bf667e66719                                |
| add_experience        | 2026-01-13T13:28:37Z | WORKS       | Created c0eeaf76-f083-11f0-8c43-ab2ffdc806a4 (mcp-test-org-mcp-test-experience-2026-01-01) |
| add_hobby             | 2026-01-13T13:30:50Z | WORKS       | Created 0f3a3362-f084-11f0-b4b2-5f6fb3d85c55 (mcp-hobby-2026-01-13)                        |
| add_language          | 2026-01-13T14:10:49Z | WORKS       | Created a9aa1ce6-f089-11f0-8055-5769e50bd137 (mcp-test-language-2026-01-13)                |
| add_project           | 2026-01-13T14:12:53Z | WORKS       | Created f34b113e-f089-11f0-8055-2b04d2c95a55 (mcp-test-project-2026-01-13)                 |
| add_skill             | 2026-01-13T13:39:00Z | WORKS       | Created 3364323c-f085-11f0-a7f7-5fd68dee7adb (mcp-test-skill-2)                            |
| add_tag               | 2026-01-13T13:39:30Z | WORKS       | Created 4450a738-f085-11f0-a7f7-5f0477512c40 (mcp-test-2)                                  |
| find_similar_tags     | 2026-01-13T13:39:54Z | WORKS       | Returns mcp-test (distance 1)                                                              |
| get_achievement       | 2026-01-13T14:03:35Z | WORKS       | Returns mcp-test-achievement-2026-01-13 with tags                                          |
| get_certification     | 2026-01-13T13:42:01Z | WORKS       | Returns full certification                                                                 |
| get_education         | 2026-01-13T13:46:13Z | WORKS       | Returns education with institutions                                                        |
| get_experience        | 2026-01-13T13:46:24Z | WORKS       | Returns experience with tags                                                               |
| get_hobby             | 2026-01-13T13:46:34Z | WORKS       | Returns full hobby object                                                                  |
| get_language          | 2026-01-13T14:10:56Z | WORKS       | Returns full language object (a9aa1ce6-f089-11f0-8055-5769e50bd137)                        |
| get_project           | 2026-01-13T14:17:45Z | WORKS       | Returns full project object (f34b113e-f089-11f0-8055-2b04d2c95a55)                         |
| get_skill             | 2026-01-13T13:47:19Z | WORKS       | Returns complete skill object                                                              |
| get_tag_usage         | 2026-01-13T13:47:37Z | WORKS       | Returns usage stats by entity                                                              |
| list_tags             | 2026-01-13T13:47:46Z | WORKS       | Returns tags; category filter works                                                        |
| search_achievements   | 2026-01-13T14:03:25Z | WORKS       | Tag filter works; returns matching achievements                                            |
| search_certifications | 2026-01-13T14:05:09Z | WORKS       | Issuer filter works (Mikrotikls SIA)                                                       |
| search_education      | 2026-01-13T14:05:09Z | WORKS       | Empty args returns all                                                                     |
| search_experiences    | 2026-01-13T14:05:09Z | WORKS       | Empty args returns all                                                                     |
| search_hobbies        | 2026-01-13T14:05:09Z | WORKS       | Empty args returns all                                                                     |
| search_languages      | 2026-01-13T14:10:56Z | WORKS       | Tag filter works (mcp-test/test); empty args currently returns []                          |
| search_projects       | 2026-01-13T14:05:09Z | WORKS       | Status filter works (active)                                                               |
| search_skills         | 2026-01-13T13:48:20Z | WORKS       | Returns list of skills; supports optional filters                                          |
| update_certification  |                      | ❌ DISABLED |                                                                                            |
| update_education      | 2026-01-13T14:17:10Z | WORKS       | Updated degree + dates.end on f37701fe-f089-11f0-8055-0b6def026149                         |
| update_experience     |                      | ❌ DISABLED |                                                                                            |
| update_hobby          |                      | ❌ DISABLED |                                                                                            |
| update_language       |                      | ❌ DISABLED |                                                                                            |
| update_project        | 2026-01-13T14:14:20Z | WORKS       | Updated article + technologies on f34b113e-f089-11f0-8055-2b04d2c95a55                     |
| update_skill          |                      | ❌ DISABLED |                                                                                            |
