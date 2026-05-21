---
tags:
  - daily
created: <% tp.file.creation_date("YYYY-MM-DD") %>
weekday: <% tp.date.now("dddd") %>
energy: 
mood: 
---

# <% tp.file.creation_date("ddd, MMM D YYYY") %>

> [!quote] <% tp.file.cursor(1) %>

## ⬆ One Big Thing

> *If I only accomplish ONE thing today, what would make everything else easier or unnecessary?*

- 

## ✅ Tasks

### Must Do (≤3)
- [ ] 
- [ ] 
- [ ] 

### Should Do
- [ ] 

### Could Do
- [ ] 

## ⏱ Timebox

| Time | Block | Outcome |
|------|-------|---------|
| 08:00–10:00 | Deep work | |
| 10:00–10:15 | Break | |
| 10:15–12:00 | | |
| 12:00–13:00 | Lunch | |
| 13:00–15:00 | | |
| 15:00–15:15 | Break | |
| 15:15–17:00 | | |

## 📝 Log

> [!info] What happened today — captured in the moment, not summarized later.

-

## 🔍 EOD Reflection

**What went well?**


**What didn't go well?**


**What did I learn?**


**Tomorrow's edge:**

-

## 🔗 Links

<%
const today = tp.file.creation_date("YYYY-MM-DD");
const yesterday = tp.date.now("YYYY-MM-DD", -1, today);
const tomorrow = tp.date.now("YYYY-MM-DD", 1, today);
%>
← <% tp.date.now("ddd, MMM D", -1, today) %> · → <% tp.date.now("ddd, MMM D", 1, today) %>
