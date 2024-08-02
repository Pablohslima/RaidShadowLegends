import subprocess

def git_auto_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Automatic commit"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Alterações enviadas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro: {e}")


"""
============== Excluir alteraçoes realizadas no documento ==============
    git checkout -- generator.py
"""

if __name__ == "__main__":
    git_auto_push()