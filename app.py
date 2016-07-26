
# -*- coding: utf-8 -*- 
from flask import Flask
from flask import render_template
from flask import request
import json
import random
import time

app = Flask(__name__)
game = {}
games = 0
config = ['狼人', '预言家', '女巫', '爱神' ,'守卫' , '白痴']

# 生成game唯一id
def generateUniqueId(games, game, condition):
	id = (str) (random.randint(0,999999))
	while (len(id) < 6):
		id = '0' + id
	# 最多1w场游戏同时
	if (games == 10000):
		return {'time': time.time(), 'id': 'error'}
	if not (id in game):
		game[id] = {'time': time.time(), 'id': id, 'condition': condition, 'intoNum': 1}
		games += 1
	else:
		pre = game[id]['time']
		now = time.time()
		# 一个房间仅存10分钟
		if abs(now - pre) > 600000:
			game[id] = {'time': time.time(), 'id': id, 'condition': condition, 'intoNum': 1}
		else:
			game[id] = generateUniqueId(games, game, condition)
	return game[id]

@app.route('/wolf')
def wolf():
	return render_template('index.html')

@app.route('/getGameStatus', methods=['GET', 'POST'])
def getGameStatus():
	gameId = request.form.get('gameId', 0)
	userId = request.form.get('userId', 0)
	# print game[gameId]
	if ((userId != 0) and (gameId != 0)):
		return json.dumps({'last' : game[gameId]['intoNum']});

@app.route('/Game')
def Game():
	method = request.args.get('method', 'none')
	if (method == 'into'):
		pass
	return render_template('game.html', method = method)

@app.route('/intoRoom', methods=['GET', 'POST'])
def intoGame():
	room = request.form.get('room', 'none')
	if (room == 'none'):
		'{error: "none"}'
	if not (room in game):
		return '{error: "no-room"}'
	targetGame = game[room]
	if (targetGame['intoNum'] == ((int)(targetGame['condition']['num']) + 1)):
		return '{error: "room-full"}'
	a = targetGame['intoNum']
	targetGame['intoNum'] = a + 1
	return json.dumps({'user': a + 1})

@app.route('/initGame', methods=['GET', 'POST'])
def initGaime():
	condition = {}
	condition['num'] = request.form.get('num', 0)
	condition['wolf'] = request.form.get('wolf', 0)
	condition['nvwu'] = request.form.get('nvwu',0)
	condition['yuyanjia'] = request.form.get('yuya', 0)
	condition['hunter'] = request.form.get('hunt', 0)
	condition['gud'] = request.form.get('gud',0)
	condition['foo'] = request.form.get('foo',0)
	condition['qiu'] = request.form.get('qiu',0)
	condition['man'] = request.form.get('man',0)
	gameid = generateUniqueId(games, game, condition)
	return json.dumps(gameid)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8520)