def test_ajouter_tache(client):
    # Envoi d'un POST sur la route "/" pour ajouter une tâche
    response = client.post("/", data={"nouvelle_tache": "Tester pytest"})
    
    # Vérifie que le serveur a répondu avec un code 200 (OK)
    assert response.status_code == 200
    
    # Vérifie que la tâche ajoutée existe bien en base
    from main import Task, db, app
    with app.app_context():
        tache = Task.query.filter_by(nom="Tester pytest").first()
        assert tache is not None
        assert tache.statut == "todo"


def test_supprimer_tache(client):
    from main import Task, db, app

    # Crée la tâche directement en base
    with app.app_context():
        tache = Task(nom="Tester pytest", statut="todo")
        db.session.add(tache)
        db.session.commit()

    # Envoie du POST pour supprimer la tâche
    response = client.post("/supprimer", data={"tache": "Tester pytest", "statut": "todo"})
    assert response.status_code == 302  # redirect

    # Vérifie que la tâche a été supprimée
    with app.app_context():
        tache = Task.query.filter_by(nom="Tester pytest").first()
        assert tache is None

def test_deplacer_tache(client):
    from main import Task, db, app
       
    # Crée la tâche directement en base
    with app.app_context():
        tache = Task(nom="Tester pytest", statut="todo")
        db.session.add(tache)
        db.session.commit()
    
    response = client.post("/deplacer", data={"tache": "Tester pytest", 
                                              "statut": "todo", 
                                              "destination" : "in_progress"})
    
    # Vérifie que la tâche a été déplacée
    with app.app_context():
        tache = Task.query.filter_by(nom="Tester pytest", ).first()
        assert tache is not None
        assert tache.statut == "in_progress"