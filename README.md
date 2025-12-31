# Scioperi Italia - Home Assistant Integration

Integrazione HACS per monitorare gli scioperi in Italia dal feed ufficiale del Ministero delle Infrastrutture e dei Trasporti.

## 🎯 Caratteristiche

- ✅ **Calendario eventi** con tutti gli scioperi
- ✅ **Sensori multipli** per ogni settore (TPL, Aereo, Ferroviario, ecc.)
- ✅ **Filtri personalizzabili** per regione e settore
- ✅ **Aggiornamento automatico** ogni 6 ore
- ✅ **Configurazione UI** super semplice
- ✅ **100% open source**

## 📥 Installazione

### Via HACS (Consigliato)

1. Apri HACS in Home Assistant
2. Clicca sui 3 puntini in alto a destra
3. Seleziona "Custom repositories"
4. Aggiungi: `https://github.com/sappadev/scioperi-italia`
5. Categoria: `Integration`
6. Cerca "Scioperi Italia" e installa

### Manuale

1. Scarica la cartella `scioperi_italia`
2. Copiala in `config/custom_components/`
3. Riavvia Home Assistant

## ⚙️ Configurazione

1. Vai in **Impostazioni** → **Dispositivi e Servizi**
2. Clicca **+ Aggiungi Integrazione**
3. Cerca **"Scioperi Italia"**
4. Configura (opzionale):
   - Filtra per Regione (default: Tutte)
   - Filtra per Settore (default: Tutti)

## 📊 Entità create

### Sensori

- `sensor.scioperi_totali` - Conteggio totale scioperi futuri
- `sensor.scioperi_oggi` - Scioperi di oggi
- `sensor.scioperi_prossimo` - Data prossimo sciopero
- `sensor.scioperi_tpl` - Scioperi Trasporto Pubblico Locale
- `sensor.scioperi_aereo` - Scioperi settore aereo
- `sensor.scioperi_ferroviario` - Scioperi settore ferroviario
- `sensor.scioperi_trasporto_merci_e_logistica` - Scioperi trasporto merci
- `sensor.scioperi_marittimo` - Scioperi settore marittimo

### Calendario

- `calendar.scioperi_italia` - Eventi calendario per tutti gli scioperi

## 🤖 Esempi automazioni

### Notifica Sciopero Domani

```yaml
automation:
  - alias: "Notifica Sciopero Domani"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.scioperi_oggi
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ Sciopero Domani"
          message: >
            Domani ci sono {{ states('sensor.scioperi_domani') }} scioperi.
            Settore: {{ state_attr('sensor.scioperi_prossimo', 'sector') }}
```
### Notifica Sciopero TPL

```yaml
automation:
  - alias: "Notifica Sciopero TPL"
    trigger:
      - platform: state
        entity_id: sensor.scioperi_tpl
    condition:
      - condition: numeric_state
        entity_id: sensor.scioperi_tpl
        above: 0
    action:
      - service: notify.telegram
        data:
          message: >
            🚌 Attenzione! {{ states('sensor.scioperi_tpl') }} 
            scioperi TPL in programma
```

## 🎨 Card Lovelace

### Card Semplice

```yaml
type: entities
title: Scioperi Italia
entities:
  - entity: sensor.scioperi_totali
    name: Totali
  - entity: sensor.scioperi_oggi
    name: Oggi
  - entity: sensor.scioperi_prossimo
    name: Prossimo
```

### Card articolata con Markdown

```yaml
type: markdown
title: 📅 Prossimi Scioperi
content: |
  **Totali:** {{ states('sensor.scioperi_totali') }}
  **Oggi:** {{ states('sensor.scioperi_oggi') }}
  
  **Prossimo Sciopero:**
  - Data: {{ state_attr('sensor.scioperi_prossimo', 'start_date') }}
  - Settore: {{ state_attr('sensor.scioperi_prossimo', 'sector') }}
  - Regione: {{ state_attr('sensor.scioperi_prossimo', 'region') }}
  - Modalità: {{ state_attr('sensor.scioperi_prossimo', 'modality') }}
```

### Card per settore

```yaml
type: horizontal-stack
cards:
  - type: statistic
    entity: sensor.scioperi_tpl
    name: TPL
    icon: mdi:bus
  - type: statistic
    entity: sensor.scioperi_aereo
    name: Aerei
    icon: mdi:airplane
  - type: statistic
    entity: sensor.scioperi_ferroviario
    name: Treni
    icon: mdi:train
```

### Calendario

```yaml
type: calendar
entities:
  - calendar.scioperi_italia
```

## 📱 Dashboard completa di esempio

```yaml
views:
  - title: Scioperi
    icon: mdi:alert-circle
    cards:
      - type: entities
        title: Riepilogo Scioperi
        entities:
          - entity: sensor.scioperi_totali
          - entity: sensor.scioperi_oggi
          - entity: sensor.scioperi_prossimo
      
      - type: horizontal-stack
        cards:
          - type: statistic
            entity: sensor.scioperi_tpl
            name: TPL
          - type: statistic
            entity: sensor.scioperi_aereo
            name: Aerei
          - type: statistic
            entity: sensor.scioperi_ferroviario
            name: Treni
      
      - type: calendar
        entities:
          - calendar.scioperi_italia
        initial_view: listWeek
      
      - type: markdown
        title: Dettagli Prossimo Sciopero
        content: |
          {% if state_attr('sensor.scioperi_prossimo', 'sector') %}
          **{{ state_attr('sensor.scioperi_prossimo', 'sector') }}**
          
          📅 {{ state_attr('sensor.scioperi_prossimo', 'start_date') }}
          📍 {{ state_attr('sensor.scioperi_prossimo', 'region') }}
          ⏰ {{ state_attr('sensor.scioperi_prossimo', 'modality') }}
          👥 {{ state_attr('sensor.scioperi_prossimo', 'unions') }}
          {% else %}
          Nessuno sciopero programmato
          {% endif %}
```

## 🔧 Configurazione avanzata

### Cambiare intervallo aggiornamento

Modifica `const.py`:
```python
UPDATE_INTERVAL_HOURS = 3  # Ogni 3 ore invece di 6
```

### Filtrare scioperi

Puoi filtrare per:
- **Regione**: Solo scioperi nella tua regione
- **Settore**: Solo settori specifici (es. solo TPL)

Configurabile dalla UI nelle opzioni dell'integrazione.

## 📝 Attributi sensori

Ogni sensore include attributi dettagliati:

```yaml
sensor.scioperi_prossimo:
  sector: "Trasporto pubblico locale"
  region: "Piemonte"
  province: "Cuneo"
  start_date: "15/01/2026"
  end_date: "15/01/2026"
  modality: "24 ORE"
  relevance: "Regionale"
  unions: "FILT-CGIL/FIT-CISL/UILT-UIL"
  category: "PERSONALE TPL REGIONE PIEMONTE"
```

## 🤝 Contribuire

Qualsiasi contributo è il benvenuto.

1. Fork il repository
2. Crea un branch (`git checkout -b feature/nuova-feature`)
3. Commit (`git commit -am 'Aggiunge nuova feature'`)
4. Push (`git push origin feature/nuova-feature`)
5. Apri una Pull Request

## 📄 Licenza

MIT License - vedi LICENSE per dettagli

## 🙏 Crediti

- Dati: [Ministero delle Infrastrutture e dei Trasporti](https://scioperi.mit.gov.it)

## ⚠️ Disclaimer

Questa integrazione non è ufficiale né affiliata al MIT. 
I dati sono forniti "as is" dal feed RSS pubblico.
Verifica sempre le informazioni sul sito ufficiale.

---

**Supporto:** Apri un issue su GitHub
**Community:** [Home Assistant Italia](https://www.hassiohelp.eu)