# Fuente: https://cosasdedevs.com/posts/primeros-pasos-con-python/

def main():
    try:
        num = int(input("Por favor introduzca un número: "))
    except ValueError as err:
        print(err)


if __name__ == '__main__':
    main()
