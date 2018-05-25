#!/usr/bin/python
# -*- coding: utf-8 -*-

from recog_app.constants import config_constant
from recog_app.etc.wording import ProductInfoFactory


def generate_html(title, content):
    html = """
        <html>
        <body>
            <center>
            <h1>%s</h1>
            </center>
            %s
        </body>
        </html>
    """ % (title, content)
    return html


def get_products_table(products, language):
    product_info = ProductInfoFactory.create_product_info(language=language)
    style = """
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    """

    column_row = """
    <tr>
        <th>%s</th>
        <th>%s</th> 
        <th>%s</th>
    </tr>
    """ % (product_info.product_id, product_info.product_name, product_info.sample_image)

    product_rows = ""
    for product in products:
        product_rows += get_product_row(product)

    products_table = """
    %s
    <center>
    <table style=\"table-layout:fixed;width:90%%\">
    %s
    %s
    </table>
    </center>
    """ % (style, column_row, product_rows)
    return products_table


def get_product_row(product):
    product_row = """
    <tr>
        <td align=\"center\">%s</td>
        <td align=\"center\">%s</td> 
        <td align=\"center\"><img src=%s width=200 height=150 display=block></img></td>
    </tr>
    """ % (product.get(config_constant.PRODUCT_ID), product.get(config_constant.PRODUCT_NAME), product.get(config_constant.PRODUCT_IMAGE_URL))
    return product_row
