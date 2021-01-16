import random

class Footballer:
    
    def __init__(self, name, speed = 40):
        self.name = name
        self.shots_taken = 0
        self.speed = speed
        self.strength = 25
        self.tackles_made = 0
    
    def __str__(self): 
        return self.name

    def shoot(self):
        print(self.name, "takes a shot!")
        self.shots_taken += 1
    
    def stamina(self,player):
        print(self.name, ("has ",random.choices(l, k=1)))
   
    def tackle(self,player):
        print(self.name, "takles",player.name)
        self.tackles_made += 1

    def injury(self,player):
        injury_duration = ["1 game", "2 games", "3 games", "7 games", "1 month", "The rest of the season"]       
        player_injury = random.choice(injury_duration)
        print("The player is injured for", player_injury)
    
    def player_decision(self,probability):
        player_said_yes = random.random() < probability
        if player_said_yes:
            print(f'{self.name} said ok.')
        else:
            print(f'{self.name} said nah i''m good.')
    
decide_list=["ok", "nah"]
name_list=["Bob", "Kevin", "Stuart", "Dave"]
l = [10,15,20,25,30,35,40,45,50]

def send_command():
    value_x = input("Please enter a player's name:\n")
    print(f'You choose {value_x} to send a order to.')
    value_y = input("Please enter a order to tell your player:\n")
    print(f'You said to {value_x} {value_y}.')
    footballer=Footballer(value_x)
    footballer.player_decision(0.7)

if __name__ == "__main__":
    footballers = []
    for n in name_list:
        footballers.append(Footballer(n))
    [print(str(f)) for f in footballers]
    send_command()

