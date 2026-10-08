#!/usr/bin/env python3
"""EAN-13 Hilfen für GS1-Nummern.

  python3 scripts/ean_tools.py check 4255822600181
  python3 scripts/ean_tools.py used  data/otto_performance_2026-10-08.csv
  python3 scripts/ean_tools.py propose --prefix 4255822 --csvs data/otto_performance_2026-10-08.csv \
         --skus data/spiegel_sets_texte_charge1.csv data/salzlampen_geschenksets_texte.csv --out data/ean_vorschlaege.csv

propose vergibt nur VORSCHLÄGE ab der ersten Nummer nach der höchsten bereits genutzten. Ob die Nummern in deinem
bei GS1 lizenzierten Bereich liegen und frei sind, muss im GS1-Portal geprüft werden, bevor sie bei Amazon eingetragen werden.
"""
import argparse
import csv
import re
import sys


def check_digit(first12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(first12))
    return (10 - s % 10) % 10


def valid(ean):
    return bool(re.fullmatch(r"\d{13}", ean)) and int(ean[12]) == check_digit(ean[:12])


def read_used(paths, prefix):
    used = set()
    for p in paths:
        with open(p, encoding="utf-8-sig") as f:
            for m in re.findall(r"\b\d{13}\b", f.read()):
                if m.startswith(prefix):
                    used.add(m)
    return used


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "used", "propose"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--prefix", default="4255822")
    ap.add_argument("--csvs", nargs="*", default=[])
    ap.add_argument("--skus", nargs="*", default=[])
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.cmd == "check":
        for e in a.args:
            print(e, "gültig" if valid(e) else "UNGÜLTIG (Prüfziffer " + str(check_digit(e[:12])) + ")")
        return

    paths = a.args if a.cmd == "used" else a.csvs
    used = read_used(paths, a.prefix)
    bad = sorted(e for e in used if not valid(e))
    refs = sorted(int(e[len(a.prefix):12]) for e in used)
    if a.cmd == "used":
        print(f"{len(used)} genutzte GTINs mit Präfix {a.prefix}, Artikelnummern {refs[0]} bis {refs[-1]}")
        print("mit falscher Prüfziffer:", bad or "keine")
        return

    width = 12 - len(a.prefix)
    nxt = refs[-1] + 1
    rows = []
    for path in a.skus:
        with open(path, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                base = a.prefix + str(nxt).zfill(width)
                rows.append([r["sku"], base + str(check_digit(base)), path])
                nxt += 1
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "gtin_vorschlag", "quelle"])
        w.writerows(rows)
    print(f"{len(rows)} Vorschläge in {a.out}, ab Artikelnummer {refs[-1] + 1}")
    print("WICHTIG: Bereich und Verfügbarkeit im GS1-Portal prüfen und die Nummern dort den Produkten zuordnen.")


if __name__ == "__main__":
    main()
