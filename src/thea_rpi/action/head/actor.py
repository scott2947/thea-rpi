from thea_rpi.action.base import BaseActor
from thea_rpi.freenove.servo import Servo
from thea_rpi.config import X_CNL, Y_CNL, X_OFFSET, Y_OFFSET
from thea_rpi.config import X_LOW_LIMIT, X_HIGH_LIMIT, Y_LOW_LIMIT, Y_HIGH_LIMIT


class HeadActor(BaseActor):
    def start(self) -> None:
        self.x = 90 + X_OFFSET
        self.y = 90 + Y_OFFSET
        self.pwm_servo = Servo()
        self._update()


    def _update(self):
        self.pwm_servo.set_servo_pwm(X_CNL, self.x, 0)
        self.pwm_servo.set_servo_pwm(Y_CNL, self.y, 0)

    
    def act(self, command: dict) -> None:
        if len(command) == 0:
            return
        
        p_x, p_y = command["x"], command["y"]

        new_x, new_y = self.x - p_x, self.y - p_y

        if new_x >= X_LOW_LIMIT and new_x <= X_HIGH_LIMIT and new_y >= Y_LOW_LIMIT and new_y <= Y_HIGH_LIMIT:
            self.x, self.y = new_x, new_y
            self._update()

        print(command, self.x, self.y)


if __name__ == "__main__":
    pass
