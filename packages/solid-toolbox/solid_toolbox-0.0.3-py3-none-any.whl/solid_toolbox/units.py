#!/usr/bin/env python3


class Vector:
    __slots__ = ("_items", "_len")

    def __init__(self, *items):
        self._items = items
        self._len = len(items)

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return "[" + ", ".join(map(str, self._items)) + "]"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if type(self) == type(other) and len(self) == len(other):
            return all(a == b for a, b in zip(self, other))
        else:
            return False

    def __hash__(self, other):
        return hash(self._items)

    def elem_op(self, op, other, allow_scalar=False):
        if isinstance(other, Vector) and len(self) == len(other):
            return type(self)(*[op(a, b) for a, b in zip(self._items, other._items)])
        elif allow_scalar and isinstance(other, (int, float)):
            return type(self)(*[op(a, other) for a in self._items])
        else:
            return NotImplemented

    def elem_rop(self, op, other, allow_scalar=False):
        if isinstance(other, Vector) and len(self) == len(other):
            return type(self)(*[op(a, b) for a, b in zip(other._items, self._items)])
        elif allow_scalar and isinstance(other, (int, float)):
            return type(self)(*[op(other, a) for a in self._items])
        else:
            return NotImplemented

    def __add__(self, other):
        return self.elem_op(lambda a, b: a + b, other)

    def __sub__(self, other):
        return self.elem_op(lambda a, b: a - b, other)

    def __mul__(self, other):
        return self.elem_op(lambda a, b: a * b, other, True)

    def __rmul__(self, other):
        return self.elem_rop(lambda a, b: a * b, other, True)

    def __truediv__(self, other):
        return self.elem_op(lambda a, b: a / b, other, True)

    def __rtruediv__(self, other):
        return self.elem_rop(lambda a, b: a / b, other, True)

    def __floordiv__(self, other):
        return self.elem_op(lambda a, b: a // b, other, True)

    def __rfloordiv__(self, other):
        return self.elem_rop(lambda a, b: a // b, other, True)

    def __matmul__(self, other):
        return self.dot(other)

    def dot(self, other):
        if isinstance(other, Vector) and len(self) == len(other):
            return sum((self * other)._items)
        else:
            return NotImplemented


class Vec(Vector):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]


class Vec2d(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


Point = Vec
Point2d = Vec2d

mm = 1
cm = 10

x_axis = x_unit = Vec(1, 0, 0)
y_axis = y_unit = Vec(0, 1, 0)
z_axis = z_unit = Vec(0, 0, 1)
