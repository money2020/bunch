from app import app, db, models

from flask import jsonify, request

@app.route('/')
def index():
    return 'ok'


@app.route('/groups', methods=['GET', 'POST'])
@app.route('/groups/<group_id>', methods=['GET'])
def groups(group_id=None):
    return _crud('group', models.Group, group_id)


@app.route('/peers', methods=['GET', 'POST'])
@app.route('/peers/<peer_id>', methods=['GET'])
def peers(peer_id=None):
    return _crud('peer', models.Peer, peer_id)


def _crud(name, model, obj_id):
    return_message = None

    if request.method == 'POST':
        obj = model.fromdict(request.get_json())

        db.session.add(obj)
        db.session.commit()

        obj_id = obj.id

    if obj_id is not None:
        obj = model.query.get(int(obj_id))
        if obj is not None:
            return jsonify(obj.serialize())
        else:
            return_message = '%s does not exist' % (name)

    else:
        objs = model.query.all()
        return jsonify({name: [o.serialize() for o in objs]})

    return jsonify({'error': return_message or 'unknown error'})