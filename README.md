# 🎯 Scioperi Italia

[![GitHub Release](https://img.shields.io/github/release/sappadev/scioperi-italia.svg)](https://github.com/sappadev/scioperi-italia/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/default)
[![License](https://img.shields.io/github/license/sappadev/scioperi-italia.svg)](LICENSE)

Questa integrazione rileva automaticamente gli scioperi in Italia attraverso il feed RSS ufficiale del Ministero dei Trasporti e delle Infrastrutture. Può essere configurata con facilità direttamente dalla UI di Home Assistant e offre diverse opzioni per personalizzare gli avvisi. Espone diverse entità che possono venire utilizzate in diverse automazioni (come negli esempi).

### 🏠 **Rileva la posizione dell'abitazione automaticamente**
- ✅ Usa coordinate configurate in Home Assistant
- ✅ Zero configurazione manuale
- ✅ Setup in 30 secondi

### 📍 **Calcola automaticamente la distanza dello sciopero dall'abitazione**
- ✅ Calcola distanza di ogni sciopero da casa tua
- ✅ Filtro raggio personalizzabile (5km → Italia intera)
- ✅ Mostra solo scioperi che ti interessano
---

## 📥 Installazione

### Via HACS (Consigliato)

1. **HACS** → **Integrazioni**
2. **⋮** (menu) → **Repository personalizzati**
3. URL: `https://github.com/sappadev/scioperi-italia`
4. Categoria: **Integration**
5. **Scarica** → **Riavvia HA**

### Manuale

```bash
cd /config/custom_components
git clone https://github.com/sappadev/scioperi-italia.git
mv scioperi-italia/custom_components/scioperi_italia .
rm -rf scioperi-italia
```

Riavvia Home Assistant.

---

## ⚙️ Configurazione

### Setup iniziale (30 secondi)

1. **Impostazioni** → **Dispositivi e Servizi** → **+ Aggiungi**
2. Cerca **"Scioperi Italia"**
3. Configura:
   - **Raggio** (default 50km)
   - **Settori preferiti** (opzionale)
   - **Notifiche automatiche** (consigliato ✅)
   - **Ore preavviso** (default 24h prima)

4. **Fatto!** 🎉

### Coordinate casa

L'integrazione usa **automaticamente** le coordinate configurate in:
- **Impostazioni** → **Sistema** → **Generale** → **Posizione**

**Non serve inserire alcun inserimento manuale.**

---

## 📊 Sensori Creati

### 🎯 In base alla posizione

| Sensore | Descrizione |
|---------|-------------|
| `sensor.scioperi_vicini` | Scioperi nel TUO raggio |
| `sensor.scioperi_prossimo_vicino` | Prossimo sciopero vicino + distanza |
| `sensor.scioperi_preferiti` | Scioperi settori che hai scelto |
| `sensor.scioperi_domani` | Cosa succede domani |

### 📅 Temporali

| Sensore | Descrizione |
|---------|-------------|
| `sensor.scioperi_totali` | Tutti i futuri scioperi |
| `sensor.scioperi_oggi` | Scioperi di oggi |
| `sensor.scioperi_prossimo` | Prossimo in assoluto |

### 🚦 Per settore

| Sensore | Descrizione | Icona |
|---------|-------------|-------|
| `sensor.scioperi_tpl` | Trasporto Pubblico Locale | 🚌 |
| `sensor.scioperi_aereo` | Settore aereo | ✈️ |
| `sensor.scioperi_ferroviario` | Treni | 🚂 |
| `sensor.scioperi_trasporto_merci_e_logistica` | Logistica | 🚚 |
| `sensor.scioperi_marittimo` | Navi | ⛴️ |

### 📅 Calendario

| Entità | Descrizione |
|--------|-------------|
| `calendar.scioperi_italia` | Tutti gli scioperi come eventi |

---

## 🤖 Automazioni di esempio

### 1. Notifica sciopero nel giorno seguente

```yaml
automation:
  - alias: "Sciopero vicino domani"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.scioperi_domani
        above: 0
    action:
      - service: notify.mobile_app_phone_TUO_DISPOSITIVO # Sostituisci con l'entità id notifica del tuo dispositivo
        data:
          title: "⚠️ Sciopero domani"
          message: >
            🚨 {{ states('sensor.scioperi_domani') }} sciopero/i domani
            nel raggio di {{ state_attr('sensor.scioperi_vicini', 'radius_km') }}km!
```

### 2. Controllo percorso (esempio: casa - lavoro)

```yaml
automation:
  - alias: "Controlla percorso"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: scioperi_italia.check_route
        data:
          destination_lat: 44.7007  # Inserisci la latitudine della destinazione
          destination_lon: 8.0357 # Inserisci la longitudine della destinazione
          radius_km: 10 # Puoi personalizzare il raggio in Km
```

### 3. TTS sciopero nella giornata di oggi

```yaml
automation:
  - alias: "Alert sciopero oggi"
    trigger:
      - platform: numeric_state
        entity_id: sensor.scioperi_oggi
        above: 0
    action:
      - service: tts.google_translate_say
        entity_id: media_player.TUO_PLAYER # Sostituisci con l'entità del tuo media player
        data:
          message: "Attenzione! Oggi ci sono scioperi in programma"
```

**Vedi tutti gli esempi in `/examples/automations.yaml`**

---

## 🎨 Dashboard lovelace

### Card semplice

```yaml
type: entities
title: 🎯 Scioperi vicini
entities:
  - entity: sensor.scioperi_vicini
    name: Nel Raggio
  - entity: sensor.scioperi_oggi
    name: Oggi
  - entity: sensor.scioperi_domani
    name: Domani
  - entity: sensor.scioperi_prossimo_vicino
    name: Prossimo vicino
```

### Dashboard di esempio completa

```yaml
type: vertical-stack
cards:
  # Statistiche
  - type: horizontal-stack
    cards:
      - type: statistic
        entity: sensor.scioperi_vicini
        name: Vicini
        icon: mdi:map-marker-radius
      - type: statistic
        entity: sensor.scioperi_oggi
        name: Oggi
      - type: statistic
        entity: sensor.scioperi_domani
        name: Domani
  
  # Prossimo vicino
  - type: markdown
    content: |
      ### 📍 Prossimo sciopero vicino
      
      **{{ states('sensor.scioperi_prossimo_vicino') }}**
      
      {{ state_attr('sensor.scioperi_prossimo_vicino', 'sector') }}
      {{ state_attr('sensor.scioperi_prossimo_vicino', 'region') }}
      
      Distanza: {{ state_attr('sensor.scioperi_prossimo_vicino', 'distance_km') }}km
  
  # Calendario
  - type: calendar
    entities:
      - calendar.scioperi_italia
```

**Vedi dashboard completa in `/examples/lovelace.yaml`**

---

## 📱 Attributi dei sensori

Ogni sensore include **attributi dettagliati** che puoi usare nelle tue dashboard o automazioni:

```yaml
sensor.scioperi_prossimo_vicino:
  state: "15/01/2026 (12km)"
  attributes:
    sector: "Trasporto pubblico locale"
    region: "Piemonte"
    start_date: "15/01/2026"
    modality: "24 ORE"
    distance: "12km"
    distance_km: 12.5
    radius_km: 50
    unions: "FILT-CGIL/FIT-CISL"
    in_radius: true
```

---

## 🔧 Opzioni avanzate

### Cambiare raggio

**Impostazioni** → **Dispositivi** → **Scioperi Italia** → **Configura**

Scegli tra: **5km, 10km, 25km, 50km, 100km, 500km** (Italia intera)

### Settori desiderati

Seleziona solo i settori che ti interessano:
- Trasporto pubblico locale
- Aereo
- Ferroviario
- Trasporto merci e logistica
- Marittimo

### Notifiche automatiche

Configura **quando** ricevere notifiche:
- **24 ore** prima (default)
- **48 ore** prima
- **72 ore** prima
- **1 settimana** prima

### Posizione lavoro/scuola (Opzionale)

Aggiungi coordinate lavoro/scuola per automazioni:
- Formato: `lat,lon` (es. `44.7007,8.0357`)
- Usato da `check_route` service

---

## 🎯 Eventi personalizzati

L'integrazione lancia **eventi** per automazioni avanzate:

### `scioperi_italia_strike_tomorrow`

Lanciato quando c'è uno sciopero domani nel raggio.

```yaml
trigger:
  - platform: event
    event_type: scioperi_italia_strike_tomorrow
action:
  - service: light.turn_on
    target:
      entity_id: light.notification
    data:
      color_name: red
```

### `scioperi_italia_strike_nearby`

Lanciato quando rileva nuovo sciopero vicino.

```yaml
trigger:
  - platform: event
    event_type: scioperi_italia_strike_nearby
```

### `scioperi_italia_route_check_result`

Risultato controllo percorso (da `check_route` service).

---

## 📚 Documentazione Completa

- [🤖 Esempi Automazioni](custom_components/scioperi_italia/examples/automations.yaml)
- [🎨 Esempi Dashboard](custom_components/scioperi_italia/examples/lovelace.yaml)
- [🤝 Contribuire](CONTRIBUTING.md)

---

## 🚀 Roadmap V3.0

- [ ] 🗺️ Card mappa custom con marker scioperi
- [ ] 📊 Grafici storici scioperi
- [ ] 🔔 Integrazione Telegram bot
- [ ] 📱 Notifiche push native
- [ ] 🎯 Multi-location (casa + lavoro + altro)
- [ ] 🤖 AI predizioni settori a rischio
- [ ] 📈 Statistiche mensili/annuali

---

## ❓ FAQ

**Q: Devo inserire le coordinate di casa?**  
A: NO! Usa automaticamente quelle configurate in Home Assistant.

**Q: Come cambio il raggio?**  
A: Impostazioni → Scioperi Italia → Configura → Raggio

**Q: Funziona con la mia versione di HA?**  
A: Sì, compatibile con HA 2023.1+

**Q: Posso monitorare solo TPL?**  
A: Sì! Configura "Settori preferiti" e usa `sensor.scioperi_preferiti`

**Q: Le notifiche sono troppo frequenti**  
A: Disabilitale o cambia "Ore preavviso" a 48/72h

---

## 🐛 Bug Report & Feature Request

- [🐛 Report Bug](https://github.com/sappadev/scioperi-italia/issues/new?template=bug_report.md)
- [✨ Richiedi Feature](https://github.com/sappadev/scioperi-italia/issues/new?template=feature_request.md)
- [💬 Discussioni](https://github.com/sappadev/scioperi-italia/discussions)

---

## 🙏 Crediti

- **Dati**: [Ministero Infrastrutture e Trasporti](https://scioperi.mit.gov.it)
- **Sviluppatore**: [@sappadev](https://github.com/sappadev)
- **Community**: Home Assistant Italia

---

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

---

## ⭐ Se ti piace, lascia una stella!

[![GitHub stars](https://img.shields.io/github/stars/sappadev/scioperi-italia.svg?style=social&label=Star)](https://github.com/sappadev/scioperi-italia)
