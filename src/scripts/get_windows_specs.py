import os

POWERSHELL = r"powershell -Command"


def get_win_cpu_specs() -> str:
    command = 'Get-CimInstance -ClassName Win32_Processor | Select-Object -ExcludeProperty "CIM*" | ConvertTo-Json'
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_ram_specs() -> str:
    command = "Get-WmiObject Win32_PhysicalMemory | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_motherboard_specs() -> str:
    command = "Get-WmiObject Win32_BaseBoard | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_chassis_specs() -> str:
    command = "Get-WmiObject Win32_SystemEnclosure | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_disks_specs() -> str:
    command = "Get-Disk | Select * | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_pnp_specs() -> str:
    command = "Get-PnpDevice | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_network_specs() -> str:
    command = "Get-NetAdapter | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def get_win_graphics_card_specs() -> str:
    command = "Get-WmiObject Win32_VideoController | ConvertTo-Json"
    data = os.popen(f'{POWERSHELL} "& {command}"').read()
    return data


def generate_win_files():
    os.makedirs("tmp", exist_ok=True)
    with open("tmp/lscpu.win", "w") as file:
        file.write(f"{get_win_cpu_specs()}")
        file.flush()
        file.close()
    with open("tmp/dimms.win", "w") as file:
        file.write(f"{get_win_ram_specs()}")
        file.flush()
        file.close()
    with open("tmp/baseboard.win", "w") as file:
        file.write(f"{get_win_motherboard_specs()}")
        file.flush()
        file.close()
    with open("tmp/chassis.win", "w") as file:
        file.write(f"{get_win_chassis_specs()}")
        file.flush()
        file.close()
    with open("tmp/disks.win", "w") as file:
        file.write(f"{get_win_disks_specs()}")
        file.flush()
        file.close()
    with open("tmp/lspci.win", "w") as file:
        file.write(f"{get_win_pnp_specs()}")
        file.flush()
        file.close()
    with open("tmp/net.win", "w") as file:
        file.write(f"{get_win_pnp_specs()}")
        file.flush()
        file.close()
    with open("tmp/graphics.win", "w") as file:
        file.write(f"{get_win_pnp_specs()}")
        file.flush()
        file.close()


def main():
    generate_win_files()


if __name__ == "__main__":
    main()
