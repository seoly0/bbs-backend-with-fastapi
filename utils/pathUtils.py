from typing import Union
from urllib.parse import quote


class QueryString:
    map: dict = {}

    def __init__(self, init: Union[dict, str, "QueryString"] = {}) -> None:
        if type(init) == dict:
            self.map = dict(init)
        elif type(init) == QueryString:
            self.map = dict(init.map)
        elif type(init) == str:
            query = init.split("&")
            for kv in query:
                self.map.update({kv.split("=")[0]: kv.split("=")[1]})
        else:
            raise TypeError

    def __repr__(self) -> str:
        return self.toString()

    def __and__(self, other: Union[dict, "QueryString"]):
        if type(other) not in [dict, QueryString]:
            raise TypeError("operands must be dict or QueryString")

        ret = {}
        if type(other) == dict:
            ret.update(self.map)
            ret.update(other)
        elif type(other) == QueryString:
            ret.update(self.map)
            ret.update(other.map)
        return QueryString(ret)

    def isEmpty(self):
        return self.map == {}

    def toString(self):
        map = []
        for k, v in self.map.items():
            map.append(f"{quote(k)}={quote(v)}")
        return "&".join(map)

    def toDict(self):
        return dict(self.map)


class HttpURL:
    scheme: str  # = "http"
    domain: str  # = ""
    path: str  # = ""
    query: QueryString  # = QueryString()

    def __init__(self, url: Union[str, "HttpURL"] = "") -> None:
        if type(url) == str:
            qs = url.split("?")[1] if len(url.split("?")) > 1 else {}
            url = url.split("?")[0]
            self.scheme = url.split("://")[0] if url.find("://") > -1 else "http"
            self.domain = url.removeprefix(self.scheme + "://").split("/")[0]
            self.path = url.removeprefix(self.scheme + "://" + self.domain)
            self.query = QueryString(qs)

        elif type(url) == HttpURL:
            self.scheme = url.scheme
            self.domain = url.domain
            self.path = url.path
            self.query = QueryString(url.query)

        else:
            raise TypeError

    def __repr__(self) -> str:
        return self.toString()

    def __and__(self, other: dict | QueryString) -> "HttpURL":
        if type(other) not in [dict, QueryString]:
            raise TypeError("operands must be dict or QueryString")

        if type(other) == dict:
            other = QueryString(other)

        new = HttpURL(self)
        new.query = new.query & other
        return new

    def __truediv__(self, other: str) -> "HttpURL":
        if type(other) not in [str]:
            raise TypeError("operands must be str")

        l = self.path.rstrip("/")
        r = str(other).lstrip("/")
        ret = HttpURL(self)
        ret.path = "/".join([l, r])
        return ret

    def toString(self):
        return f"{self.scheme}://{self.domain}{self.path}" + (
            f"?{self.query.toString()}" if not self.query.isEmpty() else ""
        )


def parse_order(entity: any, order: str):
    result = []
    try:
        t: str = order.split(",")
        for i in t:
            p = i.split(".")
            if hasattr(entity, p[0]):
                if len(p) > 1 and p[1] == "asc":
                    result.append(getattr(entity, p[0]).asc())
                result.append(getattr(entity, p[0]).desc())

        return result

    except:
        return None

