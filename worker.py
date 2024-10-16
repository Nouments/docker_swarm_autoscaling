import subprocess
import requests
import time

# Configuration des paramètres
MANAGER_API_URL = 'http://<manager-ip>:<manager-port>/scale'  # URL de l'API du manager
SERVICE_NAME = '<service-cible>'
CPU_THRESHOLD_UP = 80  # Seuil d'incrémentation (plus de 80 % CPU)
CPU_THRESHOLD_DOWN = 20  # Seuil de décrémentation (moins de 20 % CPU)
CHECK_INTERVAL = 10  # Intervalle entre chaque vérification (en secondes)

def get_running_containers(service_name):
    """Récupère les conteneurs en cours d'exécution pour un service."""
    result = subprocess.run(
        ['docker', 'ps', '--filter', f'name={service_name}', '--format', '{{.ID}}'],
        stdout=subprocess.PIPE
    )
    container_ids = result.stdout.decode('utf-8').splitlines()
    return container_ids

def get_cpu_usage(container_id):
    """Récupère l'utilisation CPU d'un conteneur spécifique avec docker stats."""
    result = subprocess.run(
        ['docker', 'stats', '--no-stream', '--format', '{{.CPUPerc}}', container_id],
        stdout=subprocess.PIPE
    )
    cpu_usage = result.stdout.decode('utf-8').strip().rstrip('%')
    return float(cpu_usage)

def notify_manager(action):
    """Envoie un signal d'incrémentation ou décrémentation au manager."""
    payload = {'action': action}
    response = requests.post(MANAGER_API_URL, json=payload)
    if response.status_code == 200:
        print(f"Notification envoyée au manager : {response.text}")
    else:
        print(f"Erreur lors de la notification : {response.status_code}, {response.text}")

def main():
    while True:
        containers = get_running_containers(SERVICE_NAME)
        cpu_usages = [get_cpu_usage(container_id) for container_id in containers]
        avg_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
        print(f"Utilisation CPU moyenne : {avg_cpu_usage}%")

        if avg_cpu_usage > CPU_THRESHOLD_UP:
            print("Utilisation CPU au-dessus du seuil. Incrémentation des réplicas.")
            notify_manager('increment')
        elif avg_cpu_usage < CPU_THRESHOLD_DOWN:
            print("Utilisation CPU en-dessous du seuil. Décrémentation des réplicas.")
            notify_manager('decrement')
        else:
            print("Utilisation CPU dans les limites acceptables. Aucun changement.")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
