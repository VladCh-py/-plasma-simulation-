import pygame
from math import *
from random import *
from statistics import mean
import matplotlib.pyplot as plt
ax = plt.subplots()[1]
import numpy as np
import keyboard
'''
Данная программа позволяет запускать расчет движения заряженной частице в "Плазме" заряженных частиц, при этом симуляция отображается сразу после старта.
"Плазма" представляет собой набор разноименно заряженных частиц с одинаковыми массами. Программа позволяет исследовать взаимодействие "главной" частицы, обладающей бОльшую
массу и заряд, чем обычные частицы, со "стандартными" частицами. При разных значениях возможно наблюдать пролет ""главной" частицы через "плазму", когда за ней образуется
"хвост" из противоположно заряженных частиц или когда исследуемую частицу окружают противоположно заряженные частицы с мЕньшей массой(данный результат, теоретически,
можно интерпретировать как образование радиуса Дебая-Хюккеля).

'''
pygame.init()
pygame.display.set_caption("PLASMA simulation")

L=1000#длина стороны окна
width0=L*1.5
height0=L
width=width0
height=height0

win = pygame.display.set_mode((width0, height0))

# Инициализация цвета
color = (255, 255, 255)
r1=5


# для "Дебаевского радиуса"
################################################################################################################################################################################################


# nn=300
# m1=1
# r1=5
# Charge=10 #заряд
# positive_percent=50
# main_Vx=10
# main_Vy=0
# main_charge=Charge*20
# main_m=m1*1000
# main_r= 1.5*r1


# для "пролета"
################################################################################################################################################################################################

nn=300
m1=1
r1=5
Charge=10 #заряд
positive_percent=50
main_Vx=45
main_Vy=0
main_charge=Charge*50
main_m=m1*1000
main_r=1.5*r1

################################################################################################################################################################################################

main_X=int(width/11)
main_Y=int(height/2)


# Раскомментировать, если необходимо вводить парметры вручную

# print("Введите параметры: ")
# print("(Например используйте: N=300, m=1, q=10, Vx=10, M=1000, Q=200, 50; ИЛИ N=300, m=1, q=10, Vx=45, M=1000, Q=500, 50)")
# print("")
# print("Количество частиц: N= ")
# nn=int(input())
# print("Масса: m= ")
# m1=float(input())
# print("Заряд: q= ")
# Charge=float(input())
# print("Скорость пробной частицы: Vx=")
# main_Vx=float(input())
# print("Масса пробной частицы: M=")
# main_m=float(input())
# print("Заряд пробной частицы: Q= ")
# main_charge=float(input())
# print("Процент положительно заряженных: ")
# positive_percent=float(input())

k=9



MAX_iterations=10000#максимальное число итераций

particles=[]
ACCELERATION=0
sqrt_dist_sum=0
running=True
dt=0.1  #Рассматриваемый промежуток времени
iterations=0
spawn=True
def free_zone_check(N):
    sqr_distance_min=width**2+height**2
    for i in range(0, nn-1):
        if particles[i].charge*particles[N].x>0:
            r_x = particles[N].x - particles[i].x
            r_y = particles[N].y - particles[i].y
            sqr_distance = r_x**2 + r_y**2
            sqr_distance_min=min(sqr_distance, sqr_distance_min)
    return sqr_distance_min**0.5


#функция остановки отображения симуляции при закрытии окна питона
def check_stop_PyGame():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            global running
            running=False#если надо прекратить симуляцию

#функции проверки суммарной кинетической и потенциальной энергий систмемы
def check_kinetic_energy():
    kinetic_energy=0
    # for p in particles: #с учетом пробной частицы
    for p in particles[:-1]:
        kinetic_energy += (p.velocity_x**2+p.velocity_y**2)**0.5
    return kinetic_energy

def check_potential_energy():
    potential_energy=0
    # for i in  range(0, nn): #с учетом пробной частицы
    #     for j in  range(i+1, nn):
    for i in  range(0, nn-1):
        for j in  range(i+1, nn-1):
            r_x = particles[j].x - particles[i].x
            r_y = particles[j].y - particles[i].y
            dobavka_k_rasstoyaniyu=2
            distance = (r_x**2 + r_y**2)**0.5+dobavka_k_rasstoyaniyu
            potential_energy+= abs(k*particles[i].charge*particles[j].charge/distance)
    return potential_energy

#вспомогательная функци присваивания цвета частице в зависимости от ее заряда
def assignment_color(charge, color):
        if charge<0: participle_color=(0,0,255)
        else: participle_color=(255,0,0)
        if color == (0,255,0):participle_color=(0,255,0)
        return participle_color

#функция создания "главной" частицы
def spawn_main_particle(X, Y, V_X, V_Y,  mass, charge, radius):
    particle = Particle(mass=mass, radius=radius, charge=charge, x=X, y=Y, 
    velocity_x=V_X, velocity_y=V_Y, color=(0,255,0))
    particles.append(particle)
    global nn
    nn+=1

#функция создания одинаковых частиц "плазмы"
def spawn_same_plasma_particles(quantity,  percentage_of_positive, height, width, mass, charge, radius):
    for i in range(0, int(quantity*(percentage_of_positive)/100)):
        particle = Particle(mass=mass, radius=radius, charge=charge, x=randrange(int(width/10),int(9*width/10)), y=randrange(int(height/10),int(9*height/10)), 
        velocity_x=0, velocity_y=0, color=())
        particles.append(particle) 

    for i in range(0, int(quantity*(100-percentage_of_positive)/100)):
        particle = Particle(mass=mass, radius=radius, charge=-charge, x=randrange(int(width/10),int(9*width/10)), y=randrange(int(height/10),int(9*height/10)), 
        velocity_x=0, velocity_y=0, color=())
        particles.append(particle)
        # print(f"Mass: {particles[i].mass}, Charge: {particles[i].charge}, Position: ({particles[i].x}, {particles[i].y}), Velocity: ({particles[i].velocity_x}, {particles[i].velocity_y})")

#остановка процесса расчета
def STOP():
    global running
    running=False
keyboard.add_hotkey("esc", STOP)

################################################################################################
#Particles Class Definition
class Particle:
    def __init__(self, mass, radius, charge, x, y, velocity_x, velocity_y, color):
        self.color=assignment_color(charge, color)
        self.radius=radius
        self.mass = mass
        self.charge = charge
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update_Position(self):
        self.x += self.velocity_x*dt
        self.y += self.velocity_y*dt

    def update_Velocity(self, other):
        r_x = other.x - self.x
        r_y = other.y - self.y

        dobavka_k_rasstoyaniyu=5
        distance = (r_x**2 + r_y**2)**0.5+dobavka_k_rasstoyaniyu
        force_magnitude = -k * (self.charge * other.charge) / distance**2
        force_x = force_magnitude * (r_x / distance)
        force_y = force_magnitude * (r_y / distance)

        acceleration_x = force_x/self.mass
        acceleration_y = force_y/self.mass
        self.velocity_x += acceleration_x*dt
        self.velocity_y += acceleration_y*dt
        
        other.velocity_x += -dt*force_x/other.mass
        other.velocity_y += -dt*force_y/other.mass
    
    def check_wall_collision(self):
        if self.x+r1>=width or self.x-r1<=0: self.velocity_x=-self.velocity_x
        if self.y+r1>=height or self.y-r1<=0: self.velocity_y=-self.velocity_y
#вспомогательный класс хранения данных о частице в какую-то итерацию
class Memory:
    def __init__(self, Iteration, color, radius, x, y):
        self.Iteration=Iteration
        self.color=color
        self.radius=radius
        self.x = x
        self.y = y

############################################################################################
# создаем частицы
spawn_same_plasma_particles(nn,  positive_percent, height, width, m1, Charge, r1)


# spawn_main_particle(main_X, main_Y, main_Vx, main_Vy,  main_m, main_charge, main_r)

while running and iterations<MAX_iterations:

    if iterations>200 and spawn: 
        # создаем главную частицу после некоторого времени(чтобы дать плазме прийти в однородное состояние)
        spawn_main_particle(main_X, main_Y, main_Vx, main_Vy,  main_m, main_charge, main_r)
        spawn=False

    check_stop_PyGame()
    win.fill((0,0,0))
    # pygame.display.set_mode((width, height))

    for p in particles:#передвигаем частицы
        p.update_Position()
        p.check_wall_collision()
        pygame.draw.circle(win, p.color, (p.x, p.y), p.radius)

    for i in  range(0, nn):
        for j in  range(i+1, nn):
            particles[i].update_Velocity(particles[j])#обновляем скорости частиц

    sqrt_dist_sum=free_zone_check(nn-1)+sqrt_dist_sum
    iterations+=1
    pygame.draw.rect(win, (0,0,255), pygame.Rect(-r1, -r1, width0+2*r1, height0+2*r1), 5)
    pygame.draw.rect(win, color, pygame.Rect(-r1, -r1,  width+2*r1, height+2*r1), 5)

    
    pygame.display.update()
    pygame.time.delay(10)
    # print(check_kinetic_energy()+check_potential_energy())


# print(f"Mass: {particles[nn-1].mass}, Charge: {particles[nn-1].charge}, Position: ({particles[nn-1].x}, {particles[nn-1].y}), Velocity: ({particles[nn-1].velocity_x}, {particles[nn-1].velocity_y})")
# print("average distance between Main and particle with different charge: "+str(sqrt_dist_sum/iterations))
# print("Main Charge: "+str(particles[nn-1].charge)+" Main start Velocity: "+ str((main_Vx**2+main_Vy**2)**0.5))
pygame.quit()
