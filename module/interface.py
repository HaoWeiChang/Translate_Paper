from . import pdf_trans
import os


def ClearConsole():
    command = 'clear'
    if os.name in ('nt', 'doc'):
        command = 'cls'
    os.system(command)


def ErrorShowHandler(err):
    print(err)
    print('請輸入任意按鍵進行')
    input('> ')
    ClearConsole()


class InterFace:
    __root_layout = """---------------
{}
---------------
{}
"""

    __menu_layout = """0:建立翻譯檔案
1:選擇翻譯檔案
2:顯示翻譯進度
3:離開
"""

    def __init__(self) -> None:
        self.show = self.__root_layout
        self.projects = []
        self.progress = []

    def Show(self, main: str, secondary: str = ""):
        secondary = secondary if secondary != ""else "輸入數字"
        self.show = self.__root_layout.format(main, secondary)
        print('\r'+self.show)

    def Menu(self):
        try:
            ClearConsole()
            self.Show(self.__menu_layout)
            mode = input('> ')
            ClearConsole()
            if mode == '0':
                self.Create()
            if mode == '1':
                self.Choose()
            if mode == '3':
                return
            self.Menu()
        except BaseException as err:
            ClearConsole()
            ErrorShowHandler(err)
            self.Menu()

    def Create(self):
        try:
            if len(self.projects) == 3:
                return print('\r'+'創建已滿')
            project = pdf_trans.CsvFile()
            project.Create()
            if project == None:
                self.Create()
            if len(self.projects) is None:
                self.projects = []
                self.projects.append(project)

            for proj in self.projects:
                if project.path == proj.path:
                    res = input('是否需要覆蓋(y/n)\n')
                    res = res.lower()
                    while res != 'y' or res != 'n':
                        if res.lower() == 'n':
                            break
                        self.projects.remove(proj)
                        self.projects.append(project)

            self.projects.append(project)

            return
        except BaseException as err:
            ClearConsole()
            ErrorShowHandler(err)
            self.Menu()

    def Choose(self):
        if len(self.projects) == 0:
            raise BaseException('沒有翻譯專案')
        for index, proj in enumerate(self.projects):
            showtxt = "{} {}".format(index, proj.name)
        self.Show(showtxt)
        while True:
            res = input('> ')
            if res > str(len(self.projects)) or res < '0':
                continue
            csvfile = self.projects[int(res)]
            self.FileMenu(csvfile)
            break

    def FileMenu(self, csvfile: pdf_trans.CsvFile):
        csvfile.Menu()
        res = input('> ')
        pass
