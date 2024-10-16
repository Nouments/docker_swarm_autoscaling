
# Docker Swarm Autoscaling

Bien que Docker Swarm soit un outil d'orchestration de conteneurs permettant de gérer un cluster de Docker, il ne fournit pas nativement la fonctionnalité d'autoscaling. Cela permettrait au cluster de supporter une montée en charge automatiquement. C'est pourquoi le script suivant a été créé afin d'ajouter cette fonctionnalité  sur votre serveur ou cluster Swarm.

Dans notre exemple, nous avons décidé de déployé un service sur chaque worker afin de répartir la charge sur les différents workers. Cependant, si vous utilisez un seul service sur les managers et les workers, ou que vous n'avez qu'un seul hôte, ne vous inquiétez pas, cela fonctionnera toujours.

## Installation

Clonez le projet sur le manager :

```bash
git clone https://github.com/Nouments/docker_swarm_autoscaling.git
```

Installez les dépendances (sur le manager du cluster Swarm) :

```bash
pip install -r requirements.txt
```

## Configuration

Si vous ne disposez que d'un seul hôte Swarm (directement sur le manager), vous pouvez mettre les deux scripts sur la même machine. Assurez-vous de bien configurer les IPs et les ports ainsi que le service cible. Si vous avez des workers et que vous avez déployer un service unique sur un nœud ou un hôte spécifique, il est préférable de mettre `worker.py` sur les workers et de configurer les IPs, les ports et le service cible.

## Création des services `systemctl` pour les deux scripts

Pour automatiser l'exécution de vos scripts Python `manager.py` et `worker.py`, nous allons créer des services `systemd`. Ces services seront gérés par `systemctl`, ce qui vous permettra de les démarrer, les arrêter et les surveiller facilement.

### 1. Créer le service pour `manager.py`

Le service `manager.py` surveille la charge du cluster et déclenche l'autoscaling en conséquence.

#### Etapes :

1. Créez un fichier de service pour le manager :

```bash
sudo nano /etc/systemd/system/autoscaler-manager.service
```

2. Ajoutez le contenu suivant :

```ini
[Unit]
Description=Autoscaler Manager Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/manager.py
WorkingDirectory=/path/to/
Restart=always
User=root
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Remplacez `/path/to/` par le chemin réel de votre script `manager.py`.

3. Rechargez `systemd` pour prendre en compte le nouveau service :

```bash
sudo systemctl daemon-reload
```

4. DÃ©marrez le service :

```bash
sudo systemctl start autoscaler-manager
```

5. Activez le service pour qu'il démarre automatiquement au démarrage du système :

```bash
sudo systemctl enable autoscaler-manager
```

### 2. Créer le service pour `worker.py`

Le service `worker.py` applique les commandes d'autoscaling envoyées par le manager et ajuste les réplicas en conséquence.

#### Etapes :

1. Créez un fichier de service pour le worker :

```bash
sudo nano /etc/systemd/system/autoscaler-worker.service
```

2. Ajoutez le contenu suivant :

```ini
[Unit]
Description=Autoscaler Worker Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/worker.py
WorkingDirectory=/path/to/
Restart=always
User=root
Environment="MANAGER_IP=<IP_MANAGER>"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Remplacez `/path/to/` par le chemin réel de votre script `worker.py` et `<IP_MANAGER>` par l'adresse IP du manager.

3. Rechargez `systemd` pour prendre en compte le nouveau service :

```bash
sudo systemctl daemon-reload
```

4. Démarrez le service :

```bash
sudo systemctl start autoscaler-worker
```

5. Activez le service pour qu'il dÃ©marre automatiquement au démarrage du système :

```bash
sudo systemctl enable autoscaler-worker
```

### 3. Vérification des services

Pour vérifier si les services fonctionnent correctement, utilisez les commandes suivantes :

- Vérifiez l'état du service `manager` :

```bash
sudo systemctl status autoscaler-manager
```

- Vérifiez l'état du service `worker` :

```bash
sudo systemctl status autoscaler-worker
```

- Redémarrez un service si nécessaire :

```bash
sudo systemctl restart autoscaler-manager
sudo systemctl restart autoscaler-worker
```

- Voir les logs des services en temps réel :

```bash
journalctl -u autoscaler-manager -f
journalctl -u autoscaler-worker -f
```

---

Avec ces instructions, vos deux scripts Python seront automatiquement géré par `systemd`, et vous pourrez les contrôler via `systemctl` sur votre serveur ou cluster Swarm.