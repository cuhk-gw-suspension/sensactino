
def _checksum(arr):
    """Checksum, last bytes is the checksum value.

    Parameters
    ----------
    arr : bytes or bytearray
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
    arr : bytes or bytearray
        Bytes to be addsum.

    Returns
    -------
    addsum: bytes
        the checksum byte.
    """
    if not isinstance(arr, (bytes, bytearray)):
        raise TypeError("invalid type of arr:", type(arr))
    if len(arr) == 0:
        raise ValueError("empty array")
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


def _send_command(serial_device, cmd):
    """Handle the byte conversion and send the command to the serial device.

    Parameters
    ----------
    serial_device: pyserial's Serial object.
        The serial device to send command to.
    cmd : str-like
        command to be sent to the stepper.
    """
    if isinstance(cmd, str):
        cmd = cmd.encode("ascii")

    if not isinstance(cmd, (bytes, bytearray)):
        raise TypeError("cmd must be string-like object")
    serial_device.write(cmd)
