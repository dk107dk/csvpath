import hashlib


class ExpressionUtility:
    @classmethod
    def is_simple_name(cls, s: str) -> bool:
        ret = False
        if s.isdigit():
            return False
        elif s.isalnum():
            ret = True
        elif s.find(".") > -1:
            dotted = True
            dots = s.split(".")
            for d in dots:
                if not cls._is_underscored_or_simple(d):
                    dotted = False
                    break
            if dotted:
                ret = dotted
        else:
            ret = cls._is_underscored_or_simple(s)

        print(
            f"""
            ExpressionUtility.is_simple_name: s: {s},
                digit: {s.isdigit()}, dot: {s.find(".")},
                underscored: {cls._is_underscored_or_simple(s)}
                ret: {ret}
                """
        )
        return ret

    @classmethod
    def _is_underscored_or_simple(cls, s: str) -> bool:
        us = s.split("_")
        ret = True
        for u in us:
            if not u.isalnum():
                ret = False
                break
        return ret

    @classmethod
    def get_id(self, thing):
        # gets a durable ID so funcs like count() can persist throughout the scan
        id = str(thing)
        p = thing.parent
        while p:
            id = id + str(p)
            if p.parent:
                p = p.parent
            else:
                break
        return hashlib.sha256(id.encode("utf-8")).hexdigest()

    @classmethod
    def _dotted(self, s, o):
        if o is None:
            return s
        cs = str(o.__class__)
        cs = cs[cs.rfind(".") :]
        c = cs[0 : cs.find("'")]
        s = f"{c}{s}"
        try:
            return self._dotted(s, o.parent)
        except Exception:
            return s
