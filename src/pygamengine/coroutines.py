from typing import Generator
import time
from .design_patterns import Singleton
from collections.abc import Callable

def generator(n):
    # initialize counter
    value = 0

    # loop until counter is less than n
    while value < n:

        print("Generator generates " + str(value))
        # produce the current value of the counter
        yield value

        # increment the counter
        value += 1
    
def unroll_generator(g):

    for x in g:
        print("Unrolling generator at value " + str(x))
        yield x

def execute_coroutine_code(n):
    g = unroll_generator(n)
    for x in g:
        print("execute coroutine")


def wait_for_seconds(n: int):
    current_time = time.perf_counter()
    end_time = current_time + n
    while current_time < end_time:
        yield current_time
        current_time = time.perf_counter()


'''You Need to implement execute() to work'''
class Coroutine:
    def __init__(self) -> None:
        self.__coroutine_system = CoroutineSystem()
        self.__coroutine_system+=self
        self.__generator = self.execute()
    
    def set_behaviour(self, function: Callable[..., None]):
        self.__coroutine_system = CoroutineSystem()
        self.execute = function
        self.__generator = function()
        self.__coroutine_system+=self

    # Generator
    def execute(self) -> Generator:
        pass

    def __call__(self):
        return self.__generator

class EndCoroutineSignal:
    pass

class CoroutineSystem(metaclass=Singleton):
    def __init__(self) -> None:
        self.__coroutines = list[Coroutine]()
        self.__end_coroutine = EndCoroutineSignal()

    def has_coroutines(self) -> bool:
        return len(self.__coroutines) > 0

    def __iadd__(self, c: Coroutine):
        self.__coroutines.append(c)
    
    def run_coroutines(self):
        if not self.has_coroutines():
            return
        ended_coroutines = []
        for coroutine in self.__coroutines:
            v = next(coroutine(), self.__end_coroutine)
            if v == self.__end_coroutine:
                ended_coroutines.append(coroutine)
        for ended in ended_coroutines:
            self.__coroutines.remove(ended)

class RunAfterSeconds(Coroutine):
    def __init__(self, seconds: int, callback: Callable[..., None], *args, **kwds) -> None:
        super().__init__()
        self.__seconds = seconds
        self.__callback = callback
        self.__args = args
        self.__kwds = kwds

    def execute(self):
        wait = WaitSeconds(self.__seconds)
        for k in wait():
            yield k
        self.__callback(*self.__args, **self.__kwds)    


class CountSeconds(Coroutine):
    def __init__(self, counter_name: str, seconds: int, step: int) -> None:
        super().__init__()
        self.counter_name = counter_name
        self.seconds = seconds
        self.step = step
    
    def execute(self):
        for i in range(0, self.seconds, self.step):
            print(f"{self.counter_name}: {i} seconds past")
            wait = WaitSeconds(self.step)
            for k in wait():
                yield k
            print(f"{self.counter_name}: {i} seconds past")
        print(f"End after {self.seconds}!")

class WaitSeconds:
    def __init__(self, seconds: float) -> None:
        self.__seconds = seconds

    def __call__(self):
        return self.execute()
    
    def execute(self):
        current_time = time.perf_counter()
        end_time = current_time + self.__seconds
        while current_time < end_time:
            yield current_time
            current_time = time.perf_counter()

if __name__ == "__main__":
    def p(ciao, mamma):
        print(f"{ciao}...{mamma}")
    system = CoroutineSystem()
    print("E vaffanculo")
    RunAfterSeconds(13, p, "cazzo", "mmerda")
    RunAfterSeconds(12, p, mamma="mamma", ciao="hello")
    CountSeconds("CLOCK", 15, 1)
    CountSeconds("timer1", 10, 2)
    CountSeconds("timer2", 15, 3)
    while system.has_coroutines():
        system.run_coroutines()

