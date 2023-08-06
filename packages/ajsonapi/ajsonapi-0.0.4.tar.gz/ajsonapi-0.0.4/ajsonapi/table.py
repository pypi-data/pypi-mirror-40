# Copyright © 2018-2019 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module table provides class Table."""

from asyncio import create_task, wait
from itertools import chain

from toposort import toposort

from ajsonapi.attribute import Attribute
from ajsonapi.conversions import pascal_to_snake
# pylint: disable=unused-import
from ajsonapi.relationships import (LocalRelationship, ManyToManyRelationship,
                                    ManyToOneRelationship, Relationship)
from ajsonapi.uri.collection import Collection


class Table:
    """Class Table is the Python representation of an SQL table."""

    by_class_name = {}

    @classmethod
    def __init_subclass__(cls):
        # pylint: disable=too-many-branches
        if cls.__name__ in ['JSON_API', 'AssociationTable']:
            return
        cls.name = cls.__name__
        collection_name = pascal_to_snake(cls.__name__)
        cls.collection = Collection(collection_name, cls)
        Collection.by_name[collection_name] = cls.collection
        cls.attributes = []
        cls.relationships = []
        cls.local_relationships = []
        cls.columns = []
        cls.constraints = []
        cls.pool = None

        # Update relationships to class 'cls' for classes in cls.by_class_name.
        for table in Table.by_class_name.values():
            for col in table.__dict__.values():
                if isinstance(col, Relationship):
                    if col.rtable == cls.__name__:
                        col.rtable = cls
                    if isinstance(col, ManyToManyRelationship):
                        if col.atable == cls.__name__:
                            col.atable = cls

        # Now insert cls in by_class_name in case it contains a relationship to
        # itself. That way the next code section resolves the circular
        # dependency.
        Table.by_class_name[cls.__name__] = cls

        # Update attributes and relationships in cls.
        for name, col in cls.__dict__.items():
            if isinstance(col, Attribute):
                col.name = name
                cls.columns.append(col)
                cls.attributes.append(col)
            elif isinstance(col, Relationship):
                col.name = name
                cls.relationships.append(col)
                col.table = cls
                col.collection = cls.collection
                if isinstance(col, LocalRelationship):
                    cls.local_relationships.append(col)
                    cls.columns.append(col)
                    cls.constraints.append(col)
                elif (isinstance(col, ManyToManyRelationship) and
                      isinstance(col.atable, str)):
                    if col.atable in Table.by_class_name:
                        col.atable = Table.by_class_name[col.atable]
                    else:
                        lclassname = cls.__name__
                        if isinstance(col.rtable, str):
                            rclassname = col.rtable
                        else:
                            rclassname = col.rtable.__name__
                        cls_def = (f"class {col.atable}(AssociationTable):\n"
                                   f"    rel0 = ManyToOneRelationship"
                                   f"('{lclassname}', lfkey='{col.lafkey}')\n"
                                   f"    rel1 = ManyToOneRelationship"
                                   f"('{rclassname}', lfkey='{col.rafkey}')\n")
                        # pylint: disable=exec-used
                        exec(compile(cls_def, '<string>', 'exec'))
                if (isinstance(col.rtable, str) and
                        col.rtable in Table.by_class_name):
                    col.rtable = Table.by_class_name[col.rtable]
                    for rel in col.rtable.relationships:
                        if col.is_reverse(rel):
                            rel.reverse = col
                            col.reverse = rel
                            break

    @classmethod
    async def create(cls):
        """Creates the SQL table, which represents this association table
        class.

        Args:
            pool: Connection pool to the database in which to create the SQL
                tables for this class of the object model.
        """
        table_fields = ',\n    '.join(
            chain((col.sql() for col in cls.columns),
                  (col.sql_constraints() for col in cls.constraints)))
        stmt = f'CREATE TABLE {cls.name} (\n    {table_fields}\n);\n'
        async with cls.pool.acquire() as connection:
            await connection.execute(stmt)

    @classmethod
    async def select(cls, *columns, where=None):
        """Executes an SQL select statement."""

        if where:
            stmt = (f"SELECT {', '.join(str(col) for col in columns)}\n"
                    f"FROM {cls.name}\n"
                    f"WHERE {where};\n")
        else:
            stmt = (f"SELECT {', '.join(str(col) for col in columns)}\n"
                    f"FROM {cls.name};\n")
        async with cls.pool.acquire() as connection:
            return await connection.fetch(stmt)

    @classmethod
    async def insert_many(cls, tuples, *columns):
        """Executes the SQL insert statement for multiple rows."""

        cols = ', '.join(col for col in columns)
        values = ', '.join(f'${i}' for i in range(1, len(columns) + 1))
        stmt = f'INSERT INTO {cls.name} ({cols})\nVALUES ({values})\n'
        async with cls.pool.acquire() as connection:
            return await connection.executemany(stmt, tuples)

    @classmethod
    async def delete(cls, where):
        """Executes an SQL delete statement."""

        stmt = f'DELETE FROM {cls.name} WHERE {where};\n'
        async with cls.pool.acquire() as connection:
            return await connection.execute(stmt)

    @classmethod
    async def update(cls, *, where=None, **columns):
        """Executes an SQL update statement."""

        def value_to_sql(value):
            if value is None:
                return 'null'
            return repr(value)

        assignments = ', '.join(
            f'{col} = {value_to_sql(value)}' for col, value in columns.items())
        if where:
            stmt = f'UPDATE {cls.name} SET {assignments} WHERE {where};\n'
        else:
            stmt = f'UPDATE {cls.name} SET {assignments};\n'
        async with cls.pool.acquire() as connection:
            return await connection.execute(stmt)

    @classmethod
    def dependencies(cls):
        """Fetches the creation dependencies for this class.

        Returns:
            A set of classes whose tables must be created before this class's
            table.
        """
        return {rel.rtable for rel in cls.local_relationships}


class AssociationTable(Table):
    """Class AssociationTable is the Python representation of an SQL
    association table.
    """

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.constraints.append(cls)

    @classmethod
    def sql_constraints(cls):
        """Returns the constraints for classes derived from AssociationTable."""
        return (f"UNIQUE "
                f"({', '.join(rel.lfkey for rel in cls.local_relationships)})")


async def create_all():
    """Creates the SQL tables for the classes in the object model."""

    dependencies = {
        table: table.dependencies() for table in Table.by_class_name.values()
    }
    for tables in toposort(dependencies):
        tasks = {create_task(table.create()) for table in tables}
        await wait(tasks)


def init(pool):
    """Initializes all user Table subclasses."""

    for table in Table.__subclasses__():
        if table.__name__ != 'JSON_API':
            table.pool = pool
    for table in AssociationTable.__subclasses__():
        table.pool = pool
