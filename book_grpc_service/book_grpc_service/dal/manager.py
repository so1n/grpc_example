import datetime
from typing import TypedDict, Optional, List
from book_grpc_service.helper.conn_proxy import context_proxy


class BookTypedDict(TypedDict):
    isbn: str
    book_name: str
    author: str
    book_desc: str
    book_url: str


class ManagerDal(object):
    @staticmethod
    def create_book(*, isbn: str, book_name: str, author: str, book_desc: str, book_url: str) -> None:
        with context_proxy.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO book_info (isbn, book_name, author, book_desc, book_url) VALUES (%s, %s, %s, %s, %s)",
                (isbn, book_name, author, book_desc, book_url)
            )

    @staticmethod
    def delete_book(*, isbn: str) -> None:
        with context_proxy.conn.cursor() as cursor:
            ret: int = cursor.execute("UPDATE book_info SET deleted=1 WHERE isbn=%s", (isbn, ))
            if not ret:
                raise RuntimeError(f"Can not found book by:{isbn}")

    @staticmethod
    def get_book(*, isbn: str) -> BookTypedDict:
        with context_proxy.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM book_info WHERE isbn=%s and deleted=0", (isbn, ))
            book_info_dict: BookTypedDict = cursor.fetchone() or {}
            if not book_info_dict:
                raise RuntimeError(f"Can not found book by:{isbn}")
            return book_info_dict

    @staticmethod
    def get_book_list(
            *, create_time: Optional[datetime.datetime] = None, limit: Optional[int] = None
    ) -> List[BookTypedDict]:
        with context_proxy.conn.cursor() as cursor:
            sql: str = "SELECT * FROM book_info WHERE deleted=0"
            param_list: list = []
            if create_time:
                sql += " AND create_time <= %s"
                param_list.append(create_time)
            sql += "ORDER BY create_time desc limit %s"
            param_list.append(limit or 20)
            cursor.execute(sql, param_list)
            return cursor.fetchall() or []


manager_dal: ManagerDal = ManagerDal()
