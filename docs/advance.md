### Good practise create virtual env

virtualenv venv && source venv/bin/activate
# Look up what installed
```
pip freeze
pip install flask
pip freeze > requirements.txt
pip instlal -r requirements.txt
```
### *args, **kwards
* *Все входящие аргументы в кортеж
* sum Сумма всех чисел из кортежа args

```
def add(*args):
    print(sum(args))
add(10,20,230)
```

* Засосвуем список 
l = [1,2,3]
add(*l)

* **kwargs засовуем в словарь

###  if __name __ == '__main__

* Выводит все операции
print(globals())

* Если запущенно было из исходного файла, то работает функция main (PS - ЭТО ТОЧКА ВХОДА)

### Генераторы списков (List comprehension)
* К примеру мы обращаемся к ключу 'car', но его может и не быть

(values) = [ (expression) for (value) in (collection) ]

```

jack = {
    'name': 'jack',
    'car': 'bmw'
}
igor = {
    'name': 'igor',
}

users = [jack, igor]

# List comprehension
cars = [person.get('car', '') for person in users]
print(cars)

```

### Filer (Фильтрация) по Первому элементу 
```
names = ['igor', 'Serhei', 'Marina']
new_name = [n for n in names if n.startswith('M')]
print(new_name)

```
### Генераторы быстрее (Замеряем время)
```

from datetime import datetime

def one():
    start = datetime.now()
    l = []
    for i in range(10**4):
        if i % 2 == 0:
            l.append(i)
    print(datetime.now() - start )
    return l

def two():
    start = datetime.now()

    l = [x for x in range(10**4) if x % 2 == 0]
    print(datetime.now() - start )

    return l

l1 = one()
l2 = two()

```
### ДЕКОРАТОРЫ, чтобы куча раз не описывать переменные для функции, мы её ошишим один раз

```
from datetime import datetime

def whattime(func):
    def wrapper():
        start = datetime.now()
        result = func()
        print(datetime.now() - start)
        return result
    return wrapper


@whattime
def two():
    # start = datetime.now() тоже самое если бы тут была это переменная 
    l = [x for x in range(10**4) if x % 2 == 0]
    # print(datetime.now() - start) Тоже самое если бы тут была эта переменная 
    return l

l2 = two()

l1 = one     # Это значит что мы передаем функцию как обьект, а если нужен вызов то one()

```
### yield
(Построчно)

```
def summ_append(n):
    result = []
    while n != 0:
        result.append(n - 1)
        n -= 1
    return result
print(summ_append(5))
[4, 3, 2, 1, 0]
(Получаем очередной єлемент последовательности)
def summ_append2(n):
    while n != 0:
        yield n -1
        n -= 1
summ = summ_append2(4)
print(next(summ))
3
print(next(summ))
2
```

### map
(Элемент функционального програмирования)

```
def upper(string):
    return string.upper()

list_lower = ['one', 'two', 'three']

big_list = list(map(upper, list_lower))

print(big_list)
['ONE', 'TWO', 'THREE']

```
### Filter
```
def has_d(string):
    return 'd' in string.lower()

l1 = ['service', 'deployment', 'ingress']

l2 = list(filter(lambda string: 'd' in string.lower(), 1))
print(l1)


def has_d(string):
    return 'd' in string.lower()

l1 = ['service', 'deployment', 'ingress']

l2 = list(filter(lambda string: 'd' in string.lower(), l1))


print(l2)

```
