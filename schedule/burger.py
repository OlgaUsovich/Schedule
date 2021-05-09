def sausage():
    return 'sausage'


def bun(f):
    def new_f():
        return f() + ' buns'
    return new_f


@bun
def meat():
    return 'meat'


def main():
    бутер = sausage
    buter2 = bun(sausage)()
    buter3 = meat()
    print(бутер, buter2, buter3)


if __name__ == '__main__':
    main()
