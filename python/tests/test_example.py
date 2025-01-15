import pytest
import subprocess

def test_game_output():
    # Lancer le script du jeu via subprocess
    result = subprocess.run(['python', 'trivia.py'], capture_output=True, text=True)

    # Lire la sortie générée par le jeu dans game_output.txt
    with open("game_output.txt", "r") as game_output_file:
        game_output = game_output_file.read()

    # Lire la sortie attendue dans expected_output.txt
    with open("expected_output.txt", "r") as expected_output_file:
        expected_output = expected_output_file.read()

    # Comparer les fichiers
    assert game_output == expected_output, "Le contenu du fichier de sortie ne correspond pas au résultat attendu"
