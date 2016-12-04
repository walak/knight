from sqlalchemy import create_engine, Column, Integer, Numeric, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Engine = create_engine("mysql://dev:dev123@127.0.0.1/dev")
Session = sessionmaker(bind=Engine)
Base.metadata.create_all(Engine)


class StorableMoveHistory(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descriptor = Column(String(49), unique=True)
    knight_start_x = Column(Integer)
    knight_start_y = Column(Integer)
    moves_number = Column(Integer)

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
        self.session.add(entity)
        self.session.commit()

    def store_batch(self, move_histories):
        entities = [StorableMoveHistory.from_move_history(m) for m in move_histories]
        self.session.bulk_save_objects(entities)
        self.session.commit()
