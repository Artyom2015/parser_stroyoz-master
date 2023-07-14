import subprocess

def execute_program(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()


# Запуск седьмой программы
# execute_program("python Msk_saturn1.py")

# Запуск восьмой программы
# execute_program("python Petrovich.py")

# Запуск девятой программы
execute_program("python Oz_saturn.py")

# Запуск седьмой программы
execute_program("python Akson.py")

# Запуск восьмой программы
execute_program("python dvoroz.py")

# Запуск девятой программы
execute_program("python famarket.py")

# Запуск седьмой программы
execute_program("python grandline.py")

# Запуск восьмой программы
execute_program("python grmsd.py")

# Запуск девятой программы
execute_program("python maxidom.py")

# Запуск седьмой программы
execute_program("python parce_discont.py")

# Запуск восьмой программы
execute_program("python parce_otvinta.py")

# Запуск девятой программы
execute_program("python parce_staroyoz.py")

# Запуск седьмой программы
execute_program("python sdvor.py")

# Запуск восьмой программы
execute_program("python stroimaks.py")

# Запуск девятой программы
execute_program("python stroydomsale.py")

# Запуск седьмой программы
execute_program("python vertical.py")

# Запуск восьмой программы
execute_program("python vsksnab.py")

# Запуск девятой программы
execute_program("python convert.py")