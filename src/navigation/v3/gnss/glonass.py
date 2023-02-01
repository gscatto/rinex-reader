import numpy as np
import io


class GLONASSNavRecordOrbitData:
    def __init__(self):
        # b-orbit 1
        self.sv_pos_X: float = 0.0
        self.velocity_X: float = 0.0
        self.acceleration_X: float = 0.0
        self.health: float = 0.0
        # b-orbit 2
        self.sv_pos_Y: float = 0.0
        self.velocity_Y: float = 0.0
        self.acceleration_Y: float = 0.0
        self.frequency_no: float = 0.0
        # b-orbit 3
        self.sv_pos_Z: float = 0.0
        self.velocity_Z: float = 0.0
        self.acceleration_Z: float = 0.0
        self.information_age: float = 0.0
        # b-orbit 4
        self.status_flags: float = 0.0
        self.delta_tau: float = 0.0
        self.urai: float = 0.0
        self.health_flags: float = 0.0


class GLONASSNavRecord:
    gnss_symbol = 'R'

    block_size = 4  # amount of orbits

    epoch_line_format = np.dtype([
        ('SV', 'S8'),
        ('year', np.int32), ('month', np.int32), ('day', np.int32),
        ('hour', np.int32), ('min', np.int32), ('sec', np.int32),
        ('clock_bias', np.float64), ('relative_frequency_bias', np.float64), ('msg_frame_time', np.float64),
    ])
    delimiter = (4, 4) + (3,) * 5 + (19,) * 3

    def __init__(self, sv: str, timestamp: str):
        self.sv = sv
        self.timestamp = timestamp
        # epoch line
        self.clock_bias: float = 0.0
        self.relative_frequency_bias: float = 0.0
        self.msg_frame_time: float = 0.0
        self.orbit_data = GLONASSNavRecordOrbitData()

    def read_lines(self, lines: [str]):
        whole_block = "".join(lines)
        result = np.genfromtxt(io.BytesIO(whole_block.encode("ascii")),
                               delimiter=(19,) * len(self.orbit_data.__dict__),
                               dtype=np.dtype([(param, np.float64) for param in self.orbit_data.__dict__.keys()]),
                               autostrip=True
                               )
        for p in self.orbit_data.__dict__.keys():
            self.orbit_data.__dict__[p] = result[p] * 1  # convert to float
