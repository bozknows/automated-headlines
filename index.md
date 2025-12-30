---
layout: default
title: Home
---

# 🤖 Matt's AI News Feed
*Updates generated automatically by local LLM.*

<hr>

{% for post in site.posts %}
  <article style="margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 20px;">
    <h2>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <p style="color: gray; font-size: 0.9em;">
      {{ post.date | date: "%B %d, %Y at %I:%M %p" }}
    </p>
    
    <div class="post-content">
      {{ post.content }}
    </div>
  </article>
{% endfor %}