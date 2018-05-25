# -*- coding: utf-8 -*-
class Language(object):
    ENUS = "enus"
    ZHTW = "zhtw"
    ZHCN = "zhcn"

    @staticmethod
    def to_dict():
        lan = Language()
        to_dict = dict()
        for key in dir(lan):
            val = getattr(lan, key)
            if key.startswith("__"):
                continue
            if callable(val):
                continue
            to_dict[key] = val
        return to_dict


class ProductInfoFactory(object):
    @staticmethod
    def create_product_info(language):
        if language == Language.ENUS:
            return ProductInfoENUS()
        elif language == Language.ZHTW:
            return ProductInfoZHTW()
        elif language == Language.ZHCN:
            return ProductInfoZHCN()
        else:
            return ProductInfoENUS()


class BaseProductInfo(object):
    def __init__(self):
        self.list_of_recognizable_product = u"undefined"
        self.product_id = u"undefined"
        self.product_name = u"undefined"
        self.sample_image = u"undefined"


class ProductInfoENUS(BaseProductInfo):
    def __init__(self):
        super(ProductInfoENUS, self).__init__()
        self.list_of_recognizable_product = u"List of Recognizable Product"
        self.product_id = u"Product ID"
        self.product_name = u"Product Name"
        self.sample_image = u"Sample Image"


class ProductInfoZHTW(BaseProductInfo):
    def __init__(self):
        super(ProductInfoZHTW, self).__init__()
        self.list_of_recognizable_product = u"可辨識商品清單"
        self.product_id = u"商品編號"
        self.product_name = u"商品名稱"
        self.sample_image = u"商品圖片"


class ProductInfoZHCN(BaseProductInfo):
    def __init__(self):
        super(ProductInfoZHCN, self).__init__()
        self.list_of_recognizable_product = u"可辨识商品清单"
        self.product_id = u"商品编号"
        self.product_name = u"商品名称"
        self.sample_image = u"商品图片"
