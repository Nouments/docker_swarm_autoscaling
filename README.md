
# Docker Swarm autoscaling

Bien que swarm soit un outil d'orchéstration de conteneur permettant de gérer un cluster de docker, elle ne fournit pas nativement la fonctionalité d'autoscaling permettant au cluster de supporter une montée en charge , c'est pourquoi le script suivant a été créer afin de  le faire  automatiquement dans votre serveur ou cluster warm . 

Dans le contexte de notre exemple on a  decider de deployer un service  sur chaque worker  afin de repartir les charges au niveaux des worker mais si vous utiliser un seul service au niveau des managers et worker ou que vous avez un seul host , ne ous inqquietez pas  cela marchera toujours


## Installation

Clonez le projet  sur le manager :

```bash
  git clone https://github.com/Nouments/docker_swarm_autoscaling.git
```
    
Installation des dépendances (sur le manager su swarm)

```bash
  pip install -r requirements.txt
```
## Configuration 


Si vous  ne disposez que  d'un seule host de swarm directement le manager vous pouvez mettre les 2 script sur la même machine  

