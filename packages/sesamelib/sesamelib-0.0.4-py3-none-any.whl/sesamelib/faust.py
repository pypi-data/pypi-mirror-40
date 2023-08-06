import faust


class BaseDynamicMessage(faust.Record):
    x: float
    y: float
    mmsi: str
    tagblock_timestamp: int
    timestamp: int
    true_heading: float
    sog: float


class MutatedDynamicMessage(BaseDynamicMessage):
    ## (x-px)/Dt or None
    v0x: float = None
    ## (y-py)/Dt or None
    v0y: float = None
    ## closest zone
    zone_mrgid: str = None
    zone_distance: float = None

    @classmethod
    def fromBasicMessage(cls, msg):
        return cls(x=msg.x,
                   y=msg.y,
                   mmsi=msg.mmsi,
                   tagblock_timestamp=msg.tagblock_timestamp,
                   timestamp=msg.timestamp,
                   true_heading=msg.true_heading,
                   sog=msg.sog)
