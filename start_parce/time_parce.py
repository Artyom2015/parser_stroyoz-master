import subprocess

def execute_program(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()


# Запуск седьмой программы
execute_program("python sdvor.py")

# Запуск восьмой программы
execute_program("python Petrovich.py")

# Запуск девятой программы
execute_program("python grandline.py")