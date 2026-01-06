"""
Address to legal dong code repository implementation.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from modules.house_analysis.application.port.address_codec_port import AddressCodecPort
from modules.house_analysis.domain.exception import InvalidAddressError


class AddressCodecRepository(AddressCodecPort):
    """
    Convert address strings to legal dong code + bun/ji.
    """

    _legal_dong_cache: list[tuple[str, str]] | None = None

    def convert_to_legal_code(self, address: str) -> dict:
        """
        Convert address to legal dong code.

        Args:
            address: input address string

        Returns:
            dict: legal_code, address, bun, ji
        """
        normalized = (address or "").strip()
        if not normalized:
            raise InvalidAddressError("주소가 비어있습니다")

        bun, ji = _parse_bun_ji(normalized)
        base_address = re.sub(r"\s+\d+(?:-\d+)?$", "", normalized).strip()
        legal_name, legal_code = _lookup_legal_dong(base_address)

        return {
            "legal_code": legal_code,
            "address": legal_name,
            "bun": bun,
            "ji": ji,
        }


def _parse_bun_ji(address: str) -> tuple[str, str]:
    match = re.search(r"(\d+)(?:-(\d+))?$", address.strip())
    if not match:
        return "0000", "0000"
    bun = match.group(1).zfill(4)
    ji = match.group(2).zfill(4) if match.group(2) else "0000"
    return bun, ji


def _lookup_legal_dong(address: str) -> tuple[str, str]:
    legal_dongs = _load_legal_dong_data()
    best_name = ""
    best_code = ""

    for name, code in legal_dongs:
        if address.startswith(name) and len(name) > len(best_name):
            best_name = name
            best_code = code

    if not best_name:
        raise InvalidAddressError("법정동 코드를 찾을 수 없습니다")

    return best_name, best_code


def _load_legal_dong_data() -> list[tuple[str, str]]:
    if AddressCodecRepository._legal_dong_cache is not None:
        return AddressCodecRepository._legal_dong_cache

    csv_path = _find_legal_dong_csv()
    if csv_path is None:
        raise InvalidAddressError("legal_dong.csv 파일을 찾을 수 없습니다")

    legal_dongs: list[tuple[str, str]] = []
    with csv_path.open("r", encoding="cp949") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if not header:
            raise InvalidAddressError("legal_dong.csv 헤더가 없습니다")

        code_idx, name_idx, active_idx = _resolve_header_indexes(header)

        for row in reader:
            if not row:
                continue
            if active_idx is not None:
                active_value = row[active_idx].strip()
                if active_value != "존재":
                    continue
            try:
                code = row[code_idx].strip()
                name = row[name_idx].strip()
            except IndexError:
                continue
            if not code or not name:
                continue
            legal_dongs.append((name, code))

    AddressCodecRepository._legal_dong_cache = legal_dongs
    return legal_dongs


def _resolve_header_indexes(header: list[str]) -> tuple[int, int, int | None]:
    try:
        code_idx = header.index("법정동코드")
    except ValueError:
        code_idx = 0

    try:
        name_idx = header.index("법정동명")
    except ValueError:
        name_idx = 1

    try:
        active_idx = header.index("폐지여부")
    except ValueError:
        active_idx = None

    return code_idx, name_idx, active_idx


def _find_legal_dong_csv() -> Path | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "legal_dong.csv"
        if candidate.exists():
            return candidate
    return None
