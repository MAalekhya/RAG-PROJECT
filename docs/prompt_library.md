# Prompt Library

A compact collection of repeatable prompts used in this project session. Copy/paste and replace placeholders (e.g., {file}, {nick}) when reusing.

---

## 1. Fix Python comment/syntax error
**Prompt:**
```
Open {file} and find why a comment is marked as an error; explain the cause and suggest an exact fix.
```
**Why useful:** Quick file inspection and small fix suggestions for syntax/linter issues.

---

## 2. List reasons a function's output isn't printed
**Prompt:**
```
I defined a function that should print a result but running the script prints nothing; list common causes and quick checks.
```
**Why useful:** Fast debugging checklist for missing output.

---

## 3. Research chat-app approaches (high-level)
**Prompt:**
```
Research the best ways to implement a simple chat application in Python for a beginner. Provide a comparison of approaches, minimal file structures, high-level pseudocode for server and client, testing/deployment notes, and one recommended approach with a minimal feature set.
```
**Why useful:** Chooses technology and scope for prototypes.

---

## 4. Research CLI chat options (detailed)
**Prompt:**
```
Compare CLI chat implementation options (TCP, UDP, asyncio, ZeroMQ, Redis). Recommend one for a beginner and provide file layout, pseudocode, UX considerations, testing/deploy notes, and a minimal feature list.
```
**Why useful:** Narrow down a CLI-first architecture.

---

## 5. Produce an implementation plan (constrained template)
**Prompt:**
```
Produce a concise implementation plan for a TCP asyncio CLI chat app that follows this template: headings, TL;DR (20-100 words), 3–6 short steps referencing exact file names and symbols (e.g., `server.py`, `handle_client`), and short further considerations; keep <= 200 words.
```
**Why useful:** Generates a ready-to-approve plan in a standard format.

---

## 6. Scaffold project files
**Prompt:**
```
Scaffold the project with minimal working files: `client.py`, `message_handler.py`, `bots/echo_bot.py`, `README.md`, `requirements.txt`, and `tests/test_message_handler.py`. Keep implementations small and runnable locally.
```
**Why useful:** Quickly bootstraps a working prototype.

---

## 7. Create a simple Mermaid diagram and save to file
**Prompt:**
```
Create a very-simple Mermaid flowchart explaining high-level component interactions and save it to `{filename}.md` in the repo.
```
**Why useful:** Produces an easy-to-render visual for docs.

---

## 8. Add line-by-line comments to a file
**Prompt:**
```
Add a simple plain-language comment to each line in {file} explaining what that line does.
```
**Why useful:** Makes code easier to teach and review.

---

## 9. Add function-summary comments
**Prompt:**
```
Add a concise summary comment above each function in {file} that explains what the function does in one sentence.
```
**Why useful:** Improves discoverability and quick comprehension.

---

## 10. Generate a simple JSON sample
**Prompt:**
```
Show a minimal JSON example for a chat message with fields: `type`, `nick`, `text`, `ts`, `id`, `source`.
```
**Why useful:** Reference for message format and tests.

---

## 11. Explain how to run the prototype and tests
**Prompt:**
```
Explain how to run the local file-backed prototype and its tests: prereqs, example commands to start clients and bots, and how to run unit tests.
```
**Why useful:** Onboarding for collaborators or re-run later.

---

If you want more prompts added (e.g., CI setup, linting rules, or detailed tests), tell me which topics to include and I'll append them.