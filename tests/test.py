# import pgapp
import pgapp


class Test:
    test = pgapp.DescriptorBasis(int, str, mode="wr")

    def __init__(self):
        self.test = "test"
        self.test = 1


print(Test().test)
