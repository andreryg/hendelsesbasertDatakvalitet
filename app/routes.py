from flask import current_app as app
from flask import render_template, request
from .add_base_data import add_base_data
from .models import user
from app import db
from app.models import (
    vegkategori,
    vegsystem,
    område,
    hovedelement,
    kvalitetskomponent,
    kvalitetsparameter,
    vegobjekttype,
    egenskapstype,
    skala
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ny_skala', methods=['GET', 'POST'])
def ny_skala():
    """
    Route to create a new scale.
    """
    if request.method == 'GET':
        områder = db.session.query(
            område
        ).all()
        kvalitetsparametere = db.session.query(
            hovedelement, kvalitetskomponent, kvalitetsparameter
        ).join(
            hovedelement, kvalitetsparameter.hovedelement_id == hovedelement.id
        ).join(
            kvalitetskomponent, kvalitetsparameter.kvalitetskomponent_id == kvalitetskomponent.id
        ).all()
        vegobjekttyper = db.session.query(
            vegobjekttype
        ).all()
        egenskapstyper = db.session.query(
            egenskapstype
        ).all()
        return render_template('add_skala.html', områder=områder, kvalitetsparametere=kvalitetsparametere, vegobjekttyper=vegobjekttyper, egenskapstyper=egenskapstyper)
    
    elif request.method == 'POST':
        område_id = int(request.form.get('område'))
        vegobjekttype_id = int(request.form.get('vegobjekttype'))
        egenskapstype_id = int(request.form.get('egenskapstype'))
        kvalitetsparameter_id = int(request.form.get('kvalitetsparameter'))
        skala_navn = request.form.get('skala_navn')
        sep_1 = float(request.form.get('sep_1'))
        sep_2 = float(request.form.get('sep_2'))
        sep_3 = float(request.form.get('sep_3'))
        sep_4 = float(request.form.get('sep_4'))

        ny_skala = skala(
            område_id=område_id if område_id > 0 else None,
            vegobjekttype_id=vegobjekttype_id if vegobjekttype_id > 0 else None,
            egenskapstype_id=egenskapstype_id if egenskapstype_id > 0 else None,
            kvalitetsparameter_id=kvalitetsparameter_id if kvalitetsparameter_id > 0 else None,
            navn=skala_navn,
            sep_1=sep_1,
            sep_2=sep_2,
            sep_3=sep_3,
            sep_4=sep_4
        )

        # Add the new user to the database
        print(ny_skala)
        db.session.add(ny_skala)
        db.session.commit()

        return render_template('index.html', message="Skala opprettet!")

@app.route('/add_base_data')
def add_base_data_route():
    """
    Route to add base data to the database.
    """
    add_base_data()
    return render_template('index.html')