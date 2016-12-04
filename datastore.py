import logging

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import get_database_config_from_file, SimpleTimer

Base = declarative_base()
Engine = create_engine(get_database_config_from_file())
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


LOG = logging.getLogger("ResultStore")
LOG.setLevel(logging.INFO)


class ResultStore:
    def __init__(self, session):
        self.session = session

    def store_one(self, move_history):
        timer = SimpleTimer.create_and_start()

        entity = StorableMoveHistory.from_move_history(move_history)
        self.session.add(entity)
        self.session.commit()

        LOG.info("Stored %i entities in %.4f s" % (1, timer.get_time()))

    def store_batch(self, move_histories):
        filtered_results = self.filter_and_convert_data(move_histories)

        timer = SimpleTimer.create_and_start()
        self.session.bulk_save_objects(filtered_results)
        self.session.commit()
        logging.info("Stored %i entities in %.4f s" % (len(filtered_results), timer.get_time()))
        return len(filtered_results)

    def filter_and_convert_data(self, move_histories):
        timer = SimpleTimer.create_and_start()
        filtered_elements = {StorableMoveHistory.from_move_history(m) for m in move_histories if
                             self.check_if_not_storable_exists(m)}

        initial_size = len(move_histories)
        final_size = len(filtered_elements)
        difference = initial_size - final_size
        time = timer.get_time()
        LOG.info("Filtered %i results in %.4f to eliminate duplicates. Uniques kept: %i Duplicates removed: %i" % (
            initial_size, time, final_size, difference))
        return filtered_elements

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
