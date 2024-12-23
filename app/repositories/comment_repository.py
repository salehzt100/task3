from sqlalchemy.orm import Session

from app.models import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_comments(self, article_id):
        pass
    def get_comment_by_id(self, comment_id):

        return self.db.query(Comment).where(Comment.id == comment_id).first()

    def insert(self, comment: Comment):
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: Comment):
        self.db.commit()
        self.db.refresh(comment)

    def delete(self, comment):
        self.db.delete(comment)
        self.db.commit()
