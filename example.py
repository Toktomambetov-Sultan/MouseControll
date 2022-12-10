from HMRunner import HMRunner
import autopy
import os
Runner = HMRunner()
stop = False


def LeftMouseClick(hand, self):
    if hand.landmark[4] != None and hand.landmark[8] != None and not stop:
        x1, y1, z1 = hand.landmark[4].x, hand.landmark[4].y, hand.landmark[4].z
        x2, y2, z2 = hand.landmark[8].x, hand.landmark[8].y, hand.landmark[8].z

        length = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        if length <= 0.004:
            autopy.mouse.toggle(
                down=True, button=autopy.mouse.Button.LEFT)
            return True
        else:
            autopy.mouse.toggle(
                down=False, button=autopy.mouse.Button.LEFT)
    return False


Runner.addEvent(
    LeftMouseClick,
    "RightMousePressedDown"
)


def RightMouseClick(hand, self):
    if hand.landmark[4] != None and hand.landmark[12] != None and not stop:
        x1, y1, z1 = hand.landmark[4].x, hand.landmark[4].y, hand.landmark[4].z
        x2, y2, z2 = hand.landmark[12].x, hand.landmark[12].y, hand.landmark[12].z

        length = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        if length <= 0.004:
            autopy.mouse.toggle(
                down=True, button=autopy.mouse.Button.RIGHT)
            return True
        else:
            autopy.mouse.toggle(
                down=False, button=autopy.mouse.Button.RIGHT)
    return False


Runner.addEvent(
    RightMouseClick,
    "RightMousePressedDown"
)


def MouseMove(hand, self):
    handmark = hand.landmark[0]
    if handmark != None and not stop:
        try:
            x = (handmark.x - 0.2)/0.6
            if x >= 1:
                x = 1
            if x <= 0:
                x = 0
            y = (handmark.y - 0.4)/0.4
            if y >= 1:
                y = 1
            if y <= 0:
                y = 0
            autopy.mouse.move(
                self.ScreenSize.width*(1-x), self.ScreenSize.height*y)
        except Exception as inst:
            print("Error: ", inst)


Runner.addEvent(
    MouseMove,
    "MouseMove"
)


def VolumeControl(hand, self):
    global stop
    if (hand.landmark[8] != None and hand.landmark[6] != None and hand.landmark[5] != None) and (
        hand.landmark[12] != None and hand.landmark[10] != None and hand.landmark[9] != None
    ) and (
        hand.landmark[16] != None and hand.landmark[14] != None and hand.landmark[13] != None
    ) and (
        hand.landmark[20] != None and hand.landmark[18] != None and hand.landmark[17] != None
    ) and (
        hand.landmark[5].x <
            hand.landmark[8].x < hand.landmark[6].x
    ) and (
            hand.landmark[9].x <
        hand.landmark[12].x < hand.landmark[10].x
        ) and (
            (hand.landmark[13].x) <
        hand.landmark[16].x < (hand.landmark[14].x)
    ) and (
            (hand.landmark[17].x) < (
                hand.landmark[20].x) < (hand.landmark[18].x)
    ):
        sin = (hand.landmark[5].x - hand.landmark[9].x)/(((hand.landmark[5].x -
                                                           hand.landmark[6].x)**2 + (hand.landmark[6].y-hand.landmark[5].y)**2))
        if sin > 1.5:
            sin = 1.5
        elif sin < -0.5:
            sin = -0.5
        volume = int(100*(1-((sin+0.5)/2)))
        cmd = f"pactl -- set-sink-volume 0 {volume}%"
        os.system(cmd)
        stop = True
        return True
    stop = False
    return False


Runner.addEvent(
    VolumeControl,
    "VolumeControl"
)


def BrightnessControl(hand, self):
    global stop
    if (hand.landmark[8] != None and hand.landmark[6] != None and hand.landmark[5] != None) and (
        hand.landmark[12] != None and hand.landmark[10] != None and hand.landmark[9] != None
    ) and (
        hand.landmark[16] != None and hand.landmark[14] != None and hand.landmark[13] != None
    ) and (
        hand.landmark[20] != None and hand.landmark[18] != None and hand.landmark[17] != None
    ) and (
        hand.landmark[5].x <
            hand.landmark[6].x < hand.landmark[8].x
    ) and (
            hand.landmark[9].x <
        hand.landmark[12].x < hand.landmark[10].x
        ) and (
            (hand.landmark[13].x) <
        hand.landmark[16].x < (hand.landmark[14].x)
    ) and (
            (hand.landmark[17].x) < (
                hand.landmark[20].x) < (hand.landmark[18].x)
    ):
        sin = (hand.landmark[5].x - hand.landmark[9].x)/(((hand.landmark[5].x -
                                                           hand.landmark[6].x)**2 + (hand.landmark[6].y-hand.landmark[5].y)**2))
        if sin > 1.5:
            sin = 1.5
        elif sin < -0.5:
            sin = -0.5
        volume = 0.2+round((1-((sin+0.5)/2))/0.8, 2)
        if volume > 1:
            volume = 1
        cmd = f"xrandr --output eDP-1 --brightness {volume}"
        os.system(cmd)
        stop = True
        return True
    stop = False
    return False


Runner.addEvent(
    BrightnessControl,
    "BrightnessControl"
)

Runner.run()
