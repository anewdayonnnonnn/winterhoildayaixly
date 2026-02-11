import math

class Shape:
    """图形基类"""
    # 类变量，记录创建的所有图形数量
    shape_count = 0

    def __init__(self):
        # 私有属性:面积
        self.__area = None
        # 创建实例时候计数
        Shape.shape_count  += 1

    def _calc_area(self):
        """计算面积的私有办法"""
        raise NotImplementedError("子类重新实现此方法")

    def get_area(self):
        """获取面积"""
        if self.__area is None:
            self.__area = self._calc_area()
        return self.__area

    @classmethod
    def get_shape_count(cls):
        """获取创建的图形总数"""
        return cls.shape_count

class Circle(Shape):
    """圆形"""

    def __init__(self, radius):
        super().__init__()
        # 实例变量：园的半径
        self.radius = radius

    def _calc_area(self):
        """重写面积计算"""
        return math.pi * self.radius ** 2

    def __str__(self):
        return f"圆形(半径={self.radius}, 面积={self.get_area():.2f})"

class Rectangle(Shape):
    """矩形类"""

    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width

    def _calc_area(self):
        """重写面积计算"""
        return self.length * self.width

    def __str__(self):
        return f"矩形(长={self.length}, 宽={self.width}, 面积={self.get_area():.2f})"

class Triangle(Shape):
    """三角形类"""

    def __init__(self, base, height):
        super().__init__()
        self.base = base
        self.height = height

    def _calc_area(self):
        return 0.5 * self.base * self.height

    def __str__(self):
        return f"三角形(底={self.base}, 高={self.height}, 面积={self.get_area():.2f})"

if __name__ == "__main__":
    circle = Circle(2)
    rectangle = Rectangle(2, 3)
    triangle = Triangle(2, 3)

    shapes = [circle, rectangle, triangle]
    for shape in shapes:
        print(f"{shape} - 面积: {shape.get_area():.2f}")

    print(f"\n创建的图形总数: {Shape.get_shape_count()}")