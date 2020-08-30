# Fuente: https://cosasdedevs.com/posts/primeros-pasos-con-python/

def main():
    print('Introduce tu nombre')
    nombre = input()
    print(f'Hola {nombre}')
    print('Hola ' + nombre)

    mensaje = "El nombre ingresado es {}."
    print(mensaje.format(nombre.upper()))


if __name__ == '__main__':
    main()