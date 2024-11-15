from typing import List


areas2tasks = {
    'Flicking': {
        'Dynamic': [
            'VT Floatshot VALORANT',
            'VT Angleshot VALORANT',
            'VT Adjustshot VALORANT',
        ],
        'Core': [
            'VT DotTS VALORANT',
            'VT Miniphase VALORANT',
            'VT Fourshot Adaptive VALORANT',
        ],
        'Reflex': [
            'VT 1w1t VALORANT',
            'VT Widereflex VALORANT',
        ],
    },
    'Micros': {
        'Evasive': [
            'VT Microshot VALORANT',
            'VT Angleshot Micro VALORANT',
            'VT Skyclick Multi VALORANT',
        ],
        'Core': [
            'VT Angelic Click VALORANT',
            'VT MiniTS VALORANT',
            'VT Micro 2 Sphere VALORANT',
        ],
        'Reflex': [
            'VT Peekshot VALORANT',
            'VT Micropace VALORANT',
            'VT Microcluster VALORANT',
        ],
    },
    'Stability': {
        'Strafe': [
            'VT Controlstrafes VALORANT',
            'VT Peektrack VALORANT',
        ],
        'Precise': [
            'VT Angle Track VALORANT',
            'VT Adjust Track VALORANT',
        ],
    },
}


def get_area1s() -> List[str]:
    return ['Flicking', 'Micros', 'Stability']


def get_area2s(area1: str | None) -> List[str]:
    if area1 is None:
        return []
    elif area1 == 'Flicking':
        return ['Dynamic', 'Core', 'Reflex']
    elif area1 == 'Micros':
        return ['Evasive', 'Core', 'Reflex']
    elif area1 == 'Stability':
        return ['Strafe', 'Precise']
    else:
        raise ValueError(area1)


def get_tasks(area1: str | None, area2: str | None) -> List[str]:
    if area1 is None or area2 is None:
        return []
    return areas2tasks[area1][area2]
