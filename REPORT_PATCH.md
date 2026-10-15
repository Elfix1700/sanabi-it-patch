REPORT_PATCH.md — test della patch universale
==============================================

Tutti gli output qui riportati sono prodotti dagli script del repository e sono
stati eseguiti su una copia reale del gioco (SANABI v1.3.53, 832 bundle
Addressables).

Ambiente di test: Linux, Wine (`/home/elfix/wine-test`), Python 3.14, UnityPy.


## 1. Contenuto verificato contro la build di riferimento
---------------------------------------------------------

Il patcher, applicato a un gioco pulito, produce bundle **identici byte a byte**
(md5) a quelli della build verificata dell'autore:

```
identici: 11/11  diversi: 0
IDENTICI  dlcresources_assets_assets/_event/dlc/dlcmessenger.bundle
IDENTICI  dlcresources_assets_assets/_event/dlc/dlctext.bundle
IDENTICI  text_assets_assets/_text/prlg.bundle
IDENTICI  text_assets_assets/_text/chap1.bundle
IDENTICI  text_assets_assets/_text/chap2.bundle
IDENTICI  text_assets_assets/_text/chap3.bundle
IDENTICI  text_assets_assets/_text/chap4.bundle
IDENTICI  text_assets_assets/_text/chap5.bundle
IDENTICI  text_assets_assets/_text/ending.bundle
IDENTICI  dataso_assets_all.bundle
IDENTICI  eventso_assets_all.bundle
```


## 2. --check su gioco pulito (dry-run)
---------------------------------------

```
Dialoghi (già=italiano, ancora=inglese da tradurre, diverso=altro testo, assente=non trovato):
   dlcmessenger.bundle    60  g=1    a=59   d=0   n=0
   dlctext.bundle        458  g=10   a=448  d=0   n=0
   chap1.bundle          681  g=26   a=655  d=0   n=0
   chap2.bundle          523  g=14   a=509  d=0   n=0
   chap3.bundle          821  g=26   a=795  d=0   n=0
   chap4.bundle          836  g=28   a=808  d=0   n=0
   chap5.bundle          887  g=11   a=876  d=0   n=0
   ending.bundle          52  g=0    a=52   d=0   n=0
   prlg.bundle           479  g=15   a=464  d=0   n=0
   TOTALE               4797  g=131  a=4666 d=0   n=0

UI: 178  g=31   a=147  d=0   n=0

ESITO: 4813 stringhe da tradurre. Esegui con --apply per installare.
```

`g` = lo slot contiene già l'italiano (stringhe identiche in entrambe le lingue:
nomi, numeri)
`a` = lo slot ha l'inglese originale, da tradurre
`d` = il testo non corrisponde a nessuno dei due (versione diversa)
`n` = oggetto o campo non trovato


## 3. --apply
-----------

```
   dlcmessenger.bundle      60 tradotte,   0 saltate
   dlctext.bundle          458 tradotte,   0 saltate
   prlg.bundle             479 tradotte,   0 saltate
   chap1.bundle            681 tradotte,   0 saltate
   chap2.bundle            523 tradotte,   0 saltate
   chap3.bundle            821 tradotte,   0 saltate
   chap4.bundle            836 tradotte,   0 saltate
   chap5.bundle            887 tradotte,   0 saltate
   ending.bundle            52 tradotte,   0 saltate
   TOTALE                 4797 tradotte,   0 saltate
   UI                      178 tradotte,   0 saltate
   Lingua corrente        -> English (indice 1), 11 lingue conservate
```


## 4. --apply ripetuto (idempotenza)
------------------------------------

```
ESITO: traduzione GIÀ INSTALLATA e verificata (4975/4975 stringhe).
La traduzione è già installata e verificata: nessuna operazione necessaria.
RC_APPLY2=0
```


## 5. Versione diversa del gioco (stringhe non corrispondenti)
-------------------------------------------------------------

5 testi inglesi di `prlg.bundle` alterati artificialmente:

```
   prlg.bundle           479  g=474  a=0    d=5   n=0
   TOTALE               4797  g=4792 a=0    d=5   n=0

ESITO: 4970/4975 già tradotte, 0 da tradurre,
       5 non corrispondenti e 0 non trovate.
       Le stringhe non corrispondenti vengono saltate: probabilmente è una
       versione diversa del gioco.
```

Nessun crash, nessuna scrittura sulle stringhe non riconosciute.


## 6. --restore e verifica contro l'originale
---------------------------------------------

```
Ripristinati 11 file originali su 11, 0 problemi.
Backup rimosso: il gioco è esattamente come prima e si può riapplicare la patch.
RC_RESTORE=0
bundle identici all'originale dopo restore: 832/832
```


## 7. Contenuti della traduzione
--------------------------------

| elemento | valore |
|---|---|
| righe di dialogo | 4.797 |
| righe di interfaccia | 178 (190 totali − 12 senza equivalente in inglese) |
| totale stringhe | 4.975 |
| lingue nel gioco | 11 (invariate) |
| lingue aggiunte | 0 |
| path_id inventati | 0 |
| slot diversi dall'inglese modificati | 0 |
| token di markup alterati | 0 |

I 162 trafiletti di differenza tra 190 e 178 sono le voci UIText il cui valore
nello slot inglese è vuoto: non c'è niente da tradurre e sono escluse dai
controlli Hash.


## 8. Cosa NON è stato testato
------------------------------

- **Windows nativo**: il patcher è Python puro e non chiama niente di specifico
  di Linux, ma non è stato eseguito su Windows. L'eseguibile compilato dal
  workflow GitHub Actions non è stato provato.
- **Steam Deck**: idem, non provato direttamente.
- **Versioni diverse da 1.3.53**: solo la versione indicata è stata testata.
  Sulle altre il patcher salta e segnala le stringhe che non corrispondono.
- **Altre installazioni del gioco**: una sola cartella di gioco è stata usata
  per i test. La ricerca automatica della cartella è stata provata solo
  implicita (percorso passato a mano).
- **Avvio con il patcher al posto della build dell'autore**: la build verificata
  e l'output del patcher sono identici byte a byte, quindi il comportamento a
  gioco avviato è lo stesso; l'avvio vero con il patcher non è stato ripetuto.


## 9. Problema noto della lingua
--------------------------------

La patch mette l'italiano nello slot inglese, quindi **nel menu Opzioni →
Lingua bisogna selezionare "English"**. Le altre lingue restano intatte.

Sperimentalmente, nel prefisso Wine dell'autore il gioco parte in **tedesco**
invece che in inglese, pur avendo il `LanguageSetting` puntato sull'inglese
(`currentLanguage` = inglese, `languageIndex` = 1, verificati dentro il bundle).
Il gioco ha una classe `LanguageSetting` con un campo `systemLanguage` per ogni
lingua (enum `SystemLanguage` di Unity: English = 10, German = 15, Korean = 23,
ecc.) e usa `Application.systemLanguage`. Modificare quel campo **non** cambia
la lingua scelta, quindi la selezione iniziale non dipende da `currentLanguage`.

Conseguenza pratica: all'avvio la schermata iniziale può comparire nella lingua
del sistema operativo. Basta aprire Opzioni → Lingua e scegliere English.
Documentato in `README_IT.md` e `README_EN.md` tra i problemi noti.
