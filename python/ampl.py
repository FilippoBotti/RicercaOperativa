from amplpy import AMPL, Environment




class Problem:
    def __init__(self, professori, classi, ore, materie, giorni, giorni_liberi, ore_libere, lezioni, cattedre, ore_per_materie, ampl):
         self.professori = professori
         self.classi = classi
         self.ore = ore
         self.materie = materie
         self.giorni = giorni
         self.giorni_liberi = giorni_liberi
         self.ore_libere = ore_libere
         self.lezioni = lezioni
         self.cattedre = cattedre
         self.ore_per_materia = ore_per_materie
         self.ampl = ampl


    def set_data(self):
        PROFESSORI = self.ampl.get_set('PROFESSORI')
        PROFESSORI.set_values(self.professori)
        CLASSI = self.ampl.get_set('CLASSI')
        
        CLASSI.set_values(self.classi)
        ORE = self.ampl.get_set('ORE')
        
        ORE.set_values(self.ore)
        MATERIE = self.ampl.get_set('MATERIE')
        
        MATERIE.set_values(self.materie)
        GIORNI = self.ampl.get_set('GIORNI')
        
        GIORNI.setValues(self.giorni)
        GIORNI_LIBERI = self.ampl.get_set('GIORNI_LIBERI')
        
        GIORNI_LIBERI.set_values(self.giorni_liberi)
        ORE_LIBERE = self.ampl.get_set('ORE_LIBERE')
        
        ORE_LIBERE.set_values(self.ore_libere)
        LEZIONI = self.ampl.get_set('LEZIONI')
        
        LEZIONI.set_values(self.lezioni)
        CATTEDRE = self.ampl.get_set('CATTEDRE')
        
        CATTEDRE.set_values(self.cattedre)
        ORE_PER_MATERIA = self.ampl.get_parameter('ore_per_materia')
        
            
        ORE_PER_MATERIA.set_values(self.ore_per_materia)
    



    def define_problem(self):
        #INSIEMI
        self.ampl.eval('set PROFESSORI; set CLASSI; set MATERIE; set ORE;\
                set GIORNI; set GIORNI_LIBERI within PROFESSORI cross GIORNI; \
                set LEZIONI within GIORNI cross ORE; set CATTEDRE within MATERIE cross PROFESSORI;\
                set ORE_LIBERE within PROFESSORI cross LEZIONI;')

        #PARAMETRI
        self.ampl.eval('param ore_per_materia{MATERIE} >= 0, integer; param M := 10000; param ore_al_giorno integer, default 5;')

        #VARIABILI
        self.ampl.eval('var x{c in CLASSI, (m,p) in CATTEDRE, (g,h) in LEZIONI} binary; \
                var gl{p in PROFESSORI, g in GIORNI} binary;')

        #GIORNO_LAV
        self.ampl.eval('subject to giorno_lav{(p,g) in PROFESSORI cross GIORNI}:\
        gl[p,g] <= sum{m in MATERIE, h in ORE, c in CLASSI : (m,p) in CATTEDRE} x[c,m,p,g,h];')

        #GIORNO_LAV2
        self.ampl.eval('subject to giorno_lav2{(m,p) in CATTEDRE, (g,h) in LEZIONI, c in CLASSI}:\
        gl[p,g] >= x[c,m,p,g,h];')

        #ORE GIORNALIERE
        self.ampl.eval('subject to ore_giornaliere{c in CLASSI, g in GIORNI} : \
        sum{(m,p) in CATTEDRE, h in ORE: (g,h) in LEZIONI} x[c,m,p,g,h] = ore_al_giorno;')

        #ORE CONTEMPORANEA CLASSI
        self.ampl.eval('subject to ore_in_contemporanea_classe{c in CLASSI, (g,h) in LEZIONI} :\
        sum{(m,p) in CATTEDRE} x[c,m,p,g,h] = 1;')

        #ORE CONTEMPORANEA PROF
        self.ampl.eval('subject to ore_in_contemporanea_prof{p in PROFESSORI, (g,h) in LEZIONI} :\
        sum{c in CLASSI, m in MATERIE : \
        (m,p) in CATTEDRE} x[c,m,p,g,h] <= 1;')

        #ORE MASSIME PROF IN UNA CLASSE
        self.ampl.eval('subject to ore_massime_professori{c in CLASSI, g in GIORNI, p in PROFESSORI} :\
        sum{h in ORE, m in MATERIE : (m,p) in CATTEDRE} x[c,m,p,g,h] <= 3;')

        #ORE MASSIME MATERIA IN UNA CLASSE
        self.ampl.eval('subject to ore_massime_materia{c in CLASSI, g in GIORNI, m in MATERIE} :\
        sum{h in ORE, p in PROFESSORI : (m,p) in CATTEDRE } x[c,m,p,g,h] <= 2;')

        #ORE MATERIA ALLA SETTIMANA
        self.ampl.eval('subject to ore_materia{c in CLASSI, m in MATERIE} :\
        sum{(g,h) in LEZIONI, p in PROFESSORI : (m,p) in CATTEDRE }\
        x[c,m,p,g,h] = ore_per_materia[m];')

        #ORE NON CONSECUTIVE
        self.ampl.eval('subject to ore_non_consecutive{c in CLASSI, g in GIORNI, m in MATERIE, p in PROFESSORI, \
            h in ORE: h+1 in ORE &&  (m,p) in CATTEDRE} :\
            sum{j in h+1..5, mat in MATERIE : (mat,p) in CATTEDRE} x[c,mat,p,g,j] <= (1-x[c,m,p,g,h])*M + x[c,m,p,g,h+1]*M;')

        #SINGOLO PROF PER MATERIA PER CLASSE
        self.ampl.eval('subject to singolo_prof_per_materia{c in CLASSI, g in GIORNI, m in MATERIE, p in PROFESSORI, \
            h in ORE: (m,p) in CATTEDRE}:\
            sum{gi in GIORNI, pr in PROFESSORI, \
            hi in ORE: pr!=p && (m,pr) in CATTEDRE} x[c,m,pr,gi,hi] <= (1-x[c,m,p,g,h])*M;')

        #GIORNI LAVORATIVI VINCOLO
        self.ampl.eval('subject to giorni_lavorativi{p in PROFESSORI}:\
        sum{g in GIORNI} gl[p,g] <=5;')

        # #MINIMIZZO GIORNI LAVORATIVI
        # self.ampl.eval('minimize obj_giorni_lavorativi{p in PROFESSORI}:\
        # sum{g in GIORNI} gl[p,g];')

        # #MINIMIZZO LEZIONI IN GIORNI LAVORATIVI
        # self.ampl.eval('minimize lezioni_in_giorni_liberi{p in PROFESSORI}:\
        # sum{g in GIORNI:\
        #     (p,g) in GIORNI_LIBERI} gl[p,g];')

        # #ORE LIBERE PROFESSORI
        # self.ampl.eval('minimize lezioni_in_ore_libere{p in PROFESSORI} :\
        # sum{(g,h) in LEZIONI,c in CLASSI, m in MATERIE :\
        #     (m,p) in CATTEDRE &&\
        #     (p,g,h) in ORE_LIBERE} x[c,m,p,g,h];')

        # self.ampl.eval('minimize ore_buche{g in GIORNI, p in PROFESSORI,h in ORE:\
        #     (g,h) in LEZIONI && h+1 in ORE}:\
        #     sum{m in MATERIE,c in CLASSI,j in ORE: (g,j) in LEZIONI\
        #     && j>h && (m,p) in CATTEDRE}\
        #     (x[c,m,p,g,j] - x[c,m,p,g,h+1] * M (1-x[c,m,p,g,h]) * M);')


        self.ampl.eval('minimize ore_buche{g in GIORNI, p in PROFESSORI,h in ORE:\
            (g,h) in LEZIONI && h+1 in ORE}:\
            sum{m in MATERIE,c in CLASSI,j in ORE: (g,j) in LEZIONI\
            && j>h && (m,p) in CATTEDRE}\
            (x[c,m,p,g,j] - x[c,m,p,g,h+1] * M - (1-x[c,m,p,g,h]) * M)+\
                sum{(g1,h1) in LEZIONI,c1 in CLASSI, m1 in MATERIE :\
            (m1,p) in CATTEDRE &&\
            (p,g1,h1) in ORE_LIBERE} x[c1,m1,p,g1,h1] +\
                sum{g2 in GIORNI:\
            (p,g2) in GIORNI_LIBERI} gl[p,g2]+\
                 sum{g3 in GIORNI} gl[p,g3] ;')


    def solve_problem(self):
        self.ampl.solve()
   