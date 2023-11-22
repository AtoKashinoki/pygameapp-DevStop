# import sys
import sys
# import pgapp
import pgapp
inh = pgapp.inh


class TestSurface(inh.Surface):

    def __init__(self):
        super().__init__((100, 100))
        self.surface.fill("black")
        return

    def update(self, owners: tuple[inh.Application]):
        self.position += [2, 1]
        self.size += [1, 1]
        if owners[0].get_key_pressed[self.pygame.K_k]:
            self.kill()
        return


class TestObject(inh.Object):

    def __init__(self):
        super().__init__()
        self.objects["test_surface"] = TestSurface()
        return

    def update(self, owners: tuple):
        return


class TestUI(inh.UI):
    def __init__(self):
        super().__init__("white")
        self.objects["test_obj"] = TestObject()
        return

    def update(self, owners):
        return


class Test(inh.Application):

    def __init__(self):
        super().__init__("test")
        self.UIs["testUI"] = TestUI()
        self.start_UI_key = "testUI"
        return


if __name__ == '__main__':
    test = Test()
    test.exe()
    sys.exit()
