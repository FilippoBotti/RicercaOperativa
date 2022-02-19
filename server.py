from flask import Flask, request, render_template
import ampl as probl
from amplpy import AMPL, Environment

app = Flask(__name__)





@app.route('/sign-up',methods=('GET', 'POST'))
def solve():
    if request.method == 'POST':
        professori = ['FAROLINI', 'COPELLI', 'RAVANETTI', 'PEDRETTI', 
                     'BALL', 'QUARTAROLI']
        classi = ['A','B']

        ore = [1,2,3,4,5]

        materie = ['ITA', 'MATE', 'TECNICA', 'GINNASTICA', 'SCIENZE', 'INGLESE', 
                        'STORIAGEO', 'MUSICA']


        giorni = ['LUN', 'MAR', 'MER', 'GIO']

        giorni_liberi = [('FAROLINI', 'MAR'),
                        ('PEDRETTI', 'MER'),
                        ('QUARTAROLI', 'LUN'),
                        ('BALL', 'GIO'),
                        ('COPELLI', 'MAR'),
                        ('RAVANETTI','MER')
                        ]

        ore_libere = [('FAROLINI', 'GIO', 1),
                        # ('PEDRETTI', 'LUN',2),
                        # ('QUARTAROLI','LUN',2),
                        # ('BALL','LUN',2),
                        # ('COPELLI','MER',1),
                        # ('RAVANETTI','GIO',5)
        ]



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
    ]

        cattedre = [('ITA', 'FAROLINI'),
            ('MATE', 'COPELLI'),
            ('TECNICA', 'RAVANETTI'),
            ('GINNASTICA', 'PEDRETTI'),
            ('SCIENZE', 'COPELLI'),
            ('INGLESE', 'BALL'),
            ('STORIAGEO', 'FAROLINI'),
            ('MUSICA', 'QUARTAROLI'),]


        ore_per_materia = {
                'ITA':4,
                'MATE':3,
                'INGLESE':3,
                'MUSICA':2,
                'GINNASTICA':2,
                'TECNICA':2,
                'STORIAGEO':2,
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
                    
        lezioni.sort(key=lambda tup: tup[4]) 
        
        if request.form['title'] not in problem.professori:
            return render_template('base.html', giorni=problem.giorni, lezioni=lezioni,  classi = problem.classi)
        return render_template('professore.html', giorni=problem.giorni, lezioni=lezioni, professore = request.form['title'])

    
@app.route('/')
def ret():
    return render_template('index.html')
                        
        