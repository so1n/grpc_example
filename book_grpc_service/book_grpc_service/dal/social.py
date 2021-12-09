import datetime
from typing import Any, Dict, List, Optional, TypedDict
from book_grpc_service.helper.conn_proxy import context_proxy


class CommentTypedDict(TypedDict):
    isbn: str
    content: str
    uid: str
    create_time: datetime.datetime


class SocialDal(object):
    @staticmethod
    def like_book(*, isbn: str, like: bool, uid: str):
        with context_proxy.conn.cursor() as cursor:
            ret: int = cursor.execute(
                "INSERT INTO book_like (isbn, `like`, uid) VALUES (%s %s %s)"
                " ON DUPLICATE KEY UPDATE `like`=%s, uid=%s",
                (isbn, int(like), uid, int(like), uid)
            )
            if not ret:
                raise RuntimeError(f"Can not found book by:{isbn}")

    @staticmethod
    def get_book_likes(*, isbn: str) -> Dict[str, Any]:
        with context_proxy.conn.cursor() as cursor:
            cursor.execute(
                "SELECT isbn, sum(`like`) as `like_cnt` FROM book_like WHERE isbn=%s", (isbn, )
            )
            return cursor.fetchone() or {}

    @staticmethod
    def get_book_likes_list(*, isbn: str) -> List[Dict[str, Any]]:
        with context_proxy.conn.cursor() as cursor:
            cursor.execute(
                "SELECT isbn, sum(`like`) as `like_cnt` FROM book_like WHERE isbn in %s GROUP BY isbn",
                (isbn, )
            )
            return cursor.fetchall() or []

    @staticmethod
    def comment_book(*, isbn: str, content: str, uid: str) -> None:
        with context_proxy.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO book_comment (isbn, content, uid) VALUES (%s, %s, %s,)",
                (isbn, content, uid)
            )

    @staticmethod
    def get_book_comment(
            *, isbn: str, create_time: Optional[datetime.datetime] = None, limit: Optional[int] = None
    ) -> List[CommentTypedDict]:
        with context_proxy.conn.cursor() as cursor:
            sql: str = "SELECT * FROM book_comment WHERE isbn=%s"
            param_list: list = [isbn]
            if create_time:
                sql += " WHERE create_time <= %s"
                param_list.append(create_time)
            sql += "ORDER BY create_time desc limit %s"
            param_list.append(limit or 20)
            cursor.execute(sql, param_list)
            return cursor.fetchall() or []


social_dal: SocialDal = SocialDal()
