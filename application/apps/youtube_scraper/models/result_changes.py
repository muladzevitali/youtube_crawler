from datetime import datetime

from apps import database


class ScraperResultChange(database.Model):
    __tablename__ = 'scraper_result_changes'

    id = database.Column(database.Integer, database.Sequence('result_change_id_sel'), primary_key=True)
    result_id = database.Column(database.Integer, database.ForeignKey('scraper_results.id'))
    field = database.Column(database.String(100))
    old_value = database.Column(database.String(1000))
    new_value = database.Column(database.String(1000))
    update_date = database.Column(database.DateTime, default=datetime.now())

    def __repr__(self):
        return f'Field {self.field} changed from {self.old_value} to {self.new_value}'
