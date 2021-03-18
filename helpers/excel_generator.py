from datetime import datetime
import os
import uuid

from django.conf import settings
import xlwt

from transact.models import UserTransaction


class ExcelGenerator:
    model = UserTransaction

    def get_file_path(self):
        self.download_dir_path = os.path.join(settings.MEDIA_ROOT, "downloads")
        if not os.path.exists(self.download_dir_path):
            os.makedirs(self.download_dir_path)
        self.filename = "request_" + "Transaction" + "_" + str(uuid.uuid4())[-4:] + ".xls"
        self.file_path = os.path.join(self.download_dir_path, self.filename)
        return self.file_path

    def create_file(self, obj_id=[], user_ids=[]):
        wb = xlwt.Workbook('utf-8')
        for user_id in user_ids:
            xlsx_sheet = wb.add_sheet(
                'report for user id %s' % str(user_id), cell_overwrite_ok=True)
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            row_num = 0
            columns = ['TimeStamp', 'Transaction Type', 'Amount']

            for col_num in range(len(columns)):
                xlsx_sheet.write(
                    row_num, col_num, columns[col_num], font_style)
            row_num += 1
            queryset = self.model.objects.filter(
                id__in=obj_id, user__id=user_id)
            for obj in queryset:
                timestamp_str = datetime.strftime(obj.timestamp, "%Y-%m-%d %H:%M:%S")
                xlsx_sheet.write(
                    row_num, columns.index('TimeStamp'), timestamp_str)
                if obj.is_debit:
                    xlsx_sheet.write(
                        row_num, columns.index('Transaction Type'), 'Debit')
                else:
                    xlsx_sheet.write(
                        row_num, columns.index('Transaction Type'), 'Credit')
                xlsx_sheet.write(row_num, columns.index('Amount'), obj.amount)
                row_num += 1
        wb.save(self.file_path)

    def run(self, obj, user_id=[]):
        self.get_file_path()
        self.create_file(obj_id=obj, user_ids=user_id)       
        return self.file_path
