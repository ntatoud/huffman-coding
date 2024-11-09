from io import IOBase
from typing import Literal

from src.compressor.bytes_utils import (
    get_source_data_bytes,
    get_data_filled_byte,
    NO_DATA_BYTE,
    ONE_REPEATED_DATA_BYTE,
    compressed_identifier,
    source_metadata_to_bytes,
)
from src.compressor.data_utils import statistics, binary_codes, huffman_tree


def compress(
    destination: IOBase,
    source: IOBase,
    serialization_nb_bytes: int = 4,
    serialization_order: Literal["big", "little"] = "big",
) -> None:
    compressed_data_bytes = compress_to_bytes(
        source, serialization_nb_bytes, serialization_order
    )

    destination.write(compressed_data_bytes)


def compress_to_bytes(
    source: IOBase,
    serialization_nb_bytes: int = 4,
    serialization_order: Literal["big", "little"] = "big",
) -> bytes:
    # Get source statistics
    source_bytes = source.read()
    stats = statistics(source_bytes)

    data_filled_byte = get_data_filled_byte(len(stats.counter.elements))
    compressed_data_id = compressed_identifier(data_filled_byte)

    if data_filled_byte == NO_DATA_BYTE:
        # No need for metadata since source data is empty
        return bytes(compressed_data_id)

    source_metadata = source_metadata_to_bytes(
        stats, serialization_nb_bytes, serialization_order
    )
    if data_filled_byte == ONE_REPEATED_DATA_BYTE:
        # We can build the original data just from metadata
        return bytes(compressed_data_id + source_metadata)

    source_binary_codes = binary_codes(huffman_tree(stats.counter))
    compressed_data_bytes = get_source_data_bytes(source_bytes, source_binary_codes)

    return bytes(compressed_data_id + source_metadata + compressed_data_bytes)
