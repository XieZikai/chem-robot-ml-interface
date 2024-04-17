from apps import db


class Hansen(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Hansen'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.String(64), unique=True)
    sample_number = db.Column(db.Integer)
    ongoing = db.Column(db.Integer)
    comments = db.Column(db.String(64))


class HansenImage(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Hansen-image'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    time = db.Column(db.String(64), unique=True)


class HansenSamples(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Hansen-samples'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    sample_name = db.Column(db.String(64))
    sample_row = db.Column(db.Integer)
    sample_col = db.Column(db.Integer)
    shake = db.Column(db.Integer)


class Particle(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Particle'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.String(64), unique=True)
    sample_number = db.Column(db.Integer)
    ongoing = db.Column(db.Integer)
    comments = db.Column(db.String(64))


class ParticleImage(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Particle-image'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    time = db.Column(db.String(64), unique=True)


class ParticleSamples(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Particle-samples'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    sample_name = db.Column(db.String(64))
    sample_row = db.Column(db.Integer)
    sample_col = db.Column(db.Integer)
    shake = db.Column(db.Integer)


class Solubility(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Solubility'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.String(64), unique=True)
    sample_number = db.Column(db.Integer)
    ongoing = db.Column(db.Integer)
    comments = db.Column(db.String(64))


class SolubilityImage(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Solubility-image'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    time = db.Column(db.String(64), unique=True)


class SolubilitySamples(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Solubility-samples'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    father_id = db.Column(db.Integer)
    sample_name = db.Column(db.String(64))
    sample_row = db.Column(db.Integer)
    sample_col = db.Column(db.Integer)
    shake = db.Column(db.Integer)


class RackAvailability(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'Rack-availability'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    row = db.Column(db.Integer)
    col = db.Column(db.Integer)
    available = db.Column(db.Integer)


class AllTasks(db.Model):
    __bind_key__ = 'history_db'
    __tablename__ = 'AllTasks'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.String(64), unique=True)
    sample_number = db.Column(db.Integer)
    ongoing = db.Column(db.Integer)
    comments = db.Column(db.String(64))
