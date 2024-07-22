class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector2D(x={self.x}, y={self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return 2

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            raise TypeError('Unsupported operand type')

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('Index out of range')

    def __call__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __getattr__(self, item):
        if item == 'magnitude':
            return (self.x ** 2 + self.y ** 2) ** 0.5
        else:
            raise AttributeError(f"'Vector2D' object has no attribute '{item}'")


v1 = Vector2D(10, 3)
v2 = Vector2D(3, 2)

# __repr__
print(v1)

# __len__
print(len(v1))

# __add__
print(v1 + v2)

# __sub__
print(v1 - v2)

# __mul__
print(v1 * 2)
print(v1 * v2)

# __getitem__
print(v1[0], v1[0])

# __call__
print(v1(2))

# __getattr__
print(v1.magnitude)
