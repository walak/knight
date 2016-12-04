import logging
from timeit import default_timer

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Engine = create_engine("mysql://dev:dev123@127.0.0.1/dev")
Session = sessionmaker(bind=Engine)
Base.metadata.create_all(Engine)
logging.basicConfig(level=logging.INFO)


class StorableMoveHistory(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descriptor = Column(String(49), unique=True)
    knight_start_x = Column(Integer)
    knight_start_y = Column(Integer)
    moves_number = Column(Integer)

    def __hash__(self):
        return 7 * hash(self.descriptor) + self.knight_start_x + (11 * self.knight_start_y) + 57 * self.moves_number

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    @staticmethod
    def from_move_history(move_history):
        descriptor = move_history.generate_sequence_description()

        return StorableMoveHistory(descriptor=descriptor,
                                   knight_start_x=move_history.knight.start.x,
                                   knight_start_y=move_history.knight.start.y,
                                   moves_number=len(descriptor))


class ResultStore:
    def __init__(self, session):
        self.session = session

    def store_one(self, move_history):
        entity = StorableMoveHistory.from_move_history(move_history)
        start = default_timer()
        self.session.add(entity)
        end = default_timer()
        logging.info("Stored %i entities in %.4f s" % (1, (end - start)))

        self.session.commit()

    def store_batch(self, move_histories):
        start = default_timer()
        entities = {StorableMoveHistory.from_move_history(m) for m in move_histories if
                    self.check_if_not_storable_exists(m)}

        self.session.bulk_save_objects(entities)
        self.session.commit()
        end = default_timer()
        logging.info("Stored %i entities in %.4f s" % (len(entities), (end - start)))

    def check_if_not_storable_exists(self, non_storable):
        storable = StorableMoveHistory.from_move_history(non_storable)
        return self.check_if_exist(storable)

    def check_if_exist(self, storable):
        query = self.session.query(StorableMoveHistory).filter(StorableMoveHistory.descriptor == storable.descriptor,
                                                               StorableMoveHistory.knight_start_x == storable.knight_start_x,
                                                               StorableMoveHistory.knight_start_y == storable.knight_start_y)
        result = query.first()
        return result is None

    def store_slow(self, move_histories):
        [self.store_one(m) for m in move_histories]
