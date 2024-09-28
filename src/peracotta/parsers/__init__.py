from .read_decode_dimms import parse_decode_dimms
from .read_dmidecode import parse_case, parse_motherboard, parse_psu
from .read_lscpu import parse_lscpu
from .read_lspci_and_glxinfo import parse_lspci_and_glxinfo
from .read_smartctl import parse_smartctl
from .read_udevadm import parse_udevadm
from .windows_parser import parse_win_chassis_specs, parse_win_cpu_specs, parse_win_motherboard_specs, parse_win_ram_specs
