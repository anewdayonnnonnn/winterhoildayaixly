from abc import ABC, abstractmethod

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self._stock = 0

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self,value):
        if not isinstance(value,(int,float)):
            raise TypeError("库存数量必须是实数")
        if value < 0:
            raise ValueError("库存不能为负数")
            self._stock = value

class Operation(ABC):
    @abstractmethod
    def excute(self,book,quantity):
        pass

class StockIn(Operation):
    def excute(self,book,quantity):
        try:
            book.stock += quantity
            return f"入库 {quantity} 本，操作成功"
        except(TypeError,ValueError) as e:
            return f"入库失败：{str(e)}"

class StockOut(Operation):
    def excute(self, book, quantity):
        try:
            if quantity <= 0:
                raise ValueError(f"出库数量必须大于0（当前传入：{quantity}）")
            if book.stock < quantity:
                raise ValueError(f"库存不足，无法出库！当前库存：{book.stock}，请求出库：{quantity}")
            book.stock -= quantity
            return f"出库 {quantity} 本，操作成功"
        except (ValueError, TypeError) as e:
            return f"出库失败：{str(e)}"

if __name__ =="__main__":
    book = Book("py编程","Tom")
    operations =[StockIn(),StockOut()]

    test_cases = [5,-3,"abc",8]

    for op in operations:
        print(f"\n=== 执行 {op.__class__.__name__} 操作 ===")
        for quantity in test_cases:
            try:
                result = op.excute(book, quantity)
                print(f"数量 {quantity}: {result}")
                print(f"当前库存: {book.stock}")
            except Exception as e:
                print(f"数量 {quantity}: 未知错误 - {str(e)}")