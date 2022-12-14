from enum import Enum
from typing import Iterable, List

from django.contrib.auth.models import Permission


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class AccountPermissions(BasePermissionEnum):
    MANAGE_USERS = "account.manage_users"
    MANAGE_STAFF = "account.manage_staff"
    MANAGE_SERVICE_ACCOUNTS = "app.manage_apps"
    MANAGE_MEMOS = "account.manage_memos"


class AppPermission(BasePermissionEnum):
    MANAGE_APPS = "app.manage_apps"


class DiscountPermissions(BasePermissionEnum):
    MANAGE_DISCOUNTS = "discount.manage_discounts"


class PluginsPermissions(BasePermissionEnum):
    MANAGE_PLUGINS = "plugins.manage_plugins"


class GiftcardPermissions(BasePermissionEnum):
    MANAGE_GIFT_CARD = "giftcard.manage_gift_card"


class MenuPermissions(BasePermissionEnum):
    MANAGE_MENUS = "menu.manage_menus"


class CheckoutPermissions(BasePermissionEnum):
    MANAGE_CHECKOUTS = "checkout.manage_checkouts"


class OrderPermissions(BasePermissionEnum):
    MANAGE_ORDERS = "order.manage_orders"


class PagePermissions(BasePermissionEnum):
    MANAGE_PAGES = "page.manage_pages"


class ProductPermissions(BasePermissionEnum):
    MANAGE_PRODUCTS = "product.manage_products"
    MANAGE_CREATEPRODUCT = "product.manage_createproduct"
    MANAGE_EVENT = "product.manage_event"


class ProductTypePermissions(BasePermissionEnum):
    MANAGE_PRODUCT_TYPES_AND_ATTRIBUTES = "product.manage_product_types_and_attributes"


class BankPermissions(BasePermissionEnum):
    VIEW_DEPOSITS = "bank.view_deposits"


class ShippingPermissions(BasePermissionEnum):
    MANAGE_SHIPPING = "shipping.manage_shipping"


class SitePermissions(BasePermissionEnum):
    MANAGE_SETTINGS = "site.manage_settings"
    MANAGE_TRANSLATIONS = "site.manage_translations"

class CalculatePermissions(BasePermissionEnum):
    MANAGE_CALCULATE = "copyright.manage_calculate"

# class CopyrightPermissions(BasePermissionEnum):
#     MANAGE_COPYRIGHTS = "copyright.manage_copyrights"

class InformationPermissions(BasePermissionEnum):
    MANAGE_INFORMATION = "statistics.manage_information"


PERMISSIONS_ENUMS = [
    AccountPermissions,
    AppPermission,
    DiscountPermissions,
    PluginsPermissions,
    GiftcardPermissions,
    MenuPermissions,
    OrderPermissions,
    PagePermissions,
    ProductPermissions,
    BankPermissions,
    ProductTypePermissions,
    ShippingPermissions,
    SitePermissions,
    CheckoutPermissions,
    CalculatePermissions,
    InformationPermissions,
]


def split_permission_codename(permissions):
    return [permission.split(".")[1] for permission in permissions]


def get_permissions_codename():
    return [
        enum.codename 
        for permission_enum in PERMISSIONS_ENUMS 
        for enum in permission_enum
        ]

def get_permissions_enum_dict():
    return {
        enum.name: enum
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    }


def get_permissions_from_names(names: List[str]):
    """Convert list of permission names - ['MANAGE_ORDERS'] to Permission db objects."""
    permissions = get_permissions_enum_dict()
    return get_permissions([permissions[name].value for name in names])


def get_permission_names(permissions: Iterable["Permission"]):
    """Convert Permissions db objects to list of Permission enums."""
    permission_dict = get_permissions_enum_dict()
    names = set()
    for perm in permissions:
        for _, perm_enum in permission_dict.items():
            if perm.codename == perm_enum.codename:
                names.add(perm_enum.name)
    return names


def get_permissions_enum_list():
    return [
        (enum.name, enum.value) 
        for permission_enum in PERMISSIONS_ENUMS 
        for enum in permission_enum
        ]


def get_permissions(permissions=None):
    if permissions is None:
        codenames = get_permissions_codename()
    else:
        codenames = split_permission_codename(permissions)
    return (
        Permission.objects.filter(codename__in=codenames)
        .prefetch_related("content_type")
        .order_by("codename")
    )
