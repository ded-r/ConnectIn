from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from .base import Base

class PostLike(Base):  # ✅ Renamed from `NewsLike`
    __tablename__ = "post_likes"  # ✅ Changed from `news_likes`

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)  # ✅ Changed from `news_id`

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_post_like"),)
