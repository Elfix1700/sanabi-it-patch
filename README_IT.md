# SANABI in italiano — patch amatoriale

Traduzione **amatoriale, non ufficiale e gratuita** di SANABI in italiano.
Richiede una copia originale del gioco. Non include nessun file del gioco.

> **Fatta per la versione 1.3.53.** Su versioni diverse lo script salta
> automaticamente le stringhe che non corrispondono e te lo dice: non rompe
> niente, semplicemente traduce meno.

---

## Cosa fa

Il gioco ha già 11 lingue, ognuna con il proprio posto ("slot") dentro i file
di testo. La patch mette l'italiano **al posto dell'inglese**. Non si aggiunge
una dodicesima lingua, non si creano riferimenti nuovi: la struttura dei file
resta identica.

**Dopo la patch devi selezionare "English" (Inglese) nel menu
Opzioni → Lingua.** È l'unico punto da ricordare: selezioni la voce che si
chiama English e il gioco parla italiano. Tutte le altre lingue restano
funzionanti e intatte, quindi puoi sempre tornare indietro.

## Requisiti

- Python 3.8 o più recente
- UnityPy: `pip install UnityPy`
- Una cartella di SANABI con `SNB.exe` e `SNB_Data/StreamingAssets/aa/`
- Nessun diritto di amministratore, nessuna connessione internet

## Installazione

### Linux / macOS / Steam Deck

```bash
cd patch_it_sanabi
./run_linux.sh --apply
```

oppure a mano:

```bash
python3 patcher/patch_sanabi_it.py --path /percorso/di/SANABI --apply
```

### Windows

Doppio click su `run_windows.bat`, oppure da terminale:

```cmd
python patcher\patch_sanabi_it.py --path "C:\percorso\di\SANABI" --apply
```

### Steam Deck

Stessa procedura di Linux. Se hai installato il gioco in
`~/.steam/steam/steamapps/common/SANABI`, lo script lo trova da solo e puoi
anche omettere `--path`.

## Controllare prima di applicare

```bash
python3 patcher/patch_sanabi_it.py --check
```

Dice quante stringhe combaciano, per bundle e per capitolo. È una lettura
solamente: non modifica nulla.

## Disinstallare

```bash
python3 patcher/patch_sanabi_it.py --restore
```

Ripristina i file originali dalla cartella di backup e verifica gli hash
SHA-256. Dopo `--restore` il gioco è esattamente come prima.

## Problemi noti

- La lingua va selezionata a mano (vedi sopra): la patch mette l'italiano nello
  slot inglese, quindi devi scegliere "English".
- La schermata iniziale e il selettore lingua partono nella lingua del tuo
  sistema operativo. Se vedi un'altra lingua all'avvio, apri
  Opzioni → Lingua e scegli English.
- I sottotitoli del DLC sono tradotti come il resto.
- Testato su Linux con Wine. Windows nativo e Steam Deck non sono stati
  provati direttamente dall'autore, ma lo script non fa niente di specifico
  di Linux.

## Segnalare un errore

Apri una issue sul repository GitHub indicando: versione del gioco, capitolo,
la battuta in inglese e quella che vedi in italiano.
