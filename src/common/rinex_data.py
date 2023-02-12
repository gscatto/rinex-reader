from datetime import datetime
from typing import Union

from navigation.v3.header import NavigationHeaderV3
from navigation.v3.navigation import NavigationV3
from navigation.v4.header import NavigationHeaderV4
from navigation.v4.navigation import NavigationV4
from observation.v3.header import ObservationHeaderV3
from observation.v3.observation import ObservationV3
from observation.v4.header import ObservationHeaderV4
from observation.v4.observation import ObservationV4


class RinexData:
    """
    Class that holds the result of reading Rinex file.
    Supports Observation and Navigation files in version 3 and 4.
    Provides API to access data.

    Examples
    --------

    >>> rinex = reader.read_rinex_file('path/to/rinex/file')

    Header can be one of: ObservationHeaderV3, NavigationHeaderV3, ObservationHeaderV4, NavigationHeaderV4.
    Depending on the actual type, fields stored in the header can vary. See also actual class documentation.

    >>> header = rinex.header
    >>> ver = header.version  # obtain file version
    >>> file_type = header.file_type  # obtain file type
    >>> antenna = header.antenna  # antenna. Applies to observation file header

    Data can be one of ObservationV3, ObservationV4, NavigationV3, NavigationV4.
    Contains list of satellites and corrections (if applicable).

    >>> data = rinex.data

    To access data for a given satellite, use following:

    >>> sv_c01 = rinex.data.satellites['C01']  # all time blocks for C01
    >>> sv_c01_C2I_val = rinex.data.satellites['C01']['2022-01-01T01:00:00']['C2I']['value']
    >>> sv_c01_C2I_lli = rinex.data.satellites['C01']['2022-01-01T01:00:00']['C2I']['lli']
    >>> sv_c01_C2I_ssi = rinex.data.satellites['C01']['2022-01-01T01:00:00']['C2I']['ssi']

    To access corrections (applicable for Navigation V4), use following:

    >>> corrections = rinex.data.corrections
    >>> sto_g_A0 = rinex.data.corrections['STO']['G']['2020-01-01T11:00:00'].A0
    >>> ion_c06_Alpha4 = rinex.data.corrections['ION']['C06']['2020-01-01T11:00:00'].Alpha4
    >>> eop_j01_Yp = rinex.data.corrections['EOP']['J01']['2020-01-01T11:00:00'].Yp
    """
    def __init__(self,
                 header: Union[ObservationHeaderV3, NavigationHeaderV3, ObservationHeaderV4, NavigationHeaderV4],
                 data: Union[ObservationV3, ObservationV4, NavigationV3, NavigationV4]):
        self.header = header
        self.data = data

    def __str__(self):
        return "Type: {t:s} (ver. {v:.2f}). Contains {s_no:d} satellites".format(
            t=self.header.file_type,
            v=self.header.version,
            s_no=len(self.data.satellites)
        )

    def find_closest_match(self, sv: str, timestamp: str):
        """
        Finds closest navigation data block for the given satellite and timestamp.

        Examples
        --------

        >>> rinex = reader.read_rinex_file('path/to/rinex/file')
        >>> result = rinex.find_closest_match(sv='E01', timestamp='2020-01-01T00:00:00')

        To query result, use dot-notation

        >>> crs = result.Crs
        >>> delta_n = result.Delta_n

        :param sv: name of the satellite, e.g. 'E05'
        :param timestamp: timestamp in ISO format, e.g. '2020-01-01T00:00:00'
        :return: block of navigation data (if found) or None
        """
        iso_format = '%Y-%m-%dT%H:%M:%S'
        if isinstance(self.data, NavigationV3) or isinstance(self.data, NavigationV4):
            if sv in self.data.satellites.keys():
                block = self.data.satellites[sv]
                timestamp = datetime.strptime(timestamp, iso_format)
                result = min(map(lambda x: datetime.strptime(x, iso_format), block.keys()),
                             key=lambda x: abs(x - timestamp))
                return self.data.satellites[sv][result.isoformat()]
            else:
                return None
        else:
            return None
