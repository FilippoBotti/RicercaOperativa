from flask import Flask, request, render_template
import ampl as probl
from amplpy import AMPL, Environment

app = Flask(__name__)





@app.route('/sign-up',methods=('GET', 'POST'))
def solve():
    if request.method == 'POST':
        professori = ['FAROLINI', 'COPELLI', 'RAVANETTI', 'PEDRETTI', 'PISTORIO', 'GERARDI', 
                    'MALANDRI', 'BALL', 'QUARTAROLI', 'BOTTI', 'NERI', 'VERDI' ,'GIALLI']
        classi = ['A','B']

        ore = [1,2,3,4,5]

        materie = ['ITA', 'MATE', 'TECNICA', 'GINNASTICA', 'ARTE', 'FRANCESE', 'SCIENZE', 'INGLESE', 
                        'STORIAGEO', 'RELIGIONE', 'MUSICA']


        giorni = ['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB']

        giorni_liberi = [('FAROLINI', 'LUN'), ('BOTTI', 'LUN'), ('BOTTI', 'MAR'), ('BOTTI', 'SAB'),
                    ('FAROLINI', 'MAR'), ('BALL', 'LUN'), ('BALL', 'MAR'), ('BALL', 'SAB')]

        ore_libere = [('FAROLINI', 'GIO', 1), ('BOTTI', 'SAB',2)]
        lezioni = [('LUN', 1),
            ('LUN', 2),
            ('LUN', 3),
            ('LUN', 4),
            ('LUN', 5),
            ('MAR', 1),
            ('MAR', 2),
            ('MAR', 3),
            ('MAR', 4),
            ('MAR', 5),
            ('MER', 1),
            ('MER', 2),
            ('MER', 3),
            ('MER', 4),
            ('MER', 5),
            ('GIO', 1),
            ('GIO', 2),
            ('GIO', 3),
            ('GIO', 4),
            ('GIO', 5),
            ('VEN', 1),
            ('VEN', 2),
            ('VEN', 3),
            ('VEN', 4),
            ('VEN', 5),
            ('SAB', 1),
            ('SAB', 2),
            ('SAB', 3),
            ('SAB', 4),
            ('SAB', 5),]

        cattedre = [('ITA', 'FAROLINI'),
            ('SCIENZE', 'NERI'),
            ('ARTE', 'VERDI'),
            ('MUSICA', 'GIALLI'),
            ('ITA', 'BOTTI'),
            ('MATE', 'COPELLI'),
            ('TECNICA', 'RAVANETTI'),
            ('GINNASTICA', 'PEDRETTI'),
            ('SCIENZE', 'COPELLI'),
            ('INGLESE', 'BALL'),
            ('FRANCESE', 'GERARDI'),
            ('ARTE', 'PISTORIO'),
            ('RELIGIONE', 'MALANDRI'),
            ('STORIAGEO', 'FAROLINI'),
            ('MUSICA', 'QUARTAROLI'),]


        ore_per_materia = {
                'ITA':6,
                'MATE':4,
                'INGLESE':3,
                'ARTE':2,
                'MUSICA':2,
                'GINNASTICA':2,
                'TECNICA':2,
                'STORIAGEO': 4,
                'FRANCESE':2,
                'RELIGIONE':1,
                'SCIENZE':2
            }

        ampl = AMPL()
        ampl.setOption('solver','gurobi')

        problem = probl.Problem(professori,classi,ore,materie,giorni,giorni_liberi,ore_libere,lezioni,cattedre,ore_per_materia,ampl)
        problem.define_problem()
        problem.set_data()
        problem.solve_problem()
        
        lezioni = []
        for key,value in problem.ampl.getVariable("x").get_values().to_dict().items():
                if value >0:
                    lezioni.append((key[0],key[1],key[2],key[3],key[4]))
                    
        for key,val in problem.ampl.get_objective("lezioni_in_giorni_liberi"):
            print(key,val)
        lezioni.sort(key=lambda tup: tup[4]) 
        # for lezione in lezioni:
        #     if lezione[2] =="BOTTI":
        #         print(lezione)
        if request.form['title'] not in problem.professori:
            return render_template('base.html', giorni=problem.giorni, lezioni=lezioni,  classi = problem.classi)
        return render_template('professore.html', giorni=problem.giorni, lezioni=lezioni, professore = request.form['title'])

    
@app.route('/')
def ret():
    return render_template('index.html')
                        
        