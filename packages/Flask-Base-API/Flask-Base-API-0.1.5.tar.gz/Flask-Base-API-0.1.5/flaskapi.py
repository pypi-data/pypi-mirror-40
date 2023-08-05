# -*- coding: utf-8 -*-
# @Time    : 18/12/26 上午11:40
# @Author  : Edward
# @Site    :
# @File    : flaskapi.py
# @Software: PyCharm Community Edition

from flask import Flask
from flask import jsonify
from flask import Blueprint


class API(Flask):
    blueprint_list = []

    # 创建蓝图
    def create_model(self, name):
        blueprint = Blueprint(name, __name__ + name)
        blueprint.logger = self.logger

        return blueprint

    def set_response_class(self, rc):
        self.response_class = rc

    def run(self, **kwargs):
        for blueprint in self.blueprint_list:
            blueprint['blueprint'].logger = self.logger
            self.register_blueprint(
                blueprint['blueprint'],
                url_prefix=blueprint['prefix']
            )

        super(API, self).run(**kwargs)

    def dispatch_request(self):
        resp = super(API, self).dispatch_request()
        if isinstance(resp, tuple):
            return jsonify({
                'data': resp[0],
                'code': resp[1]
            }), resp[1]
        else:
            return jsonify({
                'data': resp,
                'code': 200
            }), 200

    def regist(self, blueprint, url_prefix='', **options):
        if isinstance(url_prefix, str):
            url_prefix = url_prefix if url_prefix.startswith('/') else '/%s' % url_prefix
            super(API, self).register_blueprint(blueprint, url_prefix=url_prefix, **options)
        else:
            pass


if __name__ == '__main__':
    api = API('ttc')

    @api.route('/main')
    def index():
        return '首页'

    @api.route('/test')
    def error():
        api.logger.warning('200')
        return ['ERROR'], 200

    info = api.create_model('info')

    @info.route('/info')
    def get_info():
        info.logger.warning('201')
        return 'Show Info', 201

    api.regist(info, 'info')

    api.config['JSON_AS_ASCII'] = False
    api.run(debug=True)
