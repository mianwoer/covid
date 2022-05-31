
def fun2():
    try:
        a = 1/0
    except Exception as e:
        print("1")
        raise e
    finally:
        print("2")
        return a


if __name__ == '__main__':
    print(fun2())
    # fun2()