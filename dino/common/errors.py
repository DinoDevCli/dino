from __future__ import annotations


class DinoError(Exception):
    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code


def exit_code(exc: BaseException) -> int:
    if isinstance(exc, DinoError):
        return int(exc.code)
    if isinstance(exc, SystemExit):
        code = exc.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        return 1
    return 1
