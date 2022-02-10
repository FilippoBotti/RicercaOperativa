set PROFESSORI;
set CLASSI;
set MATERIE;
set ORE;
set GIORNI;
set GIORNI_LIBERI within PROFESSORI cross GIORNI;
set LEZIONI within GIORNI cross ORE;
set CATTEDRE within MATERIE cross PROFESSORI;
set ORE_LIBERE within PROFESSORI cross LEZIONI;

param ore_per_materia{MATERIE} >= 0, integer;
param M := 100;


var x{c in CLASSI, (m,p) in CATTEDRE, (g,h) in LEZIONI} binary;
var gl{p in PROFESSORI, g in GIORNI} binary;

###VINCOLI###
subject to giorno_lav{(p,g) in PROFESSORI cross GIORNI}:
	gl[p,g] <= sum{m in MATERIE, h in ORE, c in CLASSI : (m,p) in CATTEDRE} x[c,m,p,g,h];

subject to giorno_lav2{(m,p) in CATTEDRE, (g,h) in LEZIONI, c in CLASSI}:
	gl[p,g] >= x[c,m,p,g,h];
	
#5 ORE AL GIORNO	
subject to ore_giornaliere{c in CLASSI, g in GIORNI} : 
	sum{(m,p) in CATTEDRE, h in ORE: (g,h) in LEZIONI} x[c,m,p,g,h] =5;

#1 ORA IN CONTEMPORANEA PER CLASSE
subject to ore_in_contemporanea_classe{c in CLASSI, (g,h) in LEZIONI} :
	sum{(m,p) in CATTEDRE} x[c,m,p,g,h] = 1;
	
#1 ORA IN CONTEMPORANEA PER PROF
subject to ore_in_contemporanea_prof{p in PROFESSORI, (g,h) in LEZIONI} :
	sum{c in CLASSI, m in MATERIE : 
	 (m,p) in CATTEDRE} x[c,m,p,g,h] <= 1;

#3 ORE (DI FILA) MASSIME PER I PROF IN UNA CLASSE	
subject to ore_massime_professori{c in CLASSI, g in GIORNI, p in PROFESSORI} :
	sum{h in ORE, m in MATERIE : (m,p) in CATTEDRE} x[c,m,p,g,h] <= 3;
	
#2 ORE MASSIME (DI FILA) DELLA STESSA MATERIA
subject to ore_massime_materia{c in CLASSI, g in GIORNI, m in MATERIE} :
	sum{h in ORE, p in PROFESSORI : (m,p) in CATTEDRE } x[c,m,p,g,h] <= 2;

#ORE PER MATERIA A SETTIMANA	
subject to ore_materia{c in CLASSI, m in MATERIE} :
	sum{(g,h) in LEZIONI, p in PROFESSORI : (m,p) in CATTEDRE }
	 x[c,m,p,g,h] = ore_per_materia[m];
	
#GIORNI LIBERI DEI PROF
#eliminare insieme giorni_liberi e fare sommatoria <=5
#aggiungere obiettivo giorno libero = richiesta
#idem per ore
#subject to giorni_liberi{p in PROFESSORI} :
#	sum{c in CLASSI, (g,h) in LEZIONI, m in MATERIE :
#		(m,p) in CATTEDRE &&
#		(p,g) in GIORNI_LIBERI} x[c,m,p,g,h] = 0;
	
#ORE LIBERE DEI PROF	
subject to ore_libere{p in PROFESSORI} :
	sum{(g,h) in LEZIONI,c in CLASSI, m in MATERIE :
		(m,p) in CATTEDRE &&
		(p,g,h) in ORE_LIBERE} x[c,m,p,g,h] = 0;	
	
maximize ore_buche{p in PROFESSORI, g in GIORNI, h in ORE: (g,h+2) in LEZIONI}:
	sum{c in CLASSI, m in MATERIE: (m,p) in CATTEDRE } 
	(x[c,m,p,g,h]+x[c,m,p,g,h+1] - x[c,m,p,g,h+2]);
	
	
#PROFESSORE NON AVRA LEZIONI NON CONSECUTIVE IN OGNI CLASSE
subject to or_massime_professori{c in CLASSI, g in GIORNI, m in MATERIE, p in PROFESSORI, 
		h in ORE: h+1 in ORE &&  (m,p) in CATTEDRE} :
		sum{j in h+1..5, mat in MATERIE : (mat,p) in CATTEDRE} x[c,mat,p,g,j] <= (1-x[c,m,p,g,h])*M + x[c,m,p,g,h+1]*M;
	
subject to singolo_prof_per_materia{c in CLASSI, g in GIORNI, m in MATERIE, p in PROFESSORI, 
		h in ORE: (m,p) in CATTEDRE}:
		sum{gi in GIORNI, pr in PROFESSORI, 
		hi in ORE: pr!=p && (m,pr) in CATTEDRE} x[c,m,pr,gi,hi] <= (1-x[c,m,p,g,h])*M;

subject to giorni_lavorativi{p in PROFESSORI}:
	sum{g in GIORNI} gl[p,g] <=5;
	
minimize obj_giorni_lavorativi{p in PROFESSORI}:
	sum{g in GIORNI} gl[p,g];
	
minimize lezioni_in_giorni_liberi{p in PROFESSORI}:
	sum{g in GIORNI:
		(p,g) in GIORNI_LIBERI} gl[p,g];
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	
	
	
