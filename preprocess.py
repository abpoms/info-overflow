from tables import IsDescription, UInt32Col, UInt8Col
import tables
import numpy


class Tag(IsDescription):
    name = tables.StringCol()
    count = tables.UInt32Col()


class Vote(IsDescription):
    id = UInt32Col()
    post_id = UInt32Col()
    vote_type_id = UInt8Col()
    # creation_date =
    # user_id =
    # bounty_amount =


class User(IsDescription):
    pass


def load_tables():
    h5file = tables.openFile("tags.h5", mode="w", title="tags file")
