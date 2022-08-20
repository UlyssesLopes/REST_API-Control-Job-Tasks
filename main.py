from typing_extensions import Required
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# model do db
class TarefaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    solicitante = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Tarefa(descricao = {TarefaModel.descricao}, solicitante = {TarefaModel.solicitante}, status = {TarefaModel.status})"    


# arguments POST formatados para API
tarefa_put_args = reqparse.RequestParser()
tarefa_put_args.add_argument('descricao', type=str, help="Descrição da Tarefa", required=True)
tarefa_put_args.add_argument('solicitante', type=str, help="Solicitante da Tarefa", required=True)
tarefa_put_args.add_argument('status', type=str, help="Status da Tarefa", required=True)

# arguments UPDATE formatados para API
tarefa_update_args = reqparse.RequestParser()
tarefa_update_args.add_argument('descricao', type=str, help="Descrição da Tarefa")
tarefa_update_args.add_argument('solicitante', type=str, help="Solicitante da Tarefa")
tarefa_update_args.add_argument('status', type=str, help="Status da Tarefa")


resource_fields = {
    'id': fields.Integer,
    'descricao': fields.String,
    'solicitante': fields.String,
    'status': fields.String
}


#  classe de tarefas com a chamada dos métodos
class Tarefa(Resource):
    @marshal_with(resource_fields)
    def get(self, tarefa_id):
        response = TarefaModel.query.filter_by(id=tarefa_id).first()
        if not response:
            abort(404, message='Tarefa não encontrada.')
        return response

    @marshal_with(resource_fields)
    def put(self, tarefa_id):
        args = tarefa_put_args.parse_args()
        response = TarefaModel.query.filter_by(id=tarefa_id).first()
        if response:
            abort(409, message='Este ID já existe.')

        tarefa = TarefaModel(id=tarefa_id,
                             descricao=args['descricao'],
                             solicitante=args['solicitante'],
                             status=args['status'])

        db.session.add(tarefa)
        db.session.commit()
        return tarefa, 201

    @marshal_with(resource_fields)
    def patch(self, tarefa_id):
        args = tarefa_update_args.parse_args()
        response = TarefaModel.query.filter_by(id=tarefa_id).first()
        if not response:
            abort(404, message='Tarefa não encontrada, não foi possível atualizar.')

        if args['descricao']:
            response.descricao = args['descricao']
        if args['solicitante']:
            response.solicitante = args['soliciante']
        if args['status']:
            response.status = args['status']

        db.session.commit()

        return response

    @marshal_with(resource_fields)
    def delete(self, tarefa_id):
        response = TarefaModel.query.filter_by(id=tarefa_id).first()
        if not response:
            abort(404, message='Tarefa não encontrada.')

        db.session.delete(response)
        db.session.commit()

        return response


class TodasTarefas(Resource):
    def get(self):
        response = TarefaModel.query.all()
        return response


#  url's e tipos de resource
api.add_resource(Tarefa, "/tarefa/<int:tarefa_id>")
api.add_resource(TodasTarefas, '/todas-tarefas')


# app rodando
if __name__ == "__main__":
    app.run(debug=True)