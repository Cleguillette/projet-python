#import json
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# def charger_taches():
#     with open("taches.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return(data)

# def sauvegarder_taches(taches):
#     with open("taches.json", "w", encoding="utf-8") as f:
#         json.dump(taches, f, ensure_ascii=False, indent=2)

# taches = charger_taches()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taches.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    statut = db.Column(db.String(20), nullable=False, default="todo")

    def __repr__(self):
        return f"<Task {self.nom} ({self.statut})>"
    
@app.route("/", methods=["GET", "POST"])
def index():
    
    message = None
    if request.method == "POST": 

        # L'utilisateur a soumis le formulaire
        nouvelle_tache = request.form["nouvelle_tache"].strip()

        if nouvelle_tache == "":
            message = "A task cannot be empty"
        # elif (
        #     nouvelle_tache in taches["todo"] 
        #     or nouvelle_tache in taches["in_progress"] 
        #     or nouvelle_tache in taches["done"]
        # ):

        elif Task.query.filter_by(nom=nouvelle_tache).first():
            message = "This task already exists"
        else:
            # taches["todo"].append(nouvelle_tache)
            # sauvegarder_taches(taches)
            nouvelle = Task(nom=nouvelle_tache, statut="todo")
            db.session.add(nouvelle)
            db.session.commit()

    todo = Task.query.filter_by(statut="todo").all()
    in_progress = Task.query.filter_by(statut="in_progress").all()
    done = Task.query.filter_by(statut="done").all()

    return render_template("index.html", 
                           #todo=taches["todo"], 
                           todo=todo,
                           #in_progress=taches["in_progress"], 
                           in_progress = in_progress,
                           #done=taches["done"],
                           done = done, 
                           message=message)  # au lieu de renvoyer juste du texte


@app.route("/supprimer", methods=["POST"])
def supprimer():
    tache_supp = request.form["tache"]
    statut_supp = request.form["statut"]
    #if tache_supp in taches[statut_supp]:
    tache = Task.query.filter_by(nom=tache_supp, statut=statut_supp).first()
    if tache:
        #taches[statut_supp].remove(tache_supp)
        db.session.delete(tache)
        db.session.commit()
    #sauvegarder_taches(taches)
    return redirect("/")

@app.route("/deplacer", methods=["POST"])
def deplacer():
    tache_dep = request.form["tache"]
    statut_dep = request.form["statut"]
    statut_dest= request.form["destination"]
    #if tache_dep in taches[statut_dep]:
    tache = Task.query.filter_by(nom=tache_dep, statut=statut_dep).first()
    if tache:
        tache.statut = statut_dest
        db.session.commit()
        #taches[statut_dep].remove(tache_dep)
        #taches[statut_dest].append(tache_dep)
    #sauvegarder_taches(taches)
    return redirect("/")

if __name__ == "__main__": # Ne fait ce qui est dedans que si on exécutepython main.py ce fichier directement
    with app.app_context():
        db.create_all()
    app.run(debug=True)

