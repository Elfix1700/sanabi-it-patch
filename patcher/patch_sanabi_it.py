#!/usr/bin/env python3
"""
patch_sanabi_it.py — Traduzione italiana amatoriale per SANABI.

Strategy C: la traduzione italiana va nello slot della lingua INGLESE, che il
gioco già contiene in tutte le sue 11 lingue. Non si aggiunge nessuna lingua,
non si inventa nessun path_id, la struttura degli Addressables non cambia.

Punto FONDAMENTALE (scoperto verificando tutte le 4797 righe di dialogo):
l'ordine degli slot NON è costante tra i nodi. Lo stesso testo ha l'inglese
all'indice [3] nel 58% dei casi, a [2] nel 26% e a [1] nel 16%. Il gioco
risolve la lingua cercando la chiave giusta nell'array `keys`. Questo patcher
fa lo stesso: per ogni riga cerca lo slot la cui chiave è l'inglese, e
sostituisce SOLO se il testo inglese corrisponde all'hash salvato.

Uso:
    python3 patch_sanabi_it.py --check                 # solo verifica
    python3 patch_sanabi_it.py --apply                 # installa
    python3 patch_sanabi_it.py --restore               # ripristina
    python3 patch_sanabi_it.py --path <cartella gioco> --apply

Requisiti: Python 3.8+, UnityPy (pip install UnityPy). Nessun privilegio
particolare, nessuna connessione di rete.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

try:
    import UnityPy
except ImportError:
    print("ERRORE: serve UnityPy.  Installalo con:  pip install UnityPy")
    sys.exit(2)

VERSIONE_PATCH = "1.0.0"
VERSIONE_GIOCO_ATTESA = "1.3.53"

ENGLISH_PID = 7173981698464372551
UITEXTS_PID = 4393622352586803845
LANG_SETTING_PID = -7955205252535707744
FAKE_PID = -1234567890123456789
EN_INDEX_FALLBACK = 3

DATA_FILE = Path(__file__).resolve().parent / "data" / "translation_it.json.gz"
if not DATA_FILE.exists():
    DATA_FILE = Path(__file__).resolve().parent / "data" / "translation_it.json"

BUNDLE_DIALOGHI = [
    "dlcresources_assets_assets/_event/dlc/dlcmessenger.bundle",
    "dlcresources_assets_assets/_event/dlc/dlctext.bundle",
    "text_assets_assets/_text/prlg.bundle",
    "text_assets_assets/_text/chap1.bundle",
    "text_assets_assets/_text/chap2.bundle",
    "text_assets_assets/_text/chap3.bundle",
    "text_assets_assets/_text/chap4.bundle",
    "text_assets_assets/_text/chap5.bundle",
    "text_assets_assets/_text/ending.bundle",
]
BUNDLE_UI = "dataso_assets_all.bundle"
BUNDLE_LINGUA = "eventso_assets_all.bundle"

NOME_BACKUP = "backup_it_patch"
NOME_LOG = "patch_it.log"


# --------------------------------------------------------------------------- #
def log(msg, quiet=False):
    if not quiet:
        print(msg, flush=True)


def sha256_testo(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def carica_traduzione():
    if DATA_FILE.suffix == ".gz":
        import gzip
        with gzip.open(DATA_FILE, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def trova_gioco(path_arg):
    """Cerca la cartella del gioco."""
    if path_arg:
        p = Path(path_arg).expanduser().resolve()
        if (p / "SNB.exe").exists() or (p / "SNB_Data").exists():
            return p
        if (p / "SNB_Data/StreamingAssets/aa").exists():
            return p
        raise SystemExit(f"ERRORE: {p} non sembra la cartella di SANABI.")

    candidati = []
    env = os.environ.get("STEAM_COMPAT_INSTALL_PATH") or ""
    if env:
        candidati.append(Path(env))
    home = Path.home()
    for base in (home / ".steam/steam/steamapps/common/SANABI",
                 home / ".local/share/Steam/steamapps/common/SANABI",
                 home / "Games/SANABI",
                 home / "Games/Sanabi",
                 Path("/usr/local/games/SANABI"),
                 Path("C:/Program Files (x86)/Steam/steamapps/common/SANABI"),
                 Path("C:/Steam/steamapps/common/SANABI")):
        candidati.append(base)
    candidati.append(Path.cwd())
    for c in candidati:
        if not c or not c.is_dir():
            continue
        for sub in (c, c / "SANABI.v1.3.53.ALL.DLC"):
            if (sub / "SNB_Data/StreamingAssets/aa").is_dir():
                return sub
    raise SystemExit("ERRORE: cartella del gioco non trovata.\n"
                     "Uso: python3 patch_sanabi_it.py --path <cartella> --apply")


def aa_dir(gioco):
    return gioco / "SNB_Data/StreamingAssets/aa"


def live_dir(gioco):
    return aa_dir(gioco) / "StandaloneWindows64"


def indice_inglese(keys):
    """Indice dello slot la cui chiave è l'inglese (era hard-coded a 3:
    sbagliato, l'ordine cambia tra i nodi)."""
    for i, k in enumerate(keys):
        if getattr(k, "m_PathID", None) == ENGLISH_PID:
            return i
    return -1


def per_percorso(obj, path):
    cur = obj
    for part in path.split("."):
        if "[" in part:
            base, rest = part.split("[", 1)
            idx = int(rest.rstrip("]"))
            if base:
                cur = getattr(cur, base)
            cur = cur[idx]
        else:
            cur = getattr(cur, part)
    return cur


# --------------------------------------------------------------------------- #
def leggi_bundle(rel):
    env = UnityPy.load(str(rel))
    return env


def check(gioco, dati, quiet=False):
    """Dry-run: quante stringhe combaciano."""
    live = live_dir(gioco)
    if not live.is_dir():
        raise SystemExit(f"ERRORE: {live} non esiste.")

    # ---------- dialoghi ----------
    per_bundle = {}
    for e in dati["dialoghi"]:
        per_bundle.setdefault(e["bundle"], []).append(e)

    # stati distinti:
    #   gia   = lo slot contiene già l'italiano della patch
    #   ancora = lo slot ha l'inglese originale della patch (da tradurre)
    #   diverso = il testo non corrisponde a nessuno dei due (versione diversa)
    #   assente = oggetto/campo non trovato
    st = {"gia": 0, "ancora": 0, "diverso": 0, "assente": 0}
    copertura = {}
    for rel, entries in per_bundle.items():
        src = live / rel
        if not src.exists():
            st["assente"] += len(entries)
            copertura[rel] = (0, 0, 0, 0, len(entries))
            continue
        env = leggi_bundle(src)
        objs = {}
        for o in env.objects:
            if o.type.name == "MonoBehaviour":
                objs[o.path_id] = o
        b = {"gia": 0, "ancora": 0, "diverso": 0, "assente": 0}
        for e in entries:
            o = objs.get(e.get("path_id"))
            if o is None:
                st["assente"] += 1
                b["assente"] += 1
                continue
            try:
                d = o.read()
            except Exception:
                st["assente"] += 1
                b["assente"] += 1
                continue
            try:
                td = per_percorso(d, e["field"])
            except (AttributeError, IndexError):
                st["assente"] += 1
                b["assente"] += 1
                continue
            if td is None or not getattr(td, "values", None):
                st["assente"] += 1
                b["assente"] += 1
                continue
            vals = td.values
            if len(vals) != 11:
                st["assente"] += 1
                b["assente"] += 1
                continue
            i = indice_inglese(td.keys)
            if i < 0:
                i = EN_INDEX_FALLBACK
            h = sha256_testo(vals[i])
            if h == e["it_sha256"]:
                st["gia"] += 1
                b["gia"] += 1
            elif h == e["en_sha256"]:
                st["ancora"] += 1
                b["ancora"] += 1
            else:
                st["diverso"] += 1
                b["diverso"] += 1
        copertura[rel] = (b["gia"], b["ancora"], b["diverso"], b["assente"],
                          len(entries))

    # ---------- UI ----------
    uist = {"gia": 0, "ancora": 0, "diverso": 0, "assente": 0}
    src = live / BUNDLE_UI
    if src.exists():
        env = leggi_bundle(src)
        for o in env.objects:
            if o.path_id != UITEXTS_PID:
                continue
            d = o.read()
            tkd = d.textKeyDictionary
            for e in dati["ui"]:
                idx = e["index"]
                if idx >= len(tkd.valueData):
                    uist["assente"] += 1
                    continue
                vals = tkd.valueData[idx].values
                if len(vals) != 11:
                    uist["assente"] += 1
                    continue
                i = indice_inglese(tkd.valueData[idx].keys)
                if i < 0:
                    i = EN_INDEX_FALLBACK
                h = sha256_testo(vals[i])
                if h == e["it_sha256"]:
                    uist["gia"] += 1
                elif h == e["en_sha256"]:
                    uist["ancora"] += 1
                else:
                    uist["diverso"] += 1
            break

    log("", quiet) if not quiet else None
    print("=" * 62)
    print(" CONTROLLO TRADUZIONE ITALIANA (dry-run)")
    print("=" * 62)
    print(f"Gioco: {gioco}")
    print(f"Patch: v{VERSIONE_PATCH} — fatta per SANABI v{VERSIONE_GIOCO_ATTESA}")
    print()
    print("Dialoghi (già=italiano, ancora=inglese da tradurre, "
          "diverso=altro testo, assente=non trovato):")
    for rel in sorted(copertura):
        g, a, d_, n, t = copertura[rel]
        print(f"   {rel.split('/')[-1]:20s} {t:4d}  g={g:<4d} a={a:<4d} "
              f"d={d_:<3d} n={n:<3d}")
    print(f"   {'TOTALE':20s} {len(dati['dialoghi']):4d}  "
          f"g={st['gia']:<4d} a={st['ancora']:<4d} d={st['diverso']:<3d} "
          f"n={st['assente']:<3d}")
    print()
    print(f"UI: {len(dati['ui'])}  g={uist['gia']:<4d} a={uist['ancora']:<4d} "
          f"d={uist['diverso']:<3d} n={uist['assente']:<3d}")
    print()

    tutti = st["gia"] + uist["gia"]
    totale = len(dati["dialoghi"]) + len(dati["ui"])
    if tutti == totale:
        print(f"ESITO: traduzione GIÀ INSTALLATA e verificata "
              f"({tutti}/{totale} stringhe).")
        return 0
    if st["diverso"] or uist["diverso"] or st["assente"] or uist["assente"]:
        print(f"ESITO: {tutti}/{totale} già tradotte, {st['ancora'] + uist['ancora']} "
              f"da tradurre,")
        print(f"       {st['diverso'] + uist['diverso']} non corrispondenti e "
              f"{st['assente'] + uist['assente']} non trovate.")
        print("       Le stringhe non corrispondenti vengono saltate: "
              "probabilmente è una")
        print("       versione diversa del gioco. Esegui --apply per "
              "tradurre quelle che combaciano.")
        return 0
    print(f"ESITO: {st['ancora'] + uist['ancora']} stringhe da tradurre. "
          f"Esegui con --apply per installare.")
    return 0


def apply_patch(gioco, dati, quiet=False):
    live = live_dir(gioco)
    aa = aa_dir(gioco)
    backup = aa / NOME_BACKUP
    if backup.exists():
        # se la traduzione è già tutta applicata, non è un errore: idempotente
        try:
            if check(gioco, dati, quiet=True) == 0 and traduzione_completa(gioco, dati):
                print("La traduzione è già installata e verificata: "
                      "nessuna operazione necessaria.")
                return
        except Exception:
            pass
        raise SystemExit(
            f"ERRORE: esiste già {backup}.\n"
            "Se vuoi ripartire da zero: --restore e poi di nuovo --apply.")

    # 1) crea il backup degli originali
    toccati = BUNDLE_DIALOGHI + [BUNDLE_UI, BUNDLE_LINGUA]
    manifest = []
    for rel in toccati:
        src = live / rel
        if not src.exists():
            raise SystemExit(f"ERRORE: bundle mancante {rel}")
        dst = backup / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        manifest.append({"rel": rel,
                         "sha256": sha256_file(dst),
                         "dimensione": dst.stat().st_size})
    (backup / "manifest.json").write_text(
        json.dumps({"versione_patch": VERSIONE_PATCH,
                    "creato": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "file": manifest}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(f"Backup creato in: {backup}")

    # 2) patcha i bundle
    patcha_dialoghi(gioco, dati, live)
    patcha_ui(gioco, dati, live)
    patcha_lingua(gioco, live)

    # 3) log
    logf = aa / NOME_LOG
    with open(logf, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] applicata patch "
                f"v{VERSIONE_PATCH} a {gioco}\n")
    print()
    print("=" * 62)
    print(" PATCH APPLICATA")
    print("=" * 62)
    print("Per avere i testi in italiano: avvia il gioco e seleziona")
    print("la lingua **English** nel menu Opzioni → Lingua.")
    print()
    print(f"Per disinstallare: python3 {Path(__file__).name} --restore")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def traduzione_completa(gioco, dati):
    """True se ogni slot inglese contiene già l'italiano atteso."""
    live = live_dir(gioco)
    per_bundle = {}
    for e in dati["dialoghi"]:
        per_bundle.setdefault(e["bundle"], []).append(e)
    for rel, entries in per_bundle.items():
        src = live / rel
        if not src.exists():
            return False
        env = leggi_bundle(src)
        objs = {o.path_id: o for o in env.objects
                if o.type.name == "MonoBehaviour"}
        for e in entries:
            o = objs.get(e.get("path_id"))
            if o is None:
                return False
            try:
                d = o.read()
                td = per_percorso(d, e["field"])
            except Exception:
                return False
            if td is None or not getattr(td, "values", None):
                return False
            vals = td.values
            if len(vals) != 11:
                return False
            i = indice_inglese(td.keys)
            if i < 0:
                i = EN_INDEX_FALLBACK
            if sha256_testo(vals[i]) != e["it_sha256"]:
                return False
    return True


def patcha_dialoghi(gioco, dati, live):
    """Modifica TUTTI i campi di un oggetto in memoria e salva UNA SOLA VOLTA
    per oggetto: chiamare save() dopo ogni campo fa perdere le modifiche
    precedenti (bug verificato sulle SelectionNode)."""
    per_bundle = {}
    for e in dati["dialoghi"]:
        per_bundle.setdefault(e["bundle"], []).append(e)
    tot_ok = tot_no = 0
    for rel, entries in per_bundle.items():
        src = live / rel
        env = UnityPy.load(str(src))
        objs = {o.path_id: o for o in env.objects if o.type.name == "MonoBehaviour"}

        # raggruppa per path_id, conservando l'ordine dei campi
        per_obj = {}
        ordine = []
        for e in entries:
            pid = e.get("path_id")
            if pid not in per_obj:
                per_obj[pid] = []
                ordine.append(pid)
            per_obj[pid].append(e)

        n_ok = n_no = 0
        for pid in ordine:
            o = objs.get(pid)
            if o is None:
                n_no += len(per_obj[pid])
                continue
            try:
                d = o.read()
            except Exception:
                n_no += len(per_obj[pid])
                continue
            modificato = False
            for e in per_obj[pid]:
                try:
                    td = per_percorso(d, e["field"])
                except (AttributeError, IndexError):
                    n_no += 1
                    continue
                if td is None or not getattr(td, "values", None):
                    n_no += 1
                    continue
                vals = td.values
                if len(vals) != 11:
                    n_no += 1
                    continue
                i = indice_inglese(td.keys)
                if i < 0:
                    i = EN_INDEX_FALLBACK
                # sostituisci solo se il testo combacia (inglese o già tradotto)
                h = sha256_testo(vals[i])
                if h != e["en_sha256"] and h != e["it_sha256"]:
                    n_no += 1
                    continue
                vals[i] = e["it"]
                modificato = True
                n_ok += 1
            if modificato:
                d.save()
                o.assets_file.save()
        for _n, bf in env.files.items():
            bf.mark_changed()
        tmp = live.parent / (rel.split("/")[-1] + ".tmp")
        env.save(pack="lz4", out_path=str(live.parent))
        # UnityPy scrive con il nome interno: sistema il percorso
        prodotto = live.parent / rel.split("/")[-1]
        dst = live / rel
        if prodotto.exists() and prodotto.resolve() != dst.resolve():
            dst.parent.mkdir(parents=True, exist_ok=True)
            prodotto.replace(dst)
        if tmp.exists():
            tmp.unlink()
        print(f"   {rel.split('/')[-1]:22s} {n_ok:4d} tradotte, {n_no:3d} saltate")
        tot_ok += n_ok
        tot_no += n_no
    print(f"   {'TOTALE':22s} {tot_ok:4d} tradotte, {tot_no:3d} saltate")


def patcha_ui(gioco, dati, live):
    src = live / BUNDLE_UI
    env = UnityPy.load(str(src))
    for o in env.objects:
        if o.path_id != UITEXTS_PID:
            continue
        d = o.read()
        tkd = d.textKeyDictionary
        n_ok = n_no = 0
        for e in dati["ui"]:
            idx = e["index"]
            if idx >= len(tkd.valueData):
                n_no += 1
                continue
            vals = tkd.valueData[idx].values
            if len(vals) != 11:
                n_no += 1
                continue
            i = indice_inglese(tkd.valueData[idx].keys)
            if i < 0:
                i = EN_INDEX_FALLBACK
            h = sha256_testo(vals[i])
            if h != e["en_sha256"] and h != e["it_sha256"]:
                n_no += 1
                continue
            vals[i] = e["it"]
            n_ok += 1
        d.save()
        o.assets_file.save()
        print(f"   UI                     {n_ok:4d} tradotte, {n_no:3d} saltate")
        break
    for _n, bf in env.files.items():
        bf.mark_changed()
    env.save(pack="lz4", out_path=str(live.parent))
    prodotto = live.parent / BUNDLE_UI
    dst = live / BUNDLE_UI
    if prodotto.exists() and prodotto.resolve() != dst.resolve():
        prodotto.replace(dst)


def patcha_lingua(gioco, live):
    """Mette la lingua inglese come corrente ( lo slot che contiene l'italiano)."""
    src = live / BUNDLE_LINGUA
    env = UnityPy.load(str(src))
    for o in env.objects:
        if o.path_id != LANG_SETTING_PID:
            continue
        d = o.read()
        pids = [l.m_PathID for l in d.languages]
        if ENGLISH_PID in pids and FAKE_PID not in pids:
            idx = pids.index(ENGLISH_PID)
            d.currentLanguage = d.languages[idx]
            d.languageIndex = idx
            d.save()
            o.assets_file.save()
            print(f"   Lingua corrente        -> English (indice {idx}), "
                  f"{len(pids)} lingue conservate")
        else:
            print("   Lingua corrente        ! attenzione: lingua inglese non "
                  "trovata o path_id sospetto")
        break
    for _n, bf in env.files.items():
        bf.mark_changed()
    env.save(pack="lz4", out_path=str(live.parent))
    prodotto = live.parent / BUNDLE_LINGUA
    dst = live / BUNDLE_LINGUA
    if prodotto.exists() and prodotto.resolve() != dst.resolve():
        prodotto.replace(dst)


def restore(gioco, quiet=False):
    aa = aa_dir(gioco)
    backup = aa / NOME_BACKUP
    if not backup.exists():
        raise SystemExit(f"ERRORE: nessun backup in {backup}.")
    man = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    live = live_dir(gioco)
    ok = bad = 0
    for e in man["file"]:
        src = backup / e["rel"]
        if not src.exists():
            print(f"   ! manca {e['rel']}")
            bad += 1
            continue
        dst = live / e["rel"]
        # controlla prima che il backup stesso sia integro
        if sha256_file(src) != e["sha256"]:
            print(f"   ! backup corrotto: {e['rel']}")
            bad += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if sha256_file(dst) == e["sha256"]:
            ok += 1
        else:
            print(f"   ! hash diverso dopo il ripristino: {e['rel']}")
            bad += 1
    print(f"Ripristinati {ok} file originali su {len(man['file'])}, "
          f"{bad} problemi.")
    if bad == 0:
        # rimuove il backup, così si può subito riapplicare la patch
        shutil.rmtree(backup)
        print("Backup rimosso: il gioco è esattamente come prima e si può "
              "riapplicare la patch.")
    else:
        print("ATTENZIONE: backup conservato perché non tutti i file sono "
              "stati ripristinati correttamente.")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(
        description="Traduzione italiana amatoriale per SANABI (Strategy C).")
    ap.add_argument("--path", help="cartella del gioco")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="solo verifica")
    g.add_argument("--apply", action="store_true", help="installa")
    g.add_argument("--restore", action="store_true", help="ripristina")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    gioco = trova_gioco(a.path)
    if a.restore:
        sys.exit(restore(gioco, a.quiet))

    dati = carica_traduzione()
    m = dati["meta"]
    print(f"Patch v{m['versione_patch']} — {m['totale_stringhe']} stringhe "
          f"({m['stringhe_dialoghi']} dialoghi, {m['stringhe_ui']} UI)")
    print()
    if a.apply:
        apply_patch(gioco, dati, a.quiet)
    else:
        sys.exit(check(gioco, dati, a.quiet))


if __name__ == "__main__":
    main()
