SQL = """
WITH RECURSIVE EntityHierarchy AS (
  SELECT
    id as child_entity,
    parent_id as parent_entity,
    title,
    url
  FROM
    menu_menuitem
  WHERE
    url = :name_path
    or url REGEXP '(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?' || REPLACE(:name_path, '/', '\/')


  UNION

  SELECT
    t.id,
    iif(t.title like :name_menu, null, t.parent_id),
    t.title,
    t.url
  FROM
    menu_menuitem t
  INNER JOIN
    EntityHierarchy eh ON t.id = eh.parent_entity
),
EntityHierarchy2 as (
  SELECT
    child_entity,
    parent_entity,
    title,
    url
  FROM
    EntityHierarchy
  WHERE
    title = :name_menu

  UNION

  SELECT
    t.child_entity,
    t.parent_entity,
    t.title,
    t.url
  FROM
    EntityHierarchy t
  INNER JOIN
    EntityHierarchy2 eh ON t.parent_entity = eh.child_entity
)
select * from EntityHierarchy2
union
select
    id, parent_id, title, url
from menu_menuitem where parent_id = (
select child_entity
from EntityHierarchy2
where url = :name_path
or url REGEXP '(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?' || REPLACE(:name_path, '/', '\/')
);
"""
