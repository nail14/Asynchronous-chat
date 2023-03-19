class PortDescriptor:
    def __init__(self, name, default=None):
        self.name = "_" + name
        self.type = int
        self.value = default if default else 7777

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.value)

    def __set__(self, instance, new_value):
        if not isinstance(new_value, self.type):
            raise TypeError(f"Значение должно быть типа {self.type}")
        if new_value < 0 or new_value > 65535:
            raise ValueError("Значение должно быть от 0 до 65535")
        setattr(instance, self.name, new_value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class TestClass:
    port111 = PortDescriptor(name="port")

    def __init__(self, port_value):
        self.port111 = port_value


if __name__ == '__main__':
    test_class = TestClass(7979)
    print(test_class.port111)
    test_class.port111 = 9090
    print(test_class.port111)