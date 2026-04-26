from dataclasses import dataclass
from thea_rpi.config import P_LOW_LIMIT, P_HIGH_LIMIT, T_LOW_LIMIT, T_HIGH_LIMIT, P_OFFSET, T_OFFSET


@dataclass
class HeadState:
    pan_angle: float = (P_LOW_LIMIT + P_HIGH_LIMIT) / 2 + P_OFFSET
    tilt_angle: float = (T_LOW_LIMIT + T_HIGH_LIMIT) / 2 + T_OFFSET

    def apply_delta(self, dpan: float, dtilt: float) -> None:
        self.pan_angle = max(P_LOW_LIMIT, min(P_HIGH_LIMIT, self.pan_angle + dpan))
        self.tilt_angle = max(T_LOW_LIMIT, min(T_HIGH_LIMIT, self.tilt_angle + dtilt))
