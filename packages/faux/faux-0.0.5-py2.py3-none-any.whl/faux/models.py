
# TODO: figure out how to incorporate a transient database that can store data.
#       see below for junkyard code


# column types
# ------------
class Field(object):
    
    def validate():
        return


class Text(Field):
    pass


class Enum(Field):
    pass


class Numeric(Field):
    pass


class Relationship(Field):
    pass



# models
# ------
DB = {}

class BaseModel(object):
    """
    """
    def __init__(self, ident, data=dict()):
        self.ident = ident
        self.uid = self.__class__.__name__ + ':' + ident
        self.exists = False
        if data is None:
            if self.uid in DB:
                self.data = DB[self.uid]
                self.exists = True
        else:
            self.data = data
        return

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.ident)

    @staticmethod
    def new(ident):
        """
        Mock data for new object using schema.
        """
        return

    @classmethod
    def create(self, ident, **kwargs):
        self = cls(ident, data=kwargs)
        if self.exists:
            raise AssertionError('{} already exists. Use update() for updates.'.format(self))
        DB[self.ident] = self
        self.exists = True
        return

    def update(self, **kwargs):
        if not self.exists:
            raise AssertionError('{} does not exist in database. Use create() to create.'.format(self))
        self.data.update(kwargs)
        return

    def drop():
        if not self.exists:
            raise AssertionError('{} does not exist in database. Will not drop.'.format(self))
        del DB[self.ident]
        return