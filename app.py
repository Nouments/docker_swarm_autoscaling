from flask import Flask, request
import subprocess

app = Flask(__name__)

SERVICE_NAME = '<service-cible>'
INITIAL_REPLICAS = 4  # Nombre de réplicas initiaux  minimal dnas votre service
MAX_SURPLUS_REPLICAS = 6  #Nombre maximal de reolicas que l'autoscaling peut  ajouter
surplus_replicas = 0  # Surplus de réplicas actuels (initialisé à 0)

def scale_service(new_replicas):
    """Exécute la commande pour mettre à jour le nombre de réplicas."""
    command = ['docker', 'service', 'scale', f'{SERVICE_NAME}={new_replicas}']
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return f'Scaled {SERVICE_NAME} to {new_replicas} replicas.', 200
    else:
        return f'Error scaling service: {result.stderr}', 500

@app.route('/scale', methods=['POST'])
def handle_scaling():
    global surplus_replicas
    data = request.json
    action = data.get('action')

    current_replicas = INITIAL_REPLICAS + surplus_replicas

    if action == 'increment':
        if surplus_replicas < MAX_SURPLUS_REPLICAS:
            surplus_replicas += 1 # vous pouvez regler ce dernier pour  l'incrémentation de vos replicas en cas e monté en charge
            new_replicas = INITIAL_REPLICAS + surplus_replicas
            return scale_service(new_replicas)
        else:
            return f"Maximum de {MAX_SURPLUS_REPLICAS} réplicas supplémentaires atteint. Aucun changement.", 200

    elif action == 'decrement':
        if surplus_replicas > 0:
            surplus_replicas -= 1  # vous pouvez regler ce dernier pour  la décrémentation  de vos replicas
            new_replicas = INITIAL_REPLICAS + surplus_replicas
            return scale_service(new_replicas)
        else:
            return f"Déjà au nombre minimum de réplicas ({INITIAL_REPLICAS}). Aucun changement.", 200

    return f"Aucune action nécessaire. Nombre actuel de réplicas : {current_replicas}.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='<manager-port>')
