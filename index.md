---
layout: default
title: Home
---

# 🤖 AI News Feed
*Updates generated automatically by local LLM.*

<hr>

<ul>
  {% for post in site.posts %}
    <li style="margin-bottom: 15px;">
      <a href="{{ post.url | relative_url }}" style="font-weight: bold; font-size: 1.2em;">
        {{ post.title }}
      </a>
      <br>
      <span style="color: #666; font-size: 0.9em;">
        {{ post.date | date: "%B %d, %I:%M %p" }}
      </span>
      <p style="margin-top: 5px;">{{ post.excerpt | strip_html | truncatewords: 20 }}</p>
    </li>
  {% endfor %}
</ul>