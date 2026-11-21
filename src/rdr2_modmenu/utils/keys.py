"""Key name -> virtual key code mapping shared by overlay + script hook."""

VK = {
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73,
    "F5": 0x74, "F6": 0x75, "F7": 0x76, "F8": 0x77,
    "INSERT": 0x2D, "DELETE": 0x2E, "HOME": 0x24, "END": 0x23,
}


def resolve(key: str) -> int:
    key = key.upper()
    if key in VK:
        return VK[key]
    if len(key) == 1:
        return ord(key)
    raise KeyError(f"unknown key: {key}")