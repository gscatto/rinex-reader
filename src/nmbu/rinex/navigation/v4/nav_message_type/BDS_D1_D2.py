import io
from datetime import datetime

import numpy as np


class BDSNavRecordOrbitData:
    def __init__(self):
        # b-orbit 1
        self.AODE: float = 0.0
        self.Crs: float = 0.0
        self.Delta_n: float = 0.0
        self.M0: float = 0.0
        # b-orbit 2
        self.Cuc: float = 0.0
        self.e: float = 0.0
        self.Cus: float = 0.0
        self.sqrt_A: float = 0.0
        # b-orbit 3
        self.Toe: float = 0.0
        self.Cic: float = 0.0
        self.OMEGA0: float = 0.0
        self.Cis: float = 0.0
        # b-orbit 4
        self.i0: float = 0.0
        self.Crc: float = 0.0
        self.omega: float = 0.0
        self.OMEGA_DOT: float = 0.0
        # b-orbit 5
        self.IDOT: float = 0.0
        self.spare1: float = 0.0
        self.BDT_Week_no: float = 0.0
        self.spare2: float = 0.0
        # b-orbit 6
        self.SV_accuracy: float = 0.0
        self.satH1: float = 0.0
        self.TGD1: float = 0.0
        self.TGD2: float = 0.0
        # b-orbit 7
        self.t_tm: float = 0.0
        self.AODC: float = 0.0


class BDSD1D2Record:
    gnss_symbol = 'C'
    nav_message_type = ('D1', 'D2')
    block_size = 7  # amount of orbits

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
                              delimiter=BDSD1D2Record.delimiter,
                              dtype=BDSD1D2Record.epoch_line_format,
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

        # TODO decide what to do with TGD and set self.orbit_data.TGD here. See e.g. GAL_INAV_FNAV.py
