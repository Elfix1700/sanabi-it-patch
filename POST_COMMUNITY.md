POST PER LA COMMUNITY
=====================

Due versioni: italiana (Steam) e inglese (Games Translator).
Sostituisci <LINK> con l'indirizzo della repository GitHub prima di pubblicare.


--------------------------------------------------------------------------
1) STEAM — bacheca discussioni / guida (italiano)
--------------------------------------------------------------------------

TITOLO: [Guida] SANABI in italiano — patch amatoriale gratuita

Ciao a tutti,

ho finito una traduzione italiana COMPLETA di SANABI: tutti i dialoghi della
storia principale (4.797 battute, dal Prologo al Capitolo 5 finale) e del DLC,
più i menu e le schermate dell'interfaccia. È un lavoro amatoriale, gratuito e
non ufficiale: non contiene nessun file del gioco e richiede una copia
originale.

Come funziona
-------------
Il gioco ha già undici lingue. La patch copia l'italiano "al posto"
dell'inglese, così la struttura dei file resta identica e nessuna delle altre
lingue viene toccata. Questo significa una sola cosa da ricordare:

>>> dopo aver applicato la patch, seleziona ENGLISH (Inglese) nel menu
>>> Opzioni → Lingua. Scegli la voce "English" e il gioco parla in italiano.

Installazione
-------------
1. Scarica la patch da <LINK> e scompattala.
2. Linux / Steam Deck: apri un terminale nella cartella patch_it_sanabi e scrivi
       ./run_linux.sh --apply
   Windows: doppio click su run_windows.bat
3. Avvia il gioco e metti la lingua su English.

Serve solo Python 3 (con la libreria UnityPy): gli script la installano da
soli se manca. Nessun diritto di amministratore, nessuna connessione.

Controllare prima di applicare
------------------------------
    ./run_linux.sh --check      (o run_windows.bat --check)

Ti dice quante stringhe combaciano con la versione che hai installato.
È una lettura, non modifica niente.

Disinstallare
-------------
    ./run_linux.sh --restore

Ripristina i file originali e verifica gli hash SHA-256: il gioco torna
esattamente com'era. La patch salva da sé una copia degli originali prima di
toccare qualunque cosa.

Cosa c'è dentro
---------------
- 4.797 battute di dialogo (storia principale + DLC), con i token di markup
  del gioco preservati uno per uno ({B}, {!!}, [ss], [t:0.08], i segnalibri
  dei tasti come [Jump] e [Dash] ecc.)
- Interfaccia e menu tradotti
- Registro e genere dei personaggi coerenti con l'originale (ricavati dalle
  altre lingue del gioco: francese, spagnolo, portoghese, tedesco e russo)

Problemi noti
-------------
- La lingua va scelta a mano (English, come spiegato sopra).
- All'avvio la schermata iniziale può comparire nella lingua del tuo sistema
  operativo: se succede, apri Opzioni → Lingua e scegli English.
- Testata su Steam/Linux con Wine. Windows nativo e Steam Deck non provati
  direttamente, ma lo script non fa niente di specifico per un sistema.

Segnalazioni
------------
Se trovi una battuta sbagliata, apri una issue su GitHub indicando capitolo,
battuta in inglese e battuta in italiano. Ogni stringa è identificata dal suo
id interno, quindi gli errori si correggono in modo mirato.

Nota finale: questa traduzione non è approvata da NEOWIZ o WONDER POTION, che
detengono tutti i diritti su SANABI. È fatta da un giocatore per passione,
gratis, e così deve restare.


--------------------------------------------------------------------------
2) GAMES TRANSLATORS (inglese)
--------------------------------------------------------------------------

TITLE: [IT] SANABI — complete fan translation (4,797 lines + UI), free patcher

Hello,

I finished a complete Italian translation of SANABI: every story line (4,797
dialogue entries, Prologue through Chapter 5 finale) plus DLC subtitles, menus
and UI strings. It is amateur, free and unofficial: it ships no game files and
requires an original copy.

How it works
------------
The game already ships eleven languages. The patcher writes Italian *into the
English slot*, so the file layout stays byte-for-byte compatible and none of
the other languages are touched. One consequence:

>>> after patching, pick ENGLISH in Options → Language. You select the entry
>>> called "English" and the game speaks Italian.

Install
-------
1. Download from <LINK> and unzip.
2. Linux / Steam Deck: open a terminal in patch_it_sanabi and run
       ./run_linux.sh --apply
   Windows: double-click run_windows.bat
3. Launch the game and set the language to English.

Only Python 3 (with UnityPy) is required; the scripts install it if missing.
No admin rights, no network access.

Dry run
-------
    ./run_linux.sh --check

Tells you how many strings match your installed version. Read-only.

Uninstall
---------
    ./run_linux.sh --restore

Restores the originals and verifies SHA-256 hashes. The patcher keeps its own
backup of every file it touches before writing anything.

Contents
--------
- 4,797 dialogue lines (main story + DLC), every markup token preserved
  ({B}, {!!}, [ss], [t:0.08], key-binding placeholders like [Jump]/[Dash])
- Interface and menus translated
- Register and gender agreement made consistent with the source, derived from
  the game's own French/Spanish/Portuguese/German/Russian text

Known issues
------------
- The language must be selected manually (English, see above).
- The title screen may appear in your OS language on boot; if so, open
  Options → Language and choose English.
- Tested on Linux/Wine. Native Windows and Steam Deck were not tested by me,
  but nothing in the script is platform-specific.

Feedback
--------
Open an issue on GitHub with the chapter, the English line and the Italian
line. Every string carries an internal id, so fixes are targeted.

This translation is not approved by NEOWIZ or WONDER POTION, who own all
rights to SANABI. It is made by a player for passion, free of charge, and must
stay that way.
