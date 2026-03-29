from abc import ABC, abstractmethod


class BaseActor(ABC):
    @abstractmethod
    def act(self, command: dict) -> None:
        pass


if __name__ == "__main__":
    pass
