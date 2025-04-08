**** Structure du dépôt GitHub ***

Les scripts sont organisés en fonction du nom des cas de test, et chaque cas de test contient des sous-cas de test ,ainsi que Sous-sous-cas de test .

L'arborescence ci-dessous explique brièvement la structure globale.

QA_MONIT_1.0.0/

├── Analyse_des_données

            ├── extract_données.py
            ├──  test_performence.py
            ├── test_visualisation.py
            ├── verif_connectivite_user.py
            ├──verif_documentation.py
            ├──verif_gestion_user.py
           
├── Installation des tools DevOps

         ├── verif_config.py
        ├── verif_install.py
        
├── Intégration_DEV

         ├── Intégration proxmox.py
        ├── integre_VMs.py
        
├── Réponse_aux_Anomalies

         ├── verif_jira_part1.py
        ├── verif_jira_part2.py
        
**** Explication de chaque cas de test & sous cas de test ***

       "Installation_Zabbix": "Vérifie l'installation et le fonctionnement de Zabbix."
        "Intégration_DEV": "Teste l'intégration des nouvelles fonctionnalités."
        "Réponse_aux_Anomalies": "Valide la gestion et notification des anomalies."
        "Analyse_des_données": "S'assure de la précision et l'affichage des données"

**** Explication de principe de fonctionnement de scripts ***

Le principe des tests automatisés se déroule en plusieurs étapes :

Préparer un script YML ou Python pour chaque sous-cas de test, selon la tâche à accomplir. Tester chaque script individuellement. Cela constitue la première phase des tests automatisés. Commandes pour exécuter les scripts Python et YML : Exécution d'un script Python : python Intégration LDAP avec Sophos.py

Exécution d'un script python avec Ansible :
 python verif_install.py

**** Script global pour exécuter tous les tests ****

├──Integration_CICD  │ └── rapport_de_test.py La deuxième phase des tests automatisés consiste à préparer un script python global qui prend en compte tous les sous-scripts de chaque sous-cas de test, les exécute ensemble, et génère un rapport de test complet.
