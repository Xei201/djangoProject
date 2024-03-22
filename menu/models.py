from collections import namedtuple
from typing import Optional

from django.db import connection, models

from menu.sql import get_three_menu

MenuItemRecord = namedtuple(
    "MenuItemRecord",
    [
        "id",
        "parent_id",
        "title",
        "url",
    ],
)


class MenuItem(models.Model):
    """Menu block"""

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    @classmethod
    def get_entity_parents(cls, name_menu: str, name_path: str) -> Optional["MenuItem"]:
        query = get_three_menu.SQL
        params = {
            "name_path": name_path,
            "name_menu": name_menu,
        }
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            parents_raw = cursor.fetchall()
            if parents_raw:
                parents = [MenuItemRecord(*parent) for parent in parents_raw]
                return parents
        return None

    def __str__(self):
        return self.title
