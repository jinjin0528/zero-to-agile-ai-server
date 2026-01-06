"""
ê±´ì¶•ë¬¼ë???API Repository êµ¬í˜„ì²?
"""
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os as os_module
from dotenv import load_dotenv
from modules.house_analysis.application.port.building_ledger_port import BuildingLedgerPort
from modules.house_analysis.domain.exception import BuildingInfoNotFoundError

load_dotenv()


class BuildingLedgerRepository(BuildingLedgerPort):
    """
    ê±´ì¶•ë¬¼ë????•ë³´ë¥?ì¡°íšŒ?˜ëŠ” Repository
    ê³µê³µ?°ì´?°í¬??ê±´ì¶•ë¬¼ë???API ?¬ìš©
    """

    def __init__(self):
        """Initialize the Building Ledger API client."""
        self.api_key = os_module.getenv("PUBLIC_DATA_API_KEY", "")
        self.endpoint = "https://apis.data.go.kr/1613000/BldRgstHubService/getBrTitleInfo"
        self.timeout = 10  # seconds

    def fetch_building_info(self, legal_code: str, bun: str, ji: str) -> dict:
        """
        ë²•ì •??ì½”ë“œë¡?ê±´ì¶•ë¬??•ë³´ ì¡°íšŒ

        Args:
            legal_code: ë²•ì •??ì½”ë“œ (10?ë¦¬, ?? 1168010100)
                       ??5?ë¦¬: ?œêµ°êµ¬ì½”?? ??5?ë¦¬: ë²•ì •?™ì½”??            bun: ë²?(4?ë¦¬)
            ji: ì§€ (4?ë¦¬)

        Returns:
            dict: ê±´ì¶•ë¬??•ë³´ (is_violation, has_seismic_design, building_age)

        Raises:
            BuildingInfoNotFoundError: ê±´ì¶•ë¬??•ë³´ë¥?ì°¾ì„ ???†ëŠ” ê²½ìš°
        """
        # ë²•ì •??ì½”ë“œë¥??œêµ°êµ¬ì½”?œì? ë²•ì •?™ì½”?œë¡œ ë¶„ë¦¬
        if len(legal_code) != 10:
            raise ValueError(f"ë²•ì •??ì½”ë“œ??10?ë¦¬?¬ì•¼ ?©ë‹ˆ?? {legal_code}")

        sigungu_cd = legal_code[:5]  # ??5?ë¦¬
        bjdong_cd = legal_code[5:]   # ??5?ë¦¬

        # ë²?ì§€ ê°’ì? 4?ë¦¬ë¡??¨ë”©
        bun = str(bun).zfill(4)
        ji = str(ji).zfill(4)

        # API ?¸ì¶œ
        try:
            params = {
                'serviceKey': self.api_key,
                'sigunguCd': sigungu_cd,
                'bjdongCd': bjdong_cd,
                'bun': bun,
                'ji': ji,
                'numOfRows': 1,
                'pageNo': 1
            }

            response = requests.get(
                self.endpoint,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            # XML ?Œì‹±
            return self._parse_xml_response(response.text)

        except requests.Timeout:
            raise BuildingInfoNotFoundError(f"API ?”ì²­ ?œê°„ ì´ˆê³¼: {legal_code}")
        except requests.RequestException as e:
            raise BuildingInfoNotFoundError(f"API ?”ì²­ ?¤íŒ¨: {str(e)}")

    def _parse_xml_response(self, xml_text: str) -> dict:
        """
        XML ?‘ë‹µ???Œì‹±?˜ì—¬ ?„ìš”???•ë³´ ì¶”ì¶œ

        Args:
            xml_text: XML ?‘ë‹µ ?ìŠ¤??

        Returns:
            dict: ê±´ì¶•ë¬??•ë³´
        """
        try:
            root = ET.fromstring(xml_text)

            # ?ëŸ¬ ì²´í¬
            header = root.find('header')
            if header is not None:
                result_code = header.findtext('resultCode', '')
                result_msg = header.findtext('resultMsg', '')

                if result_code != '00':
                    raise BuildingInfoNotFoundError(
                        f"API ?ëŸ¬ (ì½”ë“œ: {result_code}, ë©”ì‹œì§€: {result_msg})"
                    )

            # ê±´ì¶•ë¬??°ì´??ì¶”ì¶œ
            body = root.find('body')
            if body is None:
                raise BuildingInfoNotFoundError("?‘ë‹µ??bodyê°€ ?†ìŠµ?ˆë‹¤")

            items = body.find('items')
            if items is None:
                raise BuildingInfoNotFoundError("?‘ë‹µ??itemsê°€ ?†ìŠµ?ˆë‹¤")

            item = items.find('item')
            if item is None:
                raise BuildingInfoNotFoundError("ê±´ì¶•ë¬??°ì´?°ë? ì°¾ì„ ???†ìŠµ?ˆë‹¤")

            # ?„ìš”???„ë“œ ì¶”ì¶œ ë°?ë³€??            # ?„ë°˜ ê±´ì¶•ë¬??¬ë? (vlRat: ?„ë°˜ê±´ì¶•ë¬??¬ë?)
            vl_rat_yn = item.findtext('vlRatEstbYn', 'N')  # ?„ë°˜ê±´ì¶•ë¬¼ì—¬ë¶€
            is_violation = vl_rat_yn.upper() == 'Y'

            # ?´ì§„ ?¤ê³„ ?¬ë? (qltyGradeYn: ?ˆì§ˆ?±ê¸‰ ?¬ë?, etcRoof: ê¸°í? ì§€ë¶???
            # ?¤ì œë¡œëŠ” useAprDay(?¬ìš©?¹ì¸??ë¡??´ì§„?¤ê³„ ?˜ë¬´???œì  ê¸°ì? ?ë‹¨
            use_apr_day = item.findtext('useAprDay', '')  # ?¬ìš©?¹ì¸??(YYYYMMDD)

            # 1988???´í›„ ê±´ë¬¼?€ ?´ì§„?¤ê³„ ?˜ë¬´??(ê°„ë‹¨??ê¸°ì?)
            has_seismic_design = False
            if use_apr_day and len(use_apr_day) >= 4:
                year = int(use_apr_day[:4])
                has_seismic_design = year >= 1988

            # ê±´ë¬¼ ?°ë ¹ ê³„ì‚°
            building_age = 0
            if use_apr_day and len(use_apr_day) >= 4:
                year = int(use_apr_day[:4])
                current_year = datetime.now().year
                building_age = current_year - year

            # ì£¼ìš©?„ì½”?œëª…
            main_use = item.findtext('mainPurpsCdNm', '').strip()

            return {
                "is_violation": is_violation,
                "has_seismic_design": has_seismic_design,
                "building_age": building_age,
                "main_use": main_use
            }

        except ET.ParseError as e:
            raise BuildingInfoNotFoundError(f"XML ?Œì‹± ?¤íŒ¨: {str(e)}")