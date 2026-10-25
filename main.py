import pygame
import random
import math
import cv2
import time

generation=1

img=cv2.imread("test.png")
background = pygame.image.load("test.png")
background2=pygame.transform.scale(background,(300,300))
X_image=pygame.image.load("X.png")


answer=[]
for i in range(100):
    for w in range(100):
        if img[i][w][0] == 0:
            answer.append((w,i))

pygame.init()

screen_width = img.shape[0]*8 +300
screen_height = img.shape[1]*8

font = pygame.font.SysFont(None, 30, False, False)

total_tick=1000
Mutation_percent=0.2

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("image by circles")

white = (255, 255, 255)
black = (0,   0,   0)

class circle():
    def __init__(self,start_angle,radius,angle_speed,color,pos=[screen_width/2, screen_height/2]):
        self.pos=pos
        self.angle=start_angle
        self.radius=radius
        self.angle_speed=angle_speed
        self.color=color

        self.next_pos=[self.pos[0] + self.radius*math.cos(self.angle),self.pos[1] + self.radius*math.sin(self.angle)]

    def calculate_next_pos(self):
        return [self.pos[0] + self.radius*math.cos(self.angle),self.pos[1] + self.radius*math.sin(self.angle)]

    def draw_circle(self):
        pygame.draw.circle(screen, self.color, self.pos,        self.radius,    1)
        pygame.draw.circle(screen, self.color, self.next_pos,   2                )
        pygame.draw.line(  screen, self.color, self.pos, self.next_pos,1)


class unit():
    def __init__(self,start_angle,radius,angle_speed,pos):
        self.circles=[circle(start_angle,radius,angle_speed,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),[pos[0]+img.shape[0]/2,pos[1]+img.shape[1]/2])]
        self.lines=set()
        self.pos=pos

        self.point=0

    def append_circle(self,start_angle,radius,angle_speed):
        # self.circles.append(circle(random.uniform(0,2*math.pi),
        #                            random.uniform(max(0,self.circles[-1].radius*0.8),self.circles[-1].radius*1.2),
        #                            random.randint(self.circles[-1].angle_speed-1,self.circles[-1].angle_speed+1),
        #                            self.circles[-1].next_pos))
        self.circles.append(circle(start_angle,
                                    radius,
                                    angle_speed,
                                    (random.randint(0,255),random.randint(0,255),random.randint(0,255)),
                                    self.circles[-1].next_pos))

    def update_pos(self):
        for i in range(0,len(self.circles)):
            self.circles[i].angle+= 2*math.pi * self.circles[i].angle_speed /total_tick 
            self.circles[i].next_pos=self.circles[i].calculate_next_pos()
            if i!=len(self.circles)-1:
                self.circles[i+1].pos=self.circles[i].next_pos

    def draw_unit(self):
        for i in range(len(self.circles)):
            self.circles[i].draw_circle()
        point_pos=(int(self.circles[-1].next_pos[0]-self.pos[0]),int(self.circles[-1].next_pos[1]-self.pos[1]))
        if not point_pos in answer:
            self.point-=1
        elif not point_pos in self.lines:
            self.point+=1
        self.lines.add(point_pos)

def next_generator(parents_1,parents_2,replace_target):
    next_circles=[]
    
    circle_num=int((len(unit_matrix[parents_1[0]][parents_1[1]].circles)+len(unit_matrix[parents_2[0]][parents_2[1]].circles))/2)
    while random.random()<Mutation_percent:
        if random.randint(1,2)==1:
            circle_num-=1
        else:
            circle_num+=1
    circle_num=max(1,circle_num)

    for w in range(circle_num):
        if random.randint(1,2)==1 and len(unit_matrix[parents_1[0]][parents_1[1]].circles)>w:
            next_circles.append([unit_matrix[parents_1[0]][parents_1[1]].circles[w].angle,
                                 unit_matrix[parents_1[0]][parents_1[1]].circles[w].radius,
                                 unit_matrix[parents_1[0]][parents_1[1]].circles[w].angle_speed])
        elif len(unit_matrix[parents_2[0]][parents_2[1]].circles)>w:
            next_circles.append([unit_matrix[parents_2[0]][parents_2[1]].circles[w].angle,
                                 unit_matrix[parents_2[0]][parents_2[1]].circles[w].radius,
                                 unit_matrix[parents_2[0]][parents_2[1]].circles[w].angle_speed])
        else:
            next_circles.append([random.uniform(0,2*math.pi),
                                 random.randint(1,unit_matrix[parents_1[0]][parents_1[1]].circles[-1].radius),
                                 random.randint(abs(unit_matrix[parents_1[0]][parents_1[1]].circles[-1].angle_speed)*-1,abs(unit_matrix[parents_1[0]][parents_1[1]].circles[-1].angle_speed))])

    no_stop_circle=True
    for w in range(len(next_circles)):
        if random.random()<Mutation_percent:
            next_circles[w][0]=random.uniform(0,2*math.pi)
        if random.random()<Mutation_percent:
            next_circles[w][1]=random.randint(1,int(next_circles[w][1]*1.5))
    while no_stop_circle:    
        for w in range(len(next_circles)):
            if random.random()<Mutation_percent:
                if next_circles[w][2]>=0:
                    next_circles[w][2]=random.randint(-1*(next_circles[w][2]+1),next_circles[w][2]+1)
                else:
                    next_circles[w][2]=random.randint(next_circles[w][2]-1,-1*(next_circles[w][2]-1))
            if next_circles[w][2]!=0:
                no_stop_circle=False

    unit_matrix[replace_target[0]][replace_target[1]]=unit(next_circles[0][0],next_circles[0][1],next_circles[0][2],[replace_target[1]*100,replace_target[0]*100])
    for w in range(1,len(next_circles)):
        unit_matrix[replace_target[0]][replace_target[1]].append_circle(next_circles[w][0],next_circles[w][1],next_circles[w][2])
    
            
unit_matrix=[[],
             [],
             [],
             [],
             [],
             [],
             [],
             []]

for i in range(8):
    for w in range(8):
        unit_matrix[i].append(unit(random.uniform(0,2*math.pi),30,1,[w*100,i*100]))

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
        for i in range(8):
            for w in range(8):
                screen.blit(background, (img.shape[0]*w,img.shape[0]*i))
                unit_matrix[i][w].draw_unit()
                for z in unit_matrix[i][w].lines:
                    pygame.draw.circle(screen,black,(unit_matrix[i][w].pos[0]+z[0],unit_matrix[i][w].pos[1]+z[1]),1)
                screen.blit(font.render(f"{unit_matrix[i][w].point}", True, "red", None),unit_matrix[i][w].pos)
                unit_matrix[i][w].update_pos()
        tick-=1

        sum_point=0
        sum_circle_count=0
        max_point=total_tick*-1 -1
        max_unit=(0,0)
        for i in range(8):
            for w in range(8):
                sum_point += unit_matrix[i][w].point
                sum_circle_count += len(unit_matrix[i][w].circles)
                if unit_matrix[i][w].point>max_point:
                    max_point=unit_matrix[i][w].point
                    max_unit=(i,w)
        
        screen.blit(background2,(800,100))
        screen.blit(font.render(f"avg point: {round(sum_point/64,3)}", True, "red", None),(850,20))
        screen.blit(font.render(f"avg circle: {round(sum_circle_count/64,3)}", True, "red", None),(850,40))
        screen.blit(font.render(f"generation: {generation}", True, "red", None),(850,60))
        screen.blit(font.render(f"pos: {max_unit}", True, "red", None),(850,420))
        screen.blit(font.render(f"point: {round(max_point,3)}", True, "red", None),(850,440))
        screen.blit(font.render(f"circle: {len(unit_matrix[max_unit[0]][max_unit[1]].circles)}", True, "red", None),(850,460))

        
        for i in unit_matrix[max_unit[0]][max_unit[1]].circles:
            temp_circles=circle(i.angle,i.radius*3,i.angle_speed,i.color,
                                (3*(i.pos[0]-100*max_unit[1])+800,
                                 3*(i.pos[1]-100*max_unit[0])+100
                                 ))

            temp_circles.draw_circle()
        for w in unit_matrix[max_unit[0]][max_unit[1]].lines:
            pygame.draw.circle(screen,black,(800+w[0]*3,w[1]*3+100),1)
        pygame.display.flip()  # 화면을 업데이트합니다.
    else:
        unit_list=[]
        for i in range(8):
            for w in range(8):
                unit_list.append((i,w,unit_matrix[i][w].point))
        unit_list.sort(key=lambda x:x[2])

        for i in range(32):
            screen.blit(X_image,(unit_list[i][1]*100,unit_list[i][0]*100))
            pygame.display.flip()
            time.sleep(0.05)
        time.sleep(0.5)
        for i in range(32):
            pygame.draw.rect(screen,'white',[unit_list[i][1]*100,unit_list[i][0]*100,100,100])
        pygame.display.flip()

        time.sleep(0.3)


        parents=list(range(-1,-33,-1))
        random.shuffle(parents)
        for i in range(16):
            next_generator(unit_list[parents.pop()],unit_list[parents.pop()],unit_list[i])

        parents=list(range(-1,-17,-1))
        random.shuffle(parents)
        for i in range(16,24):
            next_generator(unit_list[parents.pop()],unit_list[parents.pop()],unit_list[i])
        
        parents=list(range(-1,-17,-1))
        random.shuffle(parents)
        for i in range(24, 32):
            next_generator(unit_list[parents.pop()],unit_list[parents.pop()],unit_list[i])
        



        for i in range(32):
            screen.blit(background, (img.shape[0]*unit_list[i][1],img.shape[0]*unit_list[i][0]))
            for w in unit_matrix[unit_list[i][0]][unit_list[i][1]].circles:
                w.draw_circle()
            unit_matrix[unit_list[i][0]][unit_list[i][1]].draw_unit()
            pygame.display.flip()
            time.sleep(0.03)

        tick=total_tick
        generation+=1
        for i in range(8):
            for w in range(8):
                unit_matrix[i][w].lines=set()
                unit_matrix[i][w].point=0
pygame.quit()