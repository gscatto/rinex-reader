import numpy as np
import io


class GalileoNavRecordOrbitData:
    def __init__(self):
        # b-orbit 1
        self.iod_nav: float = 0.0
        self.crs: float = 0.0
        self.delta_n: float = 0.0
        self.m0: float = 0.0
        # b-orbit 2
        self.cuc: float = 0.0
        self.e: float = 0.0
        self.cus: float = 0.0
        self.sqrt_a: float = 0.0
        # b-orbit 3
        self.tte: float = 0.0
        self.cic: float = 0.0
        self.omega0: float = 0.0
        self.cis: float = 0.0
        # b-orbit 4
        self.i0: float = 0.0
        self.crc: float = 0.0
        self.omega: float = 0.0
        self.omega_dot: float = 0.0
        # b-orbit 5
        self.idot: float = 0.0
        self.data_sources: float = 0.0
        self.gal_week_no: float = 0.0
        self.spare1: float = 0.0
        # b-orbit 6
        self.sisa: float = 0.0
        self.sv_health: float = 0.0
        self.bgd_e5a: float = 0.0
        self.bgd_e5b: float = 0.0
        # b-orbit 7
        self.transmission_time: float = 0.0
        self.spare2: float = 0.0
        self.spare3: float = 0.0
        self.spare4: float = 0.0


class GalileoNavRecord:
    gnss_symbol = 'E'

    block_size = 7  # amount of orbits

    epoch_line_format = np.dtype([
        ('SV', 'S8'),
        ('year', np.int32), ('month', np.int32), ('day', np.int32),
        ('hour', np.int32), ('min', np.int32), ('sec', np.int32),
        ('clock_bias', np.float64), ('clock_drift', np.float64), ('clock_drift_rate', np.float64),
    ])
    delimiter = (4, 4) + (3,) * 5 + (19,) * 3

    def __init__(self, sv: str, timestamp: str):
        self.sv = sv
        self.timestamp = timestamp
        # epoch line
        self.clock_bias: float = 0.0
        self.clock_drift: float = 0.0
        self.clock_drift_rate: float = 0.0
        self.orbit_data = GalileoNavRecordOrbitData()

    def read_lines(self, lines: [str]):
        whole_block = "".join(lines)
        result = np.genfromtxt(io.BytesIO(whole_block.encode("ascii")),
                               delimiter=(19,) * len(self.orbit_data.__dict__),
                               dtype=np.dtype([(param, np.float64) for param in self.orbit_data.__dict__.keys()]),
                               autostrip=True
                               )
        for p in self.orbit_data.__dict__.keys():
            self.orbit_data.__dict__[p] = result[p] * 1  # convert to float
