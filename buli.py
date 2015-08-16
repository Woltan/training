# -*- coding: utf-8 -*-
import argparse
import itertools
import random
import sys

def GetArguments(args):
	parser = argparse.ArgumentParser(description="Simuliert eine Bundsligasaison und erzeugt eine Tabelle der Saison.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	subparsers = parser.add_subparsers(dest="prog")
	
	erzeuge = subparsers.add_parser("erzeuge", help="Erzeugt eine Bundesligasaison")
	
	erzeuge.add_argument("teams", help="Liste von Teams nach denen ein Bundesligasaison simuliert wird.")
	erzeuge.add_argument("--output", "-o", default="Saison.dat", help="Ausgabedatei der Bundsligasaison.")

	tabelle = subparsers.add_parser("tabelle", help="Erzeugt eine Tabelle aus einer Bundesligasaison")
	
	tabelle.add_argument("saison", help="Bundesligasaison in der alle Begegnungen und Ergebnisse drin stehen.")
	
	return dict([(k.replace("-", "_"), v) for k, v in vars(parser.parse_args(args)).items()])

def Erzeuge(teams, output, **kwargs):
	with open(teams)as f:
		fTeams = [t.decode("utf-8") for t in f.read().split("\n") if len(t) > 0]
	
	spiele = list(itertools.combinations(fTeams, 2))
	
	spieltage = list()
	
	while len(spiele) > 0:
		spieltag = list()
		for spiel in spiele:
			if any(t in spieltag for t in spiel):
				continue
			
			spieltag.extend(spiel)
			
			if len(spieltag) >= len(fTeams):
				break
		else:
			spiele = spiele[1:] + [spiele[0]]
			continue
			
		spieltag = list(zip(spieltag[::2], spieltag[1::2]))
		spieltage.append(spieltag)
		
		for spiel in spieltag:
			spiele.remove(spiel)

	
	spieltage.extend([[(tAway, tHome) for tHome, tAway in spieltag] for spieltag in spieltage])
	
	tMax = max(map(len, fTeams))
	with open(output, "w") as f:
		for i, spieltag in enumerate(spieltage, 1):
			f.write("{:2}. Spieltag\n".format(i))
			for tHome, tAway in spieltag:
				f.write(unicode("{1:>{0}} vs. {2:<{0}} {3} : {4}\n").format(tMax, tHome, tAway, random.randint(0, 5), random.randint(0, 4)).encode("utf-8"))
			f.write("\n")

def Tabelle(saison, **kwargs):
	pass
	#Öffne die Saisondatei und lade alle Begegnungen in eine Liste
	
	#Erzeuge eine Dictionary das alle Teams als Keys enthält und als Values die entsprechenden Punkte und Tore
	
	#Gehe durch alle eingelesenen Begengungen und füge Punkte und Tore der entsprechenden Dictionaryeinträge hinzu
	
	#Sortiere das Dictionary und gib es in der Konsole aus

def main(args=sys.argv[1:]):
	kwargs = GetArguments(args)
	
	{"erzeuge": Erzeuge, "tabelle": Tabelle}[kwargs["prog"]](**kwargs)

if __name__ == "__main__":
	main()
	
