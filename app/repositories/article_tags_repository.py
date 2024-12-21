from typing import List

from sqlalchemy.orm import Session

from app.models.article_tag import article_tag


class ArticleTagsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, article_tags: List[dict]):

            self.db.execute(article_tag.insert(), article_tags)
            self.db.commit()
            print(f"Successfully added {len(article_tags)} tags.")

    def delete(self, article_id, tag_ids: List[int]):

            self.db.execute(article_tag.delete().where(article_tag.c.article_id == article_id).where(article_tag.c.tag_id.in_(tag_ids)))
            self.db.commit()
            print(f"Successfully deleted {len(tag_ids)} tags.")
