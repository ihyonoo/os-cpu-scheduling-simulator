'''
프로그램명: CPU 스케쥴링 시뮬레이터
이름: 최현우
학번: 20214056
날짜: 2025-05-30
'''
# main.py


from process import Process
from fcfs import run_fcfs
from sjf import run_sjf
from hrn import run_hrn
from nonpreemptive_priority import run_nonpreemptive_priority
from round_robin import run_round_robin
from srt import run_srt
from preemptive_priority import run_preemptive_priority
from gantt_chart import show_gantt_chart


# 타임 슬라이스 선언
TIME_QUANTUM = 2


# 파일에서 프로세스 데이터 입력을 받는 함수
def read_processes(file_path, time_slice):
    processes = []

    # Read Mode
    with open(file_path, 'r') as f:
        # 파일에서 한 줄씩 Read
        for line in f:
            # 공백을 기준으로 문자열을 나누어 저장
            pid, arrival, service, priority = line.split()
            # process 객체 추가
            processes.append(Process(pid, int(arrival), int(service), int(priority), time_slice))

    # 완성된 process 객체 리스트 반환
    return processes



def main():

    processes = read_processes('input.txt', TIME_QUANTUM)

    # 선택한 스케줄링 알고리즘 실행
    scheduling_algorithm = "Round Robin"

    # ------------------------------비선점형-----------------------------
    if scheduling_algorithm == "FCFS":
        completed = run_fcfs(processes)
        gantt_log = [(p.pid, p.start_time, p.finish_time) for p in completed]

    elif scheduling_algorithm == "SJF":
        completed = run_sjf(processes)
        gantt_log = [(p.pid, p.start_time, p.finish_time) for p in completed]

    elif scheduling_algorithm == "HRN":
        completed = run_hrn(processes)
        gantt_log = [(p.pid, p.start_time, p.finish_time) for p in completed]

    elif scheduling_algorithm == "Nonpreemptive Priority":
        completed = run_nonpreemptive_priority(processes)
        gantt_log = [(p.pid, p.start_time, p.finish_time) for p in completed]

    # ------------------------------선점형------------------------------
    elif scheduling_algorithm == "Round Robin":
        completed, gantt_log = run_round_robin(processes)

    elif scheduling_algorithm == "SRT":
        completed, gantt_log = run_srt(processes) 

    elif scheduling_algorithm == "Preemptive Priority":
        completed, gantt_log = run_preemptive_priority(processes) 
    
    else:   # 예외
        print("Error")
        return


    # 간트 차트 출력
    show_gantt_chart(gantt_log, completed)

if __name__ == '__main__':
    main()
