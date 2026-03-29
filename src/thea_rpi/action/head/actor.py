from thea_rpi.action.base import BaseActor

class HeadActor(BaseActor):
    def act(self, command: str) -> None:
        print(command)


if __name__ == "__main__":
    pass
