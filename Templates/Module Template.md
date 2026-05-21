---
tags:
  - <% tp.file.cursor(1) %>
  - module
aliases:
  - ""
module: <% tp.file.title.match(/Module (\d+)/)?.[1] || "X" %>
parent: "[[IEC Motor Testing — Map of Content]]"
created: <% tp.file.creation_date("YYYY-MM-DD") %>
status: draft
---

# <% tp.file.title %>

> [!info] Part of [[IEC Motor Testing — Map of Content]]

## Overview


## Key Concepts

-

## Related Topics

-

## Resources

- 

## Navigation

<% 
const num = tp.file.title.match(/Module (\d+)/)?.[1] || "0";
const prev = String(parseInt(num) - 1).padStart(2, '0');
const next = String(parseInt(num) + 1).padStart(2, '0');
%>
<% if (parseInt(num) > 0) { %>
← Previous: [[Module <%= prev %>]]
<% } %>
→ Next: [[Module <%= next %>]]
