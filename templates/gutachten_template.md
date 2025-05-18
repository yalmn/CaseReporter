# Forensisches Gutachten

**Fall-ID:** {{ fall_id }}

## 1. Einleitung

{{ einleitung }}

## 2. Vorgehensweise

{{ vorgeschwindigkeit }}

## 3. Befunde

{% for fund in befundsliste %}

- **Fund:** {{ fund.beschreibung }}, **Zeit:** {{ fund.zeitstempel }}
  {% endfor %}

## 4. Fazit & Empfehlungen

{{ ki_fazit }}
