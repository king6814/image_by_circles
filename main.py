import pygame
import random
import math


pygame.init()

total_tick=3600

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("image by circles")

white = (255, 255, 255)
black = (0,   0,   0)

class circle():
    def __init__(self,start_angle,radius,angle_speed,pos=[screen_width/2, screen_height/2]):
        self.pos=pos
        self.angle=start_angle
        self.radius=radius
        self.angle_speed=angle_speed
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

        self.next_pos=[self.pos[0] + self.radius*math.cos(self.angle),self.pos[1] + self.radius*math.sin(self.angle)]

    def calculate_next_pos(self):
        return [self.pos[0] + self.radius*math.cos(self.angle),self.pos[1] + self.radius*math.sin(self.angle)]

    def move(self):
        self.pos = math.pi
    
    def draw_circle(self):
        pygame.draw.circle(screen, self.color, self.pos,        self.radius,    1)
        pygame.draw.circle(screen, self.color, self.next_pos,   5                )
        pygame.draw.line(  screen, self.color, self.pos, self.next_pos,1)


class unit():
    def __init__(self,start_angle,radius,angle_speed):
        self.circles=[circle(start_angle,radius,angle_speed)]
        self.lines=set()

    def append_circle(self,start_angle,radius,angle_speed):
        # self.circles.append(circle(random.uniform(0,2*math.pi),
        #                            random.uniform(max(0,self.circles[-1].radius*0.8),self.circles[-1].radius*1.2),
        #                            random.randint(self.circles[-1].angle_speed-1,self.circles[-1].angle_speed+1),
        #                            self.circles[-1].next_pos))
        self.circles.append(circle(start_angle,
                                    radius,
                                    angle_speed,
                                    self.circles[-1].next_pos))

    def update_pos(self):
        for i in range(0,len(self.circles)):
            self.circles[i].angle+= 2*math.pi * self.circles[i].angle_speed /total_tick 
            self.circles[i].next_pos=self.circles[i].calculate_next_pos()
            if i!=len(self.circles)-1:
                self.circles[i+1].pos=self.circles[i].next_pos

    def draw_unit(self):
        for i in range(0,len(self.circles)):
            self.circles[i].draw_circle()
        self.lines.add((int(self.circles[-1].next_pos[0]),int(self.circles[-1].next_pos[1])))
        

a=unit(0,50,1)
a.append_circle(1,25,3)
a.append_circle(2,75,-2)
a.append_circle(3,10,-5)
a.append_circle(4,10,8)
a.append_circle(5,5,5)

# 게임 루프를 위한 변수
tick=total_tick
running = True
while running:
    # 3-1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3-2. 게임 상태 업데이트 (여기서는 비워둠)

    # 3-3. 화면 그리기
    
    if tick:
        screen.fill(white)  # 화면을 하얀색으로 채웁니다.
        a.draw_unit()
        for i in a.lines:
            pygame.draw.circle(screen,black,i,1)
        tick-=1
        a.update_pos()
    pygame.display.flip()  # 화면을 업데이트합니다.
    
# 4. 종료
pygame.quit()