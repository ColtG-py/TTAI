from dataclasses import dataclass

#todo define some better types for region, tunnel_entr, and tunnel_exit
@dataclass
class Street_Config():
    region: tuple
    tunnel_entr: tuple
    tunnel_exit: tuple

SILLY_STREET = Street_Config(region=(2200, 220, 750, 1000), tunnel_entr=(8, 46), tunnel_exit=(48, 50))