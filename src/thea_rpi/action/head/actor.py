from thea_rpi.action.base import BaseActor
from thea_rpi.templates import HeadState
from thea_rpi.freenove.servo import Servo
from thea_rpi.config import P_CNL, T_CNL


class HeadActor(BaseActor):
    def start(self) -> None:
        self.hs = HeadState()
        self.pwm_servo = Servo()
        self._update()


    def _update(self):
        self.pwm_servo.set_servo_pwm(P_CNL, self.hs.pan_angle, 0)
        self.pwm_servo.set_servo_pwm(T_CNL, self.hs.tilt_angle, 0)

    
    def act(self, command: tuple) -> None:
        if len(command) == 0:
            return
        
        self.hs.apply_delta(command[0], command[1])
        self._update()


if __name__ == "__main__":
    pass
