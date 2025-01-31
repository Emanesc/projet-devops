from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Mlb'

db = SQLAlchemy(app)

# Modèle Intervenant
class Intervenant(db.Model):
    __tablename__ = 'intervenant'
    IdIntervenant = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom = db.Column(db.String(50), nullable=False)
    Prenom = db.Column(db.String(50), nullable=False)
    Poste = db.Column(db.String(50), nullable=False)
    interventions = db.relationship('Intervention', backref='intervenant', lazy=True, cascade='all, delete-orphan')

# Modèle Client
class Client(db.Model):
    __tablename__ = 'client'
    IdClient = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom = db.Column(db.String(50), nullable=False)
    Prenom = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    interventions = db.relationship('Intervention', backref='client', lazy=True, cascade='all, delete-orphan')

# Modèle Intervention
class Intervention(db.Model):
    __tablename__ = 'intervention'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    Motive = db.Column(db.String(255), nullable=False)
    etat = db.Column(db.String(20), nullable=False)
    IdIntervenant = db.Column(db.Integer, db.ForeignKey('intervenant.IdIntervenant'), nullable=False)
    IdClient = db.Column(db.Integer, db.ForeignKey('client.IdClient'), nullable=False)

# Création des tables
with app.app_context():
    db.create_all()



@app.route('/')
def homelogin():
    return render_template("loginSession.html")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '1234':
            session['username'] = username
            return redirect(url_for('homepage'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')
            return redirect(url_for('homelogin'))


# Routes CRUD pour Intervenant

@app.route('/intervenant/add', methods=['GET', 'POST'])
def add_intervenant():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        poste = request.form['poste']
        new_intervenant = Intervenant(Nom=nom, Prenom=prenom, Poste=poste)
        db.session.add(new_intervenant)
        db.session.commit()
        return redirect(url_for('homepage'))

    return render_template('add_intervenant.html')

@app.route('/list')
def homepage():
    intervenants = Intervenant.query.all()
    clients = Client.query.all()
    interventions = Intervention.query.all()
    return render_template('home.html', intervenants=intervenants,clients=clients,interventions=interventions )

@app.route('/intervenantform/<int:id>/edit')
def edit_intervenantform(id):
    intervenant = Intervenant.query.get(id)
    return render_template('edit_intervenant.html', intervenant=intervenant)

@app.route('/intervenant/<int:id>/edit', methods=['GET', 'POST'])
def edit_intervenant(id):
    intervenant = Intervenant.query.get(id)
    if request.method == 'POST':
        intervenant.Nom = request.form['nom']
        intervenant.Prenom = request.form['prenom']
        intervenant.Poste = request.form['poste']
        db.session.commit()
        return redirect(url_for('homepage'))  # Redirige vers 'homepage' (liste des intervenants)

    return render_template('edit_intervenant.html', intervenant=intervenant)


@app.route('/intervenant/<int:id>/delete')
def delete_intervenant(id):
    intervenant = Intervenant.query.get(id)
    db.session.delete(intervenant)
    db.session.commit()
    return redirect(url_for('homepage'))  # Redirige vers 'homepage' (liste des intervenants)


# Routes CRUD pour Client
@app.route('/client/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        direction = request.form['direction']
        new_client = Client(Nom=nom, Prenom=prenom, direction=direction)
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('homepage'))

    return render_template('add_client.html')

@app.route('/clientform/<int:id>/edit')
def edit_clientform(id):
    client = Client.query.get(id)
    return render_template('edit_client.html', client=client)

@app.route('/client/<int:id>/edit', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get(id)
    if request.method == 'POST':
        client.Nom = request.form['nom']
        client.Prenom = request.form['prenom']
        client.direction = request.form['direction']
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('edit_client.html', client=client)

@app.route('/client/<int:id>/delete')
def delete_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/intervention/add', methods=['GET', 'POST'])
def add_intervention():
    if request.method == 'POST':
        # Récupérez les données du formulaire
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convertir la chaîne de date en objet de date Python

        type_intervention = request.form['type']
        motive = request.form['motive']
        etat = request.form['etat']
        id_intervenant = request.form['id_intervenant']
        id_client = request.form['id_client']

        # Créez une nouvelle intervention
        new_intervention = Intervention(date=date_obj, type=type_intervention, Motive=motive, etat=etat,IdIntervenant=id_intervenant, IdClient=id_client)
        db.session.add(new_intervention)
        db.session.commit()
        return redirect(url_for('homepage'))

    intervenants = Intervenant.query.all()
    clients = Client.query.all()
    return render_template('add_intervention.html', intervenants=intervenants, clients=clients)

@app.route('/interventionform/<int:id>/edit')
def edit_interventionform(id):
    intervention = Intervention.query.get(id)
    return render_template('edit_intervention.html', intervention=intervention)

@app.route('/intervention/<int:id>/edit', methods=['GET', 'POST'])
def edit_intervention(id):
    intervention = Intervention.query.get(id)
    if request.method == 'POST':
        # Mettez à jour les données de l'intervention à partir du formulaire
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        intervention.date = date_obj
        intervention.type = request.form['type']
        intervention.Motive = request.form['motive']
        intervention.etat = request.form['etat']
        intervention.IdIntervenant = request.form['id_intervenant']
        intervention.IdClient = request.form['id_client']

        db.session.commit()
        return redirect(url_for('homepage'))

    intervenants = Intervenant.query.all()
    clients = Client.query.all()
    return render_template('edit_intervention.html', intervention=intervention, intervenants=intervenants, clients=clients)

@app.route('/intervention/<int:id>/delete')
def delete_intervention(id):
    intervention = Intervention.query.get(id)
    db.session.delete(intervention)
    db.session.commit()
    return redirect(url_for('homepage'))

# Exemple de code pour récupérer les pourcentages des tâches
def get_percentage_tasks():
    total_tasks = Intervention.query.count()

    # Pourcentage des tâches réalisées par chaque intervenant
    intervenant_percentages = []
    intervenants = Intervenant.query.all()
    for intervenant in intervenants:
        tasks_by_intervenant = Intervention.query.filter_by(IdIntervenant=intervenant.IdIntervenant).count()
        percentage = (tasks_by_intervenant / total_tasks) * 100
        intervenant_percentages.append({
            'intervenant': f"{intervenant.Nom} {intervenant.Prenom}",
            'percentage': round(percentage, 2)
        })

    # Pourcentage des tâches réalisées ou en attente globalement
    tasks_done = Intervention.query.filter_by(etat='réalisée').count()
    tasks_waiting = Intervention.query.filter_by(etat='en attente').count()
    percentage_done = (tasks_done / total_tasks) * 100
    percentage_waiting = (tasks_waiting / total_tasks) * 100

    return {
        'intervenant_percentages': intervenant_percentages,
        'percentage_done': round(percentage_done, 2),
        'percentage_waiting': round(percentage_waiting, 2)
    }

@app.route('/dashboard')
def dashboard():
    data = get_percentage_tasks()
    return render_template('dashboard.html', data=data)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('homelogin'))

if __name__ == '__main__':
   with app.app_context():
        db.create_all()
        app.run(debug=True)