# Contribuire a Scioperi Italia

Grazie per il tuo interesse nel contribuire alla mia integrazione!

## 🐛 Segnalare Bug

Apri un [Issue](https://github.com/sappadev/scioperi-italia/issues) includendo:
- Versione Home Assistant
- Versione integrazione
- Log errore completo
- Passi per riprodurre

## 💡 Proporre Funzionalità

Apri un [Issue](https://github.com/sappadev/scioperi-italia/issues) con:
- Descrizione dettagliata
- Caso d'uso
- Mockup/screenshot (se applicabile)

## 🔧 Pull request

1. **Fork** il repository
2. **Crea branch**: `git checkout -b feature/nome-feature`
3. **Committa**: `git commit -am 'Add: nuova feature'`
4. **Push**: `git push origin feature/nome-feature`
5. **Apri PR** con descrizione dettagliata

### Convenzioni commit

- `Add:` - Nuova funzionalità
- `Fix:` - Bug fix
- `Update:` - Aggiornamento esistente
- `Docs:` - Solo documentazione
- `Style:` - Formattazione
- `Refactor:` - Refactoring codice
- `Test:` - Aggiunta test

### Codice

- Python 3.12+
- Segui PEP 8
- Aggiungi docstring
- Testa localmente

### Testing locale

```bash
# Test parser
python test_simple.py

# Test integrazione
# Copia in /config/custom_components/
# Riavvia HA
# Controlla log
```

## 📋 Checklist PR

- [ ] Codice testato localmente
- [ ] Documentazione aggiornata
- [ ] CHANGELOG.md aggiornato
- [ ] Nessun warning nei log
- [ ] Compatibile HA attuale

## 📝 Licenza

Contribuendo accetti la licenza MIT del progetto.

## ❓ Domande

Apri un [Discussion](https://github.com/sappadev/scioperi-italia/discussions) o unisciti alla community Home Assistant Italia.
