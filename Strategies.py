

def Attack(player_platoon, enemy_platoon):
	#print('in Attack')
	if player_platoon.total_health >= enemy_platoon.total_health:
		while enemy_platoon.total_health > 0:
			p=player_platoon.platoon_members[0]
			e=enemy_platoon.platoon_members[0]
			p.health-=1
			e.health-=1
			player_platoon.update()
			enemy_platoon.update()
			# print(len(player_platoon.platoon_members),len(player_platoon.platoon_members))
			# print(player_platoon.total_health, enemy_platoon.total_health)
			# print(player_platoon.platoon_members[0].health,enemy_platoon.platoon_members[0].health)
	elif player_platoon.total_health < enemy_platoon.total_health:
		while player_platoon.total_health > 0:
			p=player_platoon.platoon_members[0]
			e=enemy_platoon.platoon_members[0]
			p.health-=1
			e.health-=1
			player_platoon.update()
			enemy_platoon.update()
