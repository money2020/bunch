from app import db


peers_groups = db.Table('peers_to_groups',
    db.Column('peer_id', db.Integer, db.ForeignKey('peers.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

vendors_groups = db.Table('vendors_to_groups',
    db.Column('vendor_id', db.Integer, db.ForeignKey('vendors.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

class SuperModel:

    @classmethod
    def fromdict(cls, d):
        allowed_keys = [v for v in dir(cls) if not callable(getattr(cls, v)) and not v.startswith('_')]
        df = {k : v for k, v in d.iteritems() if k in allowed_keys}

        # ugh...
        if 'peers' in df:
            df['peers'] = [x for x in Peer.query.filter(Peer.id.in_(df['peers'])).all()]

        # UGH...
        if 'vendor' in df:
            df['vendor'] = [v for v in Vendor.query.filter(Vendor.id.in_(df['vendor'])).all()]

        return cls(**df)


class Peer(db.Model, SuperModel):

    __tablename__ = 'peers'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(64))
    owner_name = db.Column(db.String(64))
    image = db.Column(db.String(64))
    paid = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id': self.id,
            'businessName': self.business_name,
            'ownerName': self.owner_name,
            'image': self.image,
            'paid': self.paid
        }

    def __repr__(self):
        return '<Peer "%r">' % (self.id)


class Vendor(db.Model, SuperModel):

    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(64))
    name = db.Column(db.String(64))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image
        }

    def __repr__(self):
        return '<Vendor "%r">' % (self.id)


class Group(db.Model, SuperModel):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    peers = db.relationship('Peer', secondary=peers_groups)
    vendor = db.relationship('Vendor', secondary=vendors_groups)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'peers': [p.serialize() for p in self.peers],
            'vendor': [v.serialize() for v in self.vendor]
        }

    def __repr__(self):
        return '<Group "%r">' % (self.name)