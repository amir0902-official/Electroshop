from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
import xlwt

from .models import Product, Category, Photo, Data


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    print(queryset.values_list('name', 'price', 'quantity', 'status'))
    serializers.serialize("json", queryset, stream=response)
    return response


export_as_json.short_description = 'خروجی json'


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

    rows = queryset.values_list('name', 'humanize_price', 'quantity', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_products.short_description = 'خروجی اکسل'


def make_active(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    if updated == 1:
        msg = 'فعال شد.'
    else:
        msg = 'فعال شدند.'

    modeladmin.message_user(request, f'{updated} مورد {msg}', messages.SUCCESS)


make_active.short_description = 'فعال کردن موارد انتخاب شده'


def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    if updated == 1:
        msg = 'شد.'
    else:
        msg = 'شدند.'

    modeladmin.message_user(request, f'{updated} مورد غیرفعال {msg}', messages.WARNING)


make_inactive.short_description = 'غیرفعال کردن موارد انتخاب شده'
