import faust


class PreviousMessage(faust.Record):
    x: float
    y: float
    mmsi: str
    timestamp: int

class DynamicMessage(faust.Record):
    x: float
    y: float
    mmsi: str
    tagblock_timestamp: int
    timestamp: int
    true_heading: float
    sog: float

    # the previous message
    previous: PreviousMessage = None

    v0x: float = None
    ## (y-py)/Dt or None
    v0y: float = None
    ## closest zone
    zone_mrgid: str = None
    zone_distance: float = None
