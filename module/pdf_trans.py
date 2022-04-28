from pathlib import Path
from google_trans_new import google_translator
import pandas as pd
import csv


class RootFile:
    def __init__(self) -> None:
        self.name = ''
        self.columns = ['Document Title', 'PDF Link', 'Abstract']
        self.start = 0
        self.path = ''

    def Create(self):
        pass

    def Info(self):
        pass


class CsvFile(RootFile):
    def __init__(self) -> None:
        self.name = ''
        self.columns = ['Document Title', 'PDF Link', 'Abstract']
        self.start = 0
        self.path = ''

    def Create(self):
        path = input("論文csv路徑:\n> ")
        file = Path(path)
        if not file.exists():
            raise BaseException('檔案不存在，請重新輸入')
        if file.suffix != '.csv':
            raise BaseException('非csv，請重新輸入')
        self.name = file.stem
        self.path = file.resolve()
        self.df = pd.read_csv(self.path)
        self.rows = len(self.df)
        self.end = len(self.df)
        return CsvFile

    def Menu(self) -> str:
        menu = """---------------
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
        return menu

    def SelectRow(self):
        res = list(map(int, input('> ').split(',')))
        if len(res) == 0:
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
