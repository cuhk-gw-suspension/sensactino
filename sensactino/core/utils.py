
def _checksum(arr):
    """Checksum, default last bytes is the checksum value.

    Parameters
    ----------
    arr : bytes or bytearray
        Bytes to be checksum, including the checksum byte.

    Returns
    -------
    : bool
        return True if checksum is correct.
    """
    checksum = arr[0]
    for byte in arr[1:]:
        checksum ^= byte

    if checksum == 0:
        return True
    else:
        return False
