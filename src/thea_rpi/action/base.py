from abc import ABC, abstractmethod


class BaseActor(ABC):
    @abstractmethod
    def act(self, command: str) -> None:
        pass


if __name__ == "__main__":
    pass
