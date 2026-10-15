# Changelog

## 1.0.0 — prima release

- Traduzione italiana completa dei dialoghi della storia principale
  (4.797 battute, dal Prologo al Capitolo 5 finale) e del DLC.
- Traduzione dell'interfaccia e dei menu (righe della schermata UITexts).
- Strategia C: l'italiano viene scritto nello slot della lingua inglese, che il
  gioco contiene già in tutte le sue 11 lingue. Nessuna lingua aggiunta,
  nessun path_id inventato, struttura degli Addressables invariata.
- Selezione dello slot per chiave (path_id della lingua inglese
  `7173981698464372551`), mai per indice fisso: l'ordine degli slot cambia da
  nodo a nodo (l'inglese è all'indice 3 nel 58% dei casi, a 2 nel 26%, a 1 nel
  16%).
- Verifica per hash SHA-256 del testo originale: se il gioco è una versione
  diversa, le stringhe che non corrispondono vengono saltate e segnalate.
- Correzione della concordanza di genere usando le altre lingue del gioco
  (francese, spagnolo, portoghese, tedesco, russo) come prova, con la mappa
  speaker → genere in `work/speakers_genere.json`.
- Registro tu/Lei uniformato sulla base degli stessi confronti
  (`work/registri.json`).
- Rimozione dei frammenti di inglese rimasti saldati nel testo italiano.
- Doppi spazi, spazi prima della punteggiatura, apostrofi tipografici
  U+2019 → U+0027 (presente in tutti gli atlas dei font).
- Token di markup preservati uno a uno: `{B}`, `{!!}`, `[ss]`, `[t:0.08]`,
  segnalibri dei tasti `[Jump]`, `[Dash]`, `[Hook]`, `[Move Left]`,
  `[DLCBurst]`, `[Restore]`, `[Right Click]`, `[마우스 좌클릭]` (questi ultimi
  restano in inglese/coreano perché è il gioco a sostituirli col tasto reale).
- Patcher con `--check`, `--apply`, `--restore`, idempotente, con backup
  interno e verifica SHA-256.
