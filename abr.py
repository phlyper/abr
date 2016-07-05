# >python -m py_compile abr.py
import sys, pickle;
from datetime import datetime;
import time, random;
# pip install graphviz *** graphviz-0.4.2
from graphviz import Digraph
__author__ = "Phlyper";

# STRUCT {valeur, [pere], [fils_gauche], [fils_droit]}

def est_vide(abr = None):
	return abr == None;

def valeur(abr = None):
	if abr != None:
		return abr["valeur"];
	return None;

def pere(abr = None):
	if abr != None:
		return abr["pere"];
	return None;

def fils_gauche(abr = None):
	if abr != None:
		return abr["fils_gauche"];
	return None;

def fils_droit(abr = None):
	if abr != None:
		return abr["fils_droit"];
	return None;

def insertion(abr = None, pere = None, v = None):
	if v == None:
		return None;
	if abr != None:
		if abr["valeur"] > v:
			abr["fils_gauche"] = insertion(abr["fils_gauche"], abr, v);
		else:
			abr["fils_droit"] = insertion(abr["fils_droit"], abr, v);
	else:
		abr = {};
		abr["valeur"] = v;
		abr["pere"] = pere;
		#abr["pere"]["fils_gauche"] = abr;
		#abr["pere"]["fils_droit"] = abr;
		abr["fils_gauche"] = None;
		abr["fils_droit"] = None;
	return abr;

def insertion_liste(abr = None, list_v = []):
	for v in list_v:
		abr = insertion(abr, pere = None, v = v);
	return abr;

def est_abr(abr = None):
	if abr != None:
		if abr["fils_gauche"] != None and max_val(abr["fils_gauche"]) > abr["valeur"]:
			return False;

		if abr["fils_droit"] != None and min_val(abr["fils_droit"]) < abr["valeur"]:
			return False;

		if not est_abr(abr["fils_gauche"]) or not est_abr(abr["fils_gauche"]):
			return False;

	return True; 

def afficher(abr = None):
	if abr != None:
		print("Noeud * @ %#010x" % id(abr));
		print("valeur =", abr["valeur"]);
		if abr["pere"] != None:
			print("\tpere =", abr["pere"]["valeur"]);
		if abr["fils_gauche"] != None:
			print("\tfils_gauche =", abr["fils_gauche"]["valeur"]);
		if abr["fils_droit"] != None:
			print("\tfils_droit =", abr["fils_droit"]["valeur"]);
		print("");
		afficher(abr["fils_gauche"]);
		afficher(abr["fils_droit"]);

def print_arbre(abr = None, level = 0):
	sep = 5;
	if level == 0:
		print("*" * 60);
	if abr != None:
		print_arbre(abr["fils_droit"], level + 1);
		if level > 0:
			for i in range(0, level-1):
				print("|%s" % (" " * sep), end = "");
			print("|%s>%03d" % ("-" * sep, abr["valeur"]));
		else:
			print("%02d" % (abr["valeur"]));
		print_arbre(abr["fils_gauche"], level + 1);
	if level == 0:
		print("\npaths =", paths(abr));
		print("*" * 60);
		
def draw_arbre(abr = None, fils = None, pere = None, dot = None, kn = 0):
	kn += 1;
	if abr != None:
		if abr["pere"] == None:
			dot = Digraph(format = "png", name = "ABR", comment = "The Binary Search Tree");
		if dot == None:
			return;
		
		abr["kn"] = kn;
		label = "A%d" % kn;
		dot.node(label, "{<valeur> %s|{<fils_gauche> %s|<fils_droit> %s}}" % (abr["valeur"], abr["fils_gauche"]["valeur"] if abr["fils_gauche"] != None else None, abr["fils_droit"]["valeur"] if abr["fils_droit"] else None), shape = "Mrecord" if abr["pere"] == None else "record", fontsize="14");
		if abr["pere"] != None:
			label_pere = "A%d" % abr["pere"]["kn"];
			label_pere = "%s%s" % (label_pere, ":fils_%s" % fils if fils != None else "");
			label = "%s:valeur" % label
			dot.edge(label_pere, label, constraint = "true", dir = "both", arrowhead = "normal", color = "blue");
		kn = draw_arbre(abr["fils_gauche"], "gauche", abr, dot, kn);
		kn = draw_arbre(abr["fils_droit"], "droit", abr, dot, kn);
		del abr["kn"];
		
		if abr["pere"] == None:
			dot.body.append("\tlabel = \"ABR Arbre Binaire de Recherche - BST Binary Search Tree - Diagram drawn by graphviz - @PHLYPER\"");
			dot.body.append("\tfontsize = 20");
			print(dot.source);
			print(dot.save("abr"));
			print(dot.render("abr", view = True, cleanup = False));
			# dot.engine("neato");
			# dot.format("pdf");
			# print(dot.render("abr", view = True, cleanup = False));
	else:
		label = "A%d" % kn;
		dot.node(label, "None", style = "filled", fillcolor = "lightgrey", fontsize="12");
		if pere != None:
			label_pere = "A%d" % pere["kn"];
			dot.edge(label_pere, label, constraint = "true", dir = "both", color = "blue");
	return kn;

def recherche(abr = None, v = None):
	if v == None:
		return None;
	if abr != None:
		if abr["valeur"] == v:
			return abr;
		elif abr["valeur"] > v:
			return recherche(abr["fils_gauche"], v);
		else:
			return recherche(abr["fils_droit"], v);
	return None;

def modifie(abr = None, v1 = None, v2 = None):
	if v2 == None:
		return abr;
	if abr != None:
		x = recherche(abr, v1);
		if x != None:
			if x["pere"]["fils_gauche"] == x:
				x["pere"]["fils_gauche"] = None;
			if x["pere"]["fils_droit"] == x:
				x["pere"]["fils_droit"] = None;
			abr = insertion(abr, None, v2);
			abr = fusion(abr, x["fils_gauche"]);
			abr = fusion(abr, x["fils_droit"]);
			x = vider(x);
	return abr;

def fusion(abr = None, abr2 = None):
	if abr2 != None:
		abr = insertion(abr, None, abr2["valeur"]);
		abr = fusion(abr, abr2["fils_gauche"]);
		abr = fusion(abr, abr2["fils_droit"]);
	return abr;

def copy(abr = None, pere = None):
	abr2 = None;
	if abr != None:
		abr2 = insertion(abr2, None, abr["valeur"]);
		abr2["pere"] = pere;
		abr2["fils_gauche"] = copy(abr["fils_gauche"], pere = abr2);
		abr2["fils_droit"] = copy(abr["fils_droit"], pere = abr2);
	return abr2;

def mirror(abr = None, pere = None):
	abr2 = None;
	if abr != None:
		if abr["pere"] == None:
			abr2 = copy(abr);
		else:
			abr2 = {"valeur" : abr["valeur"], "pere" : pere};
		abr2["fils_gauche"] = mirror(abr["fils_droit"], abr2);
		abr2["fils_droit"] = mirror(abr["fils_gauche"], abr2);
	return abr2;

def paths(abr = None):
	path = [];
	if abr != None:
		if abr["fils_gauche"] == None and abr["fils_droit"] == None:
			path.append([valeur(abr)]);
		else:
			lg = paths(abr["fils_gauche"]);
			if len(lg):
				for p in lg:
					if len(p):
						p.append(valeur(abr));
				path += lg;
			ld = paths(abr["fils_droit"]);
			if len(ld):
				for p in ld:
					if len(p):
						p.append(valeur(abr));
				path += ld;
	return path;

def extrait_max(abr = None):
	if abr != None:
		max = noeud_max(abr);
		if max != None:
			max["pere"]["fils_droit"] = None;
			abr = fusion(abr, max["fils_gauche"]);
			abr = fusion(abr, max["fils_droit"]);
			max = vider(max);
	return abr;

def extrait_min(abr = None):
	if abr != None:
		min = noeud_min(abr);
		if min != None:
			min["pere"]["fils_gauche"] = None;
			abr = fusion(abr, min["fils_gauche"]);
			abr = fusion(abr, min["fils_droit"]);
			min = vider(min);
	return abr;

def arbre_to_list(abr = None):
	l = [];
	if abr != None:
		lg = arbre_to_list(abr["fils_gauche"]);
		if len(lg):
			l += lg;
		l.append(abr["valeur"]);
		ld = arbre_to_list(abr["fils_droit"]);
		if len(ld):
			l += ld;
	return l;

def racine(abr = None):
	if abr != None:
		if abr["pere"] == None:
			return abr;
	return None;

def noeuds_internes(abr = None):
	ns = [];
	if abr != None:
		lg = noeuds_internes(abr["fils_gauche"]);
		if len(lg):
			ns += lg;
		if abr["pere"] != None and (abr["fils_gauche"] != None or abr["fils_droit"] != None):
			ns.append(abr["valeur"]);
		ld = noeuds_internes(abr["fils_droit"]);
		if len(ld):
			ns += ld;
	return ns;

def feuilles(abr = None): # noeuds externes
	fs = [];
	if abr != None:
		lg = feuilles(abr["fils_gauche"]);
		if len(lg):
			fs += lg;
		if abr["fils_gauche"] == None and abr["fils_droit"] == None:
			fs.append(abr["valeur"]);
		ld = feuilles(abr["fils_droit"]);
		if len(ld):
			fs += ld;
	return fs;

def successeur(abr = None, v = None):
	if abr != None:
		x = recherche(abr, v);
		if x != None:
			if x["fils_droit"] != None:
				min = noeud_min(x["fils_droit"]);
				if min != None:
					return min;
			elif x["fils_droit"] == None and x["pere"] != None:
				while x["pere"] != None:
					x = x["pere"];
					if  x["valeur"] > v:
						return x;
	return None;
	
def predecesseur(abr = None, v = None):
	if abr != None:
		x = recherche(abr, v);
		if x != None:
			if x["fils_gauche"] != None:
				max = noeud_max(x["fils_gauche"]);
				if max != None:
					return max;
			elif x["fils_gauche"] == None and x["pere"] != None:
				while x["pere"] != None:
					x = x["pere"];
					if  x["valeur"] < v:
						return x;
	return None;

def plus_proche(abr = None, v = None):
	if v == None:
		return None;
	pp = None;
	if abr != None:
		pp = abr;
		ppg = plus_proche(abr["fils_gauche"], v);
		if ppg != None:
			if abs(v - abr["valeur"]) > abs(v - ppg["valeur"]):
				pp = ppg;
		ppd = plus_proche(abr["fils_droit"], v);
		if ppd != None:
			if abs(v - abr["valeur"]) > abs(v - ppd["valeur"]):
				pp = ppd;
	return pp;

def nbr_noeuds(abr = None):
	if abr != None:
		return nbr_noeuds(abr["fils_gauche"]) + nbr_noeuds(abr["fils_droit"]) + 1;
	return 0;

def noeud_max(abr = None):
	if abr != None:
		if abr["fils_droit"] != None:
			return noeud_max(abr["fils_droit"]);
		return abr;
	return None;

def max_val(abr = None):
	return valeur(noeud_max(abr));

def noeud_min(abr = None):
	if abr != None:
		if abr["fils_gauche"] != None:
			return noeud_min(abr["fils_gauche"]);
		return abr;
	return None;

def min_val(abr = None):
	return valeur(noeud_min(abr));

def hauteur(abr = None):
	if abr != None:
		return max(hauteur(abr["fils_gauche"]), hauteur(abr["fils_droit"])) + 1;
	return 0;

def balance(abr = None):
	if abr != None:
		return hauteur(abr["fils_gauche"]) - hauteur(abr["fils_droit"]);
	return 0;

def est_equilibrer(abr = None):
	return balance(abr) in [-1, 0, 1];

def vider(abr = None):
	if abr != None:
		abr["pere"] = None;
		abr["fils_gauche"] = vider(abr["fils_gauche"]);
		abr["fils_droit"] = vider(abr["fils_droit"]);
		
		abr.clear();
		abr = None;
		del abr;
		#if abr:
			#print("free %s", abr);
	return None;

def save_arbre(abr = None):
	with open("abr.bin", "wb") as f:
		pickle.dump(abr, f);

def open_arbre():
	abr = None;
	with open("abr.bin", "rb") as f:
		abr = pickle.load(f);
	return abr;

def cmp_arbre(abr = None, abr2 = None):
	result = [];
	if abr != None and abr2 != None:
		result.append([abr["valeur"], "==" if abr["valeur"] == abr2["valeur"] else "<>", abr2["valeur"]]);
		lg = cmp_arbre(abr["fils_gauche"], abr2["fils_gauche"]);
		if len(lg):
			result += lg;
		ld = cmp_arbre(abr["fils_droit"], abr2["fils_droit"]);
		if len(ld):
			result += ld;
	elif abr != None and abr2 == None:
		result.append([abr["valeur"], "<>", None]);
		lg = cmp_arbre(abr["fils_gauche"], None);
		if len(lg):
			result += lg;
		ld = cmp_arbre(abr["fils_droit"], None);
		if len(ld):
			result += ld;
	elif abr == None and abr2 != None:
		result.append([None, "<>", abr2["valeur"]]);
		lg = cmp_arbre(None, abr2["fils_gauche"]);
		if len(lg):
			result += lg;
		ld = cmp_arbre(None, abr2["fils_droit"]);
		if len(ld):
			result += ld;
	else:
		result.append([None, "==", None]);
	return result;

def est_egaux(abr = None, abr2 = None):
	result = cmp_arbre(abr, abr2);
	print(result);
	for x in result:
		if x[1] == "<>":
			return False;
	return True;

def main():
	ABR = None;
	ABR2 = None;
	ABR3 = None;
	ABR4, ABR5 = None, None;
	print("ABR");
	print("insertion");
	ABR = insertion(ABR, None, 5);
	ABR = insertion(ABR, None, 1);
	ABR = insertion(ABR, None, 8);
	ABR = insertion(ABR, None, 15);
	ABR = insertion_liste(ABR, [10, 12, 4, 6, 2, 14]);
	ABR2 = insertion_liste(ABR2, [11, 3, 16, 9, 13, 7]);
	print("est vide", est_vide(ABR));
	print("pere", pere(ABR));
	print("fils_gauche", fils_gauche(ABR));
	print("fils_droit", fils_droit(ABR));
	print("afficher");
	afficher(ABR);
	ABR = fusion(ABR, ABR2);
	print("afficher apres fusion");
	afficher(ABR);
	print("nbr noeuds", nbr_noeuds(ABR));
	print("min val", min_val(ABR));
	print("max val", max_val(ABR));
	print("hauter", hauteur(ABR));
	print("recherche(14)", recherche(ABR, 14));
	print("ABR2");
	print("afficher");
	afficher(ABR2);
	ABR2 = extrait_max(ABR2);
	print("afficher apres extrait max");
	afficher(ABR2);
	ABR2 = extrait_min(ABR2);
	print("afficher apres extrait min");
	afficher(ABR2);
	print("balance ABR =", balance(ABR), "equilibrer", est_equilibrer(ABR));
	print("balance ABR2 =", balance(ABR2), "equilibrer", est_equilibrer(ABR2));
	print("ABR to list =", arbre_to_list(ABR));
	print("ABR2 to list =", arbre_to_list(ABR2));
	print("modifie 10 -> 20");
	ABR = modifie(ABR, 10, 20);
	print("recherche(10)", recherche(ABR, 10));
	print("recherche(20)", recherche(ABR, 20));
	print("racine", racine(ABR));
	print("noeuds_internes", noeuds_internes(ABR));
	print("feuilles", feuilles(ABR));
	save_arbre(ABR);
	ABR3 = open_arbre();
	print("afficher ABR3");
	afficher(ABR3);
	ABR4 = copy(ABR);
	nbr_ARB, nbr_ARB2, nbr_ARB3, nbr_ARB4 = nbr_noeuds(ABR), nbr_noeuds(ABR2), nbr_noeuds(ABR3), nbr_noeuds(ABR4);
	print("comparer ABR '%d' et ABR2 '%d'" % (nbr_ARB, nbr_ARB2), est_egaux(ABR, ABR2));
	print("comparer ABR '%d' et ABR3 '%d'" % (nbr_ARB, nbr_ARB3), est_egaux(ABR, ABR3));
	print("comparer ABR '%d' et ABR4 '%d'" % (nbr_ARB, nbr_ARB4), est_egaux(ABR, ABR4));
	ABR4 = insertion_liste(ABR4, [19, 18, 17, 10]);
	vs = list(range(-10, 30));
	random.shuffle(vs);
	for x in arbre_to_list(ABR4):
		vs.remove(x);
	random.shuffle(vs);
	ABR4 = insertion_liste(ABR4, vs);
	print("afficher ABR4");
	afficher(ABR4);
	print("successeur(1)", valeur(successeur(ABR4, 1)), "predecesseur(1)", valeur(predecesseur(ABR4, 1)));
	print("successeur(5)", valeur(successeur(ABR4, 5)), "predecesseur(5)", valeur(predecesseur(ABR4, 5)));
	print("successeur(9)", valeur(successeur(ABR4, 9)), "predecesseur(9)", valeur(predecesseur(ABR4, 9)));
	print("successeur(10)", valeur(successeur(ABR4, 10)), "predecesseur(10)", valeur(predecesseur(ABR4, 10)));
	print("successeur(15)", valeur(successeur(ABR4, 15)), "predecesseur(15)", valeur(predecesseur(ABR4, 15)));
	print("successeur(16)", valeur(successeur(ABR4, 16)), "predecesseur(16)", valeur(predecesseur(ABR4, 16)));
	print("successeur(20)", valeur(successeur(ABR4, 20)), "predecesseur(20)", valeur(predecesseur(ABR4, 20)));
	print("plus_proche(0)", valeur(plus_proche(ABR4, 0)));
	print("plus_proche(5.6)", valeur(plus_proche(ABR4, 5.6)));
	print("plus_proche(12.01)", valeur(plus_proche(ABR4, 12.01)));
	print("plus_proche(21)", valeur(plus_proche(ABR4, 21)));
	print("mirror ABR2");
	ABR5 = mirror(ABR2);
	afficher(ABR2);
	print("-" * 40);
	afficher(ABR5);
	print("-" * 40);
	print("est_abr(ABR) =", est_abr(ABR));
	print_arbre(ABR);
	print("est_abr(ABR2) =", est_abr(ABR2));
	print_arbre(ABR2);
	print("est_abr(ABR3) =", est_abr(ABR3));
	print_arbre(ABR3);
	print("est_abr(ABR4) =", est_abr(ABR4));
	print_arbre(ABR4);
	print("est_abr(ABR5) =", est_abr(ABR5));
	print_arbre(ABR5);
	try:
		draw_arbre(ABR4);
	except Exception as e:
		print("Erreur : %s" % e);
	ABR = vider(ABR);
	ABR2 = vider(ABR2);
	print("afficher apres vider");
	afficher(ABR);
	afficher(ABR2);
	print("%#010x %#010x %#010x %#010x" % (id(ABR), id(ABR2), id(ABR3), id(ABR4)));
	print("%06d %06d %06d %06d" % (sys.getsizeof(ABR), sys.getsizeof(ABR2), sys.getsizeof(ABR3), sys.getsizeof(ABR4)));

if __name__ == "__main__":
	time1, timec1 = datetime.now(), time.clock();
	main();
	time2, timec2 = datetime.now(), time.clock();

print("time1 = %s, timec1 = %0.8f secondes" % (time1, timec1));
print("time2 = %s, timec2 = %0.8f secondes" % (time2, timec2));
print("delay 1-2 = %s, %0.8f secondes" % (time2 - time1, timec2 - timec1));
