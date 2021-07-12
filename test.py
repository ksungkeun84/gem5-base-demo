from tasks import add

for i in range(10):
    x = add.delay(2,2)
    print(x)
