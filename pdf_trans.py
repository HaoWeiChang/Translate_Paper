from pathlib import Path
from google_trans_new import google_translator
import pandas as pd
import csv
import os


class CsvFile:
    def __init__(self) -> None:
        self.columns = ['Document Title', 'PDF Link', 'Abstract']
        self.start = 0
        self.name = ''

    def InterFaceQ(self) -> int:
        interface = """
        ---------------
        0:輸入檔案
        1:選擇範圍(未啟用)
        2:選擇欄位(未啟用)
        3:執行翻譯
        4:離開
        ---------------
        """
        if self.name == '':
            interface += '檔案名稱: \n'
        else:
            interface += """檔案名稱: {}
        行數範圍: {} ~ {}
        已選擇欄位: {}
        """.format(self.name, self.start, self.end, self.columns)
        print(interface)
        mode = input("> ")
        os.system('cls')
        if mode == '0':
            self.File_Input()
        # elif mode == '1':
        #     self.SelectRow()
        # elif mode == '2':
        #     self.SelectCol()
        elif mode == '3':
            self.CreateTransFile()
        elif mode == '4':
            return
        else:
            self.InterFaceQ()
        self.InterFaceQ()

    def File_Input(self):
        path = input("論文csv路徑:\n> ")
        file = Path(path)
        os.system('cls')
        if not file.exists():
            print('檔案不存在，請重新輸入\n')
            return self.File_Input()
        if file.suffix != '.csv':
            print('非csv，請重新輸入\n')
            return self.File_Input()
        self.name = file.stem
        self.df = pd.read_csv(file.resolve())
        self.rows = len(self.df)
        self.end = len(self.df)

    def SelectRow(self):
        print('請輸入範圍(ex: 1,5 or 5)')
        res = list(map(int, input('> ').split(',')))
        if len(res) == 0:
            os.system('cls')
            return self.columns
        if len(res) == 1:
            self.start = res[0]
            self.end = res[1]
        self.end[0]
        return

    def SelectCol(self):
        selected = self.columns
        columns = self.df.columns
        print('*********選擇欄位*********')
        i = 0
        for col in columns:
            show = '{} {}'.format(i, col)
            if col in selected:
                show += 'v'
            i += 1
            print(show)
        print('********請輸入數字********')
        print('********ex: 1 2 3 ********')
        selector = list(map(int, input(">").split(' ')))
        temp = []
        for select in selector:
            temp.append(columns[select])
        item = list(set(temp))
        self.columns = item
        return

    def CreateTransFile(self) -> None:
        df = self.df[self.item]
        df = df.iloc[self.start:self.end]

        filename = self.name[0] + '_trans.csv'

        translator = google_translator()
        trans_row = df.reset_index()
        with open(filename, 'w', newline='', encoding='utf_8_sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['標題', '摘要', '連結'])
            trans_rows = []
            for _, row in trans_row.iterrows():
                res_title = translator.translate(
                    row["Document Title"], lang_src='en', lang_tgt='zh-tw')
                res_abstract = translator.translate(
                    row["Abstract"], lang_src='en', lang_tgt='zh-tw')
                trans_rows.append(
                    [res_title, res_abstract, row["PDF Link"]])
            writer.writerows(trans_rows)
        csvfile.close()
        return


def Loading():
    os.system('cls')
    figma = '-'
    finish = '*'


def main():
    csvfile = CsvFile()
    csvfile.InterFaceQ()


main()
