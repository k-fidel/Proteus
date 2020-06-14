import Adafruit_CharLCD as LCD
import time
import random
import smbus

bus = smbus.SMBus(1)
arduino = 12
rs = 12
en = 16
D4 = 18
D5 = 23
D6 = 24
D7 = 25
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(rs, en, D4, D5, D6, D7, lcd_columns, lcd_rows)

carMap = [0b00000, 0b00000, 0b10100, 0b11110, 0b11111, 0b11110, 0b10100, 0b00000]
StageMap = [0b10001, 0b01010, 0b00100, 0b11111, 0b11111, 0b00100, 0b01010, 0b10001]
GoalMap = [0b00100, 0b01111, 0b10100, 0b10100, 0b01111, 0b00101, 0b11110, 0b00100]
NegativeHeartMap = [0b00000, 0b01010, 0b10101, 0b10001, 0b10001, 0b01010, 0b00100, 0b00000]
HeartMap = [0b00000, 0b01010, 0b11111, 0b11111, 0b11111, 0b01110, 0b00100, 0b00000]
Score_empty_heartMap = [0b00000, 0b01010, 0b10101, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100]
Score_half_heartMap = [0b00000, 0b01010, 0b10101, 0b10001, 0b11111, 0b11111, 0b01110, 0b00100]
Score_full_heartMap = [0b00000, 0b01010, 0b11111, 0b11111, 0b11111, 0b11111, 0b01110, 0b00100]

lcd.create_char(0, carMap)
lcd.create_char(1, StageMap)
lcd.create_char(2, GoalMap)
lcd.create_char(3, NegativeHeartMap)
lcd.create_char(4, HeartMap)

Goal = 2
Stage = 1
empty_Heart = 3
Heart = 4

Item = [Stage, Goal, Stage, empty_Heart, Stage, Heart]


y_pos = 1
y_cash = 16
y_stage = 16
y_emp_heart = 16
y_heart = 16

life = 3
point = 0
x_stage_flag = False
cnt = 0
choice = 0

x_stage = 0
x_cash = 0
x_emp_heart = 0
x_heart = 0


def dismiss(point, life):
    lcd.clear()
    lcd.set_cursor(4, 0)
    lcd.message("Game over")
    lcd.set_cursor(0, 1)
    lcd.message("$: " + str(point)+" Life: " + str(life))
    exit()


def item_cash(y_car, y_cash1_, y_stage_, y_heart_, y_emp_heart_, x_car, x_stage_, x_cash_, x_emp_heart_, x_heart_):
    global life, point
    print(point, life)
    if 0 <= point < 100 or 1 <= life <= 3:
        if y_car == y_cash1_:
                point += 1
        if y_car == y_stage_:
            if x_car == x_stage_:
                if life <= 0:
                    dismiss(point, life)
                else:
                    life -= 1
        if y_car == y_heart_:
            if x_car == x_heart_:
                if life >= 3:
                    pass
                else:
                    life += 1

        if y_car == y_emp_heart_:
            if x_car == x_emp_heart_:
                if life <= 1:
                    dismiss(point, life)
                else:
                    life -= 1
                    point -= 1

    elif point >= 100:
        dismiss(point, life)
    elif point < 0 or life < 1:
        dismiss(point, life)


def design(y_car,x_car,item,y_item,x_item):
    lcd.set_cursor(y_car, x_car)
    lcd.write8(0, True)
    lcd.set_cursor(y_item, x_item)
    lcd.write8(item, True)
    time.sleep(0.1)


# Stage, Goal, empty_Heart, Heart
def items_up_to_down(x_pos, y_pos, choice, x_stage, x_cash, x_emp_heart, x_heart):
    global y_cash, y_stage, y_emp_heart, y_heart
    if choice == 1:
        if y_stage == 1:
            y_stage = 17
        y_stage -= 1
        design(y_pos, x_pos, 1, y_stage, x_stage)
        item_cash(y_pos, 16, y_stage, 16, 16, x_pos, x_stage, x_cash, x_emp_heart, x_heart)

    elif choice == 2:
        if y_cash == 1:
            y_cash = 17
        y_cash -= 1
        design(y_pos, x_pos, 2, y_cash, x_cash)
        item_cash(y_pos, y_cash, 16, 16, 16, x_pos, x_stage, x_cash, x_emp_heart, x_heart)

    elif choice == 3:
        if y_emp_heart == 1:
            y_emp_heart = 17
        y_emp_heart -= 1
        design(y_pos, x_pos, 3, y_emp_heart, x_emp_heart)
        item_cash(y_pos, 16, 16, 16,y_emp_heart, x_pos, x_stage, x_cash, x_emp_heart, x_heart)

    elif choice == 4:
        if y_heart == 1:
            y_heart = 17
        y_heart -= 1
        design(y_pos, x_pos, 4, y_heart, x_heart)
        item_cash(y_pos, 16, 16, y_heart, 16, x_pos, x_stage, x_cash, x_emp_heart, x_heart)


def car_down_to_up():
    global y_pos, x_pos
    pos = bus.read_byte(arduino)
    if pos == 76:
        x_pos = 0
    elif pos == 82:
        x_pos = 1
    elif pos == 85:
        y_pos += 1
        if y_pos > 15:
            y_pos = 15
    elif pos == 68:
        y_pos -= 1
        if y_pos < 1:
            y_pos = 1
    return x_pos, y_pos


if __name__ == "__main__":

    while 1:
        if cnt > 15 or cnt == 0:
            choice = random.choice(Item)
            if choice == 1:
                x_stage = random.randint(0, 1)
            if choice == 2:
                x_cash = random.randint(0, 1)
            if choice == 3:
                x_emp_heart = random.randint(0, 1)
            if choice == 4:
                x_heart = random.randint(0, 1)
            cnt = 0
        cnt += 1
        xpos, ypos = car_down_to_up()
        items_up_to_down(x_pos, y_pos, choice, x_stage, x_cash, x_emp_heart, x_heart)

        lcd.clear()
