from sqlalchemy.orm import Session
from typing import Optional, Dict
from modules.abang_user.adapter.output.abang_user_model import AbangUser

class AbangUserRepository:
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def find_by_email(self, email: str) -> Optional[Dict]:
        db: Session = self.db_session_factory()
        try:
            # ✅ is_deleted 조건 제거
            user: Optional[AbangUser] = db.query(AbangUser).filter(
                AbangUser.email == email
            ).first()

            # ✅ .first()가 None 반환하면 그대로 None 리턴
            if not user:
                return None
            return {
                "abang_user_id": user.abang_user_id,
                "nickname": user.nickname,
                "email": user.email,
                "user_type": user.user_type,
                "created_dt": user.created_dt,
                "updated_dt": user.updated_dt
            }
        finally:
            db.close()

    def create_user(self, nickname: str | None, email: str, user_type: str) -> Dict:
        """
        ✅ 실제 사용하는 파라미터만 받도록 간소화
        """
        db: Session = self.db_session_factory()
        try:
            new_user = AbangUser(
                nickname=nickname,
                email=email,
                user_type=user_type
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "abang_user_id": new_user.abang_user_id,
                "nickname": new_user.nickname,
                "email": new_user.email,
                "user_type": new_user.user_type,
                "created_dt": new_user.created_dt,
                "updated_dt": new_user.updated_dt
            }
        finally:
            db.close()
