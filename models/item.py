from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(500), nullable=False)
    inventory = db.Column(db.Text(500), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    def __init__(self, slug, description, inventory):
        self.slug = slug
        self.description = description
        self.inventory = inventory

    @classmethod
    def find_by_slug(cls, _slug: str):
        return cls.query.filter_by(slug=_slug).first()

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
