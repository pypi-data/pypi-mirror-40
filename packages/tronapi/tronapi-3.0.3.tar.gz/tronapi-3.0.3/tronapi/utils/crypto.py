# --------------------------------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from typing import Union

from eth_hash.auto import keccak as keccak_256
from eth_utils import to_bytes


def keccak(
    primitive: Union[bytes, int, bool] = None, hexstr: str = None, text: str = None
) -> bytes:
    return keccak_256(to_bytes(primitive, hexstr, text))
