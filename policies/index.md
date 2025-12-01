---
title: Policies
layout: default
language: en
---

# Policies

<ul class="policy-list">
  {% assign items = site.pages | where_exp: "p", "p.path contains 'policies/'" %}
  {% for p in items %}
    {% unless p.url contains '/examples/' %}
      {% if p.id and p.type == 'generic-policy' %}
<li class="policy-list-item">
  <h2><a href="{{ p.url | relative_url }}">{{ p.title }}</a></h2>
  {% if p.summary %}
  <p class="policy-list-summary">{{ p.summary }}</p>
  {% endif %}
  <dl class="policy-list-meta">
    {% if p.hazard_type %}
    <div>
      <dt>Hazard</dt>
      <dd>{{ p.hazard_type | join: ", " }}</dd>
    </div>
    {% endif %}
    {% if p.level_of_government_applicability %}
    <div>
      <dt>Levels of government</dt>
      <dd>{{ p.level_of_government_applicability | join: ", " }}</dd>
    </div>
    {% endif %}
    {% if p.implementation_horizon %}
    <div>
      <dt>Implementation horizon</dt>
      <dd>{{ p.implementation_horizon }}</dd>
    </div>
    {% endif %}
    {% if p.fiscal_profile %}
    <div>
      <dt>Fiscal profile</dt>
      <dd>{{ p.fiscal_profile.cost_range | default: "not specified" }}, {{ p.fiscal_profile.cost_type | default: "not specified" }}</dd>
    </div>
    {% endif %}
  </dl>
</li>
      {% endif %}
    {% endunless %}
  {% endfor %}
</ul>
