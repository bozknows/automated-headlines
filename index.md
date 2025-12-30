---
layout: default
title: Home
---

# 🤖 Matt's AI News Feed
*Updates generated automatically by local LLM.*

---

## Latest Updates

<ul>
  {% for post in site.posts %}
    <li>
      <span style="color:gray">{{ post.date | date: "%b %d" }}</span> -
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>