import subprocess
import time
import os
from datetime import datetime
from tabulate import tabulate
from git import Repo  # Utilisation de la bibliothèque GitPython pour cloner le dépôt

def collect_test_results(test_case_id, test_description, test_result, execution_time, error_message=None, test_case_global=None, sub_test_case=None):
    """
    Collecte les résultats du test dans une liste pour un affichage sous forme de tableau.
    """
    test_execution_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tester_name = "Walid Toumi"

    # Collecter les données du test dans une liste
    result = [
        test_case_id,
        test_case_global,
        sub_test_case,
        test_description,
        test_result,
        execution_time,
        test_execution_date,
        tester_name,
        error_message if error_message else "None"
    ]
    return result

def get_test_description(test_case_global):
    """
    Fournit la description du test en fonction du nom du répertoire (Cas de Test Global).
    """
    descriptions = {
        "Installation_Zabbix": "Vérifie l'installation et le fonctionnement de Zabbix.",
        "Intégration_DEV": "Teste l'intégration des nouvelles fonctionnalités.",
        "Réponse_aux_Anomalies": "Valide la gestion et notification des anomalies.",
        "Analyse_des_données": "S'assure de la précision et l'affichage des données."
        
    }
    return descriptions.get(test_case_global, "Description non définie pour ce cas de test.")

def clone_repo(github_url, clone_path):
    """
    Clone le dépôt GitHub si ce n'est pas déjà fait.
    """
    if not os.path.exists(clone_path):
        print(f"Clonage du dépôt depuis {github_url} vers {clone_path}...")
        Repo.clone_from(github_url, clone_path)
        print("Dépôt cloné avec succès.")
    else:
        print(f"Le dépôt existe déjà à {clone_path}.")

def list_and_execute_files(repo_path):
    """
    Affiche l'arborescence des fichiers dans le dépôt et exécute les fichiers Python,
    puis génère un rapport de test sous forme de tableau.
    """
    print(f"Accès au dépôt existant : {repo_path}\n")

    # Vérifier si le répertoire existe
    if not os.path.exists(repo_path):
        print(f"Le répertoire '{repo_path}' n'existe pas.")
        return

    # Initialiser la liste pour stocker les résultats des tests
    test_results = []
    test_case_id_counter = 1  # Compteur pour les ID des tests

    # Afficher l'arborescence des fichiers
    print("\nArborescence du dépôt :")
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

    # Exécuter le fichier Python dans le répertoire 'Integration_CI-CD'
    print("\nExécution des fichiers Python dans 'Integration_CI-CD' :")
    integration_cicd_path = os.path.join(repo_path, 'Integration_CI-CD')

    # Vérifier si le répertoire existe et exécuter les fichiers Python dans ce répertoire
    if os.path.exists(integration_cicd_path):
        for file in os.listdir(integration_cicd_path):
            if file.endswith('.py'):
                full_path = os.path.join(integration_cicd_path, file)
                test_case_global = 'Integration_CI-CD'  # Cas de test global
                sub_test_case = os.path.splitext(file)[0]
                test_description = get_test_description(test_case_global)

                # Créer un identifiant unique pour le cas de test
                test_case_id = f"TST_MONIT{test_case_id_counter}"
                test_case_id_counter += 1

                print(f"\n{'='*50}\nExécution de : {full_path}\n{'='*50}")

                start_time = time.time()  # Enregistrer le temps de début

                try:
                    # Exécution du fichier Python
                    subprocess.run(["python3", full_path], check=True)

                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec succès
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Passed",
                            execution_time=execution_time
                        )
                    )
                except subprocess.CalledProcessError as e:
                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec échec
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Failed",
                            execution_time=execution_time,
                            error_message=str(e)
                        )
                    )
                except Exception as e:
                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec erreur inattendue
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Failed",
                            execution_time=execution_time,
                            error_message=f"Erreur inattendue : {e}"
                        )
                    )

    # Exécuter les autres fichiers Python dans les répertoires restants
    print("\nExécution des autres fichiers Python dans le dépôt :")
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py') and "Integration_CI-CD" not in root:
                full_path = os.path.join(root, file)
                test_case_global = os.path.basename(root)
                sub_test_case = os.path.splitext(file)[0]
                test_description = get_test_description(test_case_global)

                # Créer un identifiant unique pour le cas de test
                test_case_id = f"TST_MONIT{test_case_id_counter}"
                test_case_id_counter += 1

                print(f"\n{'='*50}\nExécution de : {full_path}\n{'='*50}")

                start_time = time.time()  # Enregistrer le temps de début

                try:
                    # Exécution du fichier Python
                    subprocess.run(["python3", full_path], check=True)

                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec succès
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Passed",
                            execution_time=execution_time
                        )
                    )
                except subprocess.CalledProcessError as e:
                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec échec
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Failed",
                            execution_time=execution_time,
                            error_message=str(e)
                        )
                    )
                except Exception as e:
                    end_time = time.time()  # Enregistrer le temps de fin
                    execution_time = round(end_time - start_time, 2)

                    # Collecter les résultats du test avec erreur inattendue
                    test_results.append(
                        collect_test_results(
                            test_case_id=test_case_id,
                            test_case_global=test_case_global,
                            sub_test_case=sub_test_case,
                            test_description=test_description,
                            test_result="Failed",
                            execution_time=execution_time,
                            error_message=f"Erreur inattendue : {e}"
                        )
                    )

    # Affichage du rapport final sous forme de tableau
    if test_results:
        headers = ["Test_Case_ID", "Global Test Case", "Sub-Test Case", "Test_Description",
                   "Test_Result", "Execution_Time", "Test_Execution_Date", "Tester_Name", "Error_Message"]
        print("\n=== Rapport des tests ===")
        print(tabulate(test_results, headers=headers, tablefmt="pretty"))

if __name__ == "__main__":
    # URL du dépôt GitHub
    github_url = "https://github.com/SecuLeague/MONIT1.0.0.git"
    # Chemin vers le répertoire local où cloner le dépôt
    clone_path = "./MONIT1.0.0"

    # Cloner le dépôt s'il n'est pas encore cloné
    clone_repo(github_url, clone_path)

    # Lancer l'exécution des fichiers dans le dépôt cloné
    list_and_execute_files(clone_path)
