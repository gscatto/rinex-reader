import io
from datetime import datetime

import numpy as np


class BDSNavRecordOrbitData:
    def __init__(self):
        # b-orbit 1
        self.A_DOT: float = 0.0
        self.C_rs: float = 0.0
        self.Delta_n0: float = 0.0
        self.M0: float = 0.0
        # b-orbit 2
        self.C_uc: float = 0.0
        self.e: float = 0.0
        self.C_us: float = 0.0
        self.sqrt_A: float = 0.0
        # b-orbit 3
        self.Toe: float = 0.0
        self.C_ic: float = 0.0
        self.OMEGA0: float = 0.0
        self.C_is: float = 0.0
        # b-orbit 4
        self.i0: float = 0.0
        self.C_rc: float = 0.0
        self.omega: float = 0.0
        self.OMEGA_DOT: float = 0.0
        # b-orbit 5
        self.IDOT: float = 0.0
        self.Delta_n0_dot: float = 0.0
        self.SatType: float = 0.0
        self.t_op: float = 0.0
        # b-orbit 6
        self.SISAI_oe: float = 0.0
        self.SISAI_ocb: float = 0.0
        self.SISAI_oc1: float = 0.0
        self.SISAI_oc2: float = 0.0
        # b-orbit 7
        self.SISMAI: float = 0.0
        self.health: float = 0.0
        self.B2b_integrity_flag: float = 0.0
        self.TGD_B2bI: float = 0.0
        # b-orbit 8
        self.t_tm: float = 0.0


class BDSCNAV3Record:
    gnss_symbol = 'C'
    nav_message_type = 'CNV3'
    block_size = 8  # amount of orbits

    epoch_line_format = np.dtype([
        ('SV', 'S8'),
        ('year', np.int32), ('month', np.int32), ('day', np.int32),
        ('hour', np.int32), ('min', np.int32), ('sec', np.int32),
        ('clock_bias', np.float64), ('clock_drift', np.float64), ('clock_drift_rate', np.float64),
    ])
    delimiter = (4, 4) + (3,) * 5 + (19,) * 3

    def __init__(self, sv: str):
        self.sv: str = sv
        self.timestamp: str = ""
        # epoch line
        self.clock_bias: float = 0.0
        self.clock_drift: float = 0.0
        self.clock_drift_rate: float = 0.0
        self.orbit_data = BDSNavRecordOrbitData()

    def read_epoch_line(self, line: str):
        epoch = np.genfromtxt(io.BytesIO(line.encode("ascii")),
                              delimiter=BDSCNAV3Record.delimiter,
                              dtype=BDSCNAV3Record.epoch_line_format,
                              autostrip=True
                              )
        self.timestamp = datetime(
            epoch["year"], epoch["month"], epoch["day"], epoch["hour"], epoch["min"], epoch["sec"]
        ).isoformat()
        self.clock_bias = epoch["clock_bias"] * 1
        self.clock_drift = epoch["clock_drift"] * 1
        self.clock_drift_rate = epoch["clock_drift_rate"] * 1

    def read_lines(self, lines: [str]):
        whole_block = "".join(lines)
        result = np.genfromtxt(io.BytesIO(whole_block.encode("ascii")),
                               delimiter=(19,) * len(self.orbit_data.__dict__),
                               dtype=np.dtype([(param, np.float64) for param in self.orbit_data.__dict__.keys()]),
                               autostrip=True
                               )
        for p in self.orbit_data.__dict__.keys():
            self.orbit_data.__dict__[p] = result[p] * 1  # convert to float
