
def _checksum(arr):
    """Checksum, last bytes is the checksum value.

    Parameters
    ----------
    arr : bytes, bytearray, or list of int.
        Bytes to be checksum, including the checksum byte.

    Returns
    -------
    bool
        return True if checksum is correct.
    """
    checksum = _addsum(arr)

    if checksum == 0:
        return True
    else:
        return False

def _addsum(arr):
    """Compute the XOR checksum value.

    Parameters
    ----------
    arr : bytes, bytearray, or list of int
        Bytes to be addsum.

    Returns
    -------
    addsum: int
        the checksum byte as integer.
    """
    if not isinstance(arr, (bytes, bytearray, list)):
        raise TypeError("invalid type of arr:", type(arr))
    if len(arr) == 0:
        raise ValueError("empty array")
    arr = list(arr)
    addsum = arr[0]
    for byte in arr[1:]:
        addsum ^= byte
    return addsum

def ceildiv(a, b):
    return -(-a // b)

def _int2bytes(x, byteorder="big", signed=True):
    """A wrapper around the to_bytes function in native Python.
    It returns the integer value in minimal bytes.

    Parameters
    ----------
    x: int
        The integer to convert to bytes.
    byteorder: str, optional
        'big' or 'little', see python docs on to_bytes.
    signed: bool, optional
        whether x is signed or not.

    Returns
    -------
    y : bytes
        the integer value in minimal bytes.
    """
    y = x.to_bytes(ceildiv(x.bit_length(), 8),
                   byteorder=byteorder,
                   signed=signed)
    return y


def _send_command(serial_device, cmd, value=0, signed=True):
    """Handle the byte conversion and send the command to the serial device.
    Protocol: | header | cmd | value | checksum | footer |

    Parameters
    ----------
    serial_device : pyserial's Serial object.
        The serial device to send command to.
    cmd : str
        a character to be sent to the arduino for interpretation.
    value : int
        value to write in the data session, maxmimum 4 bytes.
        Default to 0.
    signed : bool, optional
        Select whether the bytes converted from value is signed or not.
        Default is True.
    """
    if not isinstance(cmd, str):
        raise TypeError("cmd must be string-like object")
    if len(cmd) > 1:
        raise ValueError("cmd must be a single character")
    if value.bit_length() >= 32:
        raise ValueError("value is too large to be sent over")

    msg = cmd.encode("ascii")
    msg += value.to_bytes(4, byteorder="little", signed=signed)
    msg += bytes([_addsum(msg)])
    msg = b'\t'+ msg + b'\n'
    serial_device.write(msg)

