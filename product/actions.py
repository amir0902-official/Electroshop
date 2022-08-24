from django.http import HttpResponse
import xlwt

from .models import Product, Category, Photo, Data


def export_products(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['نام', 'قیمت', 'موجودی', "وضعیت", ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = queryset.values_list('name', 'price', 'quantity', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_products.short_description = 'خروجی اکسل'
