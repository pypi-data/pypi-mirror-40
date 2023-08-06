import zipfile
from docx import Document
from test_docx.utils import *

import os

TEMP_PATH = './temp'


class Word2Text:
    def __init__(self, filename, dest='.'):
        self.filename = filename
        self.dest = dest

        # get code
        parts = self.filename.split('/')[-1].split('-')
        self.pre_code = '-'.join(parts[:len(parts) - 1])

        self.path = self.dest + '/' + self.pre_code
        self.temp = TEMP_PATH + '/' + self.pre_code
        delete_dir(self.temp)
        ensure_dir(self.path)

        self.questions = {
            'file_code': self.pre_code,
            'filename': self.filename
        }
        self.rels = None

    def transform(self):
        # check file name is docx
        ext = self.filename.split('.')[-1]
        if ext != 'docx':
            return False, 'Only accept docx file'

        zipp = zipfile.ZipFile(self.filename, 'r')
        zipp.extractall(self.temp)
        zipp.close()

        document = Document(self.filename)
        self.rels = document.part.rels

        quests = []
        current = None
        answers_map = {}
        index = 0

        # loop
        table = document.element.body.tbl_lst[0]
        for tr in table.tr_lst:
            meta = tr.tc_lst[0]
            content = tr.tc_lst[1]
            extra = tr.tc_lst[2]

            meta = self._handle_ps(meta.p_lst)
            if meta == '':
                continue
            cmd = int(meta[:1])

            if cmd == 1:
                if current is not None:
                    quests.append(current)

                current = {}
                answers_map = {}
                index = 0

                de = self._handle_ps(content.p_lst, True)
                if de == '':
                    break

                current['code'] = self.pre_code + '-' + meta[2:]
                current['content'] = de
                current['answers'] = []
                current['answers_true'] = None
            elif cmd == 2:
                answers_map[meta[2:]] = index
                index += 1
                current['answers'].append(self._handle_ps(content.p_lst, True))
            elif cmd == 3:
                char = self._handle_ps(content.p_lst)
                current['answers_true'] = answers_map[char]
            elif cmd == 4:
                current['answers_detail'] = self._handle_ps(content.p_lst, True)
            elif cmd == 5:
                current['level'] = int(self._handle_ps(content.p_lst))
            elif cmd == 6:
                current['note'] = self._handle_ps(content.p_lst)

        self.questions['questions'] = quests

        delete_dir(self.temp)

        return True, None

    def _handle_ps(self, ps, is_formated=False):
        texts = []
        for p in ps:
            text = ''
            for r in p.r_lst:
                run = ''
                if len(r.drawing_lst) > 0:
                    for drawing in r.drawing_lst:
                        img_id = str(drawing.inline.graphic.graphicData.pic.blipFill.blip.embed)
                        img = self.rels[img_id].target_ref.split('/')[-1]
                        run += '<img src="' + self.path + '/' + img + '" />'
                        os.rename(self.temp + '/word/media/' + img, self.path + '/' + img)
                else:
                    run = clean(r.text)
                    if is_formated and run != '':
                        if self._is_bold(r.rPr):
                            run = '<b>' + run + '</b>'
                        elif self._is_italic(r.rPr):
                            run = '<i>' + run + '</i>'
                        elif self._is_underline(r.rPr):
                            run = '<u>' + run + '</u>'

                        color = self._is_color(r.rPr)
                        if color is not None:
                            run = '<font color="#' + str(color) + '">' + run + '</font>'
                text = text + ' ' + run
            texts.append(text)
        return clean('<br />'.join(texts))

    @staticmethod
    def _is_bold(rpr):
        return rpr.b is not None and rpr.b.val

    @staticmethod
    def _is_italic(rpr):
        return rpr.i is not None and rpr.i.val

    @staticmethod
    def _is_underline(rpr):
        return rpr.u is not None and rpr.u.val

    @staticmethod
    def _is_color(rpr):
        if rpr.color is not None:
            return rpr.color.val
        return None
