import csv
from lib2to3.pgen2.pgen import DFAState
from pathlib import Path
from signal import raise_signal
from google_trans_new import google_translator
import pandas as pd


class CsvFile:
    def __init__(self, path: str) -> None:
        self.name = ''
        self.path = ''
        self.columns = ['PDF Link']
        self.trans = ['Document Title', 'Abstract']
        self.start = 0
        self.end = 0
        self.rows = 0
        self._new(path)

    def _new(self, path: str):
        file = Path(path)
        if not file.exists():
            raise BaseException('檔案不存在，請重新輸入')
        if file.suffix != '.csv':
            raise BaseException('非csv，請重新輸入')
        self._df = pd.read_csv(self.path, encoding='utf-8')
        self.name = file.stem
        self.path = file.resolve()
        self._columns = self._df.columns
        self.end = len(self._df)
        self.rows = len(self._df)

    def select_row(self, start: int = 0, end: int = 0):
        if start < 0 or end < 0:
            raise BaseException("Negative number")
        if end < start:
            raise BaseException("End_Row can't be less than Start_Row")
        self.start = 0 if start == 0 else start
        self.end = self.rows if end == 0 else end

    def select_column(self, column: list(int)):
        if len(column) == 0:
            self.columns = ['PDF Link']
            return
        if not 0 <= column < len(self.columns):
            raise BaseException('column not in range')
        column = list(set(column))
        temp = self.columns
        for select in column:
            temp.append(self.columns[select])
        self.columns = list(set(temp))

    @property
    def get_column(self) -> list(str):
        return self._columns

    def create_trans_csv(self):
        trans = self.trans
        columns = self.columns
        df = self._df[trans+columns]
        df = df.iloc[self.start:self.end]
        trans_rows = df.reset_index()
        filename = self.name + '_trans'
        with open(filename, mode='w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow()
        trans_result = []
        for _, row in trans_rows.iterrows():
            res1: str = self.__trans(row[self.trans[0]])
            res2: str = self.__trans(row[self.trans[1]])
            temp = [res1, res2]
            for col in columns:
                temp.append(row[col])

            trans_result.append(temp)

        csvfile.close()

    def __trans(trans_str: str) -> str:
        translator = google_translator()
        return translator.translate(
            trans_str, lang_src='en', lang_tgt='zh-tw')
