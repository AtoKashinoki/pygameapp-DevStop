# import pgapp
import pgapp
inh = pgapp.inh


class Test(inh.Object):

    def __init__(self):
        super().__init__()
        self.position = (1, 2)
        self.size = (10, 20)
        print(self.rect, self.position, self.size)
        return

    def update(self):
        pass


if __name__ == '__main__':
    test = Test()
