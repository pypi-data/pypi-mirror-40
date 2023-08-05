class Layer(object):
    def __init__(self,name):
        self.name=name

    def forword(self):
        pass
    def backword(self):
        pass
    # @staticmethod
    # def animal_talk(obj): #动物叫的接口
    #     obj.talk()

    # def __getattribute__(self, item):
    #     if item == 'a':
    #         print('------%s------' % item)
    #         return '%s is get' % item
    #     else:
    #         return object.__getattribute__(self, item)
class ALayer(Layer):
    def forword(self):
        print("ALayer forword!")
    def backword(self):
        print("ALayer forword!")
class BLayer(Layer):
    def forword(self):
        print("BLayer forword!")
    def backword(self):
        print("BLayer forword!")

c=ALayer('李丽')
d=BLayer('王张')
list = {"c":c, "d":d}
# Animal.animal_talk(list["c"])#多态：一个接口多种实现
# Animal.animal_talk(list["d"]) #一个接口多种实现

list["c"].forword()
list["d"].forword()