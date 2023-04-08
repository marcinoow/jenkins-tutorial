import time
from tasks import add, mull, sub


def main():
    add_task = add.delay(1, 2)
    print(f'Is {add_task.name} ready? ', end='')
    print(add_task.ready())
    print('Waiting...')
    time.sleep(1)
    print(f'Is {add_task.name} ready? ', end='')
    print(add_task.ready())
    print(add_task.result)

    mull_task = mull.delay(2, 2)
    time.sleep(1)
    print(mull_task.result)

    sub_task = sub.delay(2, 1)
    time.sleep(4)
    print(sub_task.ready())
    print(sub_task.result)


if __name__ == '__main__':
    main()
