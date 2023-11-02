# import sys
import sys
# import pgapp
import pgapp
inh = pgapp.inh


class TestUI(inh.UI):

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
