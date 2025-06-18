# gantt_chart.py
# 간트 차트 GUI 구현

from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsTextItem, QWidget, QVBoxLayout
)
from PyQt5.QtGui import QBrush, QColor, QFont, QPen
from PyQt5.QtCore import QRectF, Qt
import sys


def show_gantt_chart(gantt_log, processes):
    app = QApplication(sys.argv)

    # 장면(Scene) 생성
    scene = QGraphicsScene()  

    # 간트차트 크기 설정
    x_scale = 20            # 시간 단위당 가로 픽셀 크기
    height = 60             # 막대 높이
    y = 120                 # 막대의 Y 위치

    total_time = max(end for _, _, end in gantt_log)  # 전체 실행 시간 계산
    view_width = total_time * x_scale + 200           # 뷰 폭 결정

    view = QGraphicsView(scene)
    view.setFixedSize(view_width, 400)  # 간트차트 창 크기 고정

    font = QFont()
    font.setPointSize(8)  # 기본 텍스트 폰트 크기

    color_map = {}        # 각 프로세스의 색상을 저장
    color_index = 0       # 색상 인덱스 증가용

    process_map = {p.pid: p for p in processes}  # PID -> Process 객체 매핑

    # 간트 차트 데이터 순회
    for i, (pid, start, end) in enumerate(gantt_log):
        proc = process_map.get(pid)
        if proc is None:
            continue

        x = start * x_scale                  # 시작 x 위치
        width = (end - start) * x_scale      # 실행 시간에 따른 폭 계산

        # 프로세스마다 고유 색 지정
        if pid not in color_map:

            # (색조, 채도, 명도), 색조를 70의 배수로 변경
            color_map[pid] = QColor.fromHsv((color_index * 70) % 360, 255, 255)
            color_index += 1

        # 실행 막대
        bar = QGraphicsRectItem(QRectF(x, y, width, height))
        bar.setBrush(QBrush(color_map[pid]))
        scene.addItem(bar)

        # PID + 실행 시간 텍스트 표시
        label = QGraphicsTextItem(f"{pid}({end - start})")
        label_font = QFont()
        label_font.setPointSize(7)  # 폰트 크기기 설정
        label.setFont(label_font)
        label.setPos(x + width / 4, y + 15)  # 막대 내부 위치 조정
        scene.addItem(label)

        # 프로세스 시작 시간 텍스트
        start_time = QGraphicsTextItem(str(start))
        start_time.setFont(font)
        start_time.setDefaultTextColor(Qt.black)                # 검정
        text_width = start_time.boundingRect().width()
        start_time.setPos(x - text_width / 2, y + height + 10)  # 막대 아래 중앙 정렬
        scene.addItem(start_time)

        # 프로세스 도착 시간 텍스트 
        arrival_x = proc.arrival_time * x_scale  # 도착 x 위치
        arrival_time = QGraphicsTextItem(str(proc.arrival_time))
        arrival_time.setFont(font)
        arrival_time.setDefaultTextColor(Qt.blue)               # 블루
        text_width = arrival_time.boundingRect().width()
        arrival_time.setPos(arrival_x - text_width / 2, y + height + 25)  # 중앙 정렬
        scene.addItem(arrival_time)

    # 창 구성
    win = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(view)
    win.setLayout(layout)
    win.setWindowTitle("Gantt Chart")
    win.show()

    sys.exit(app.exec_())  
