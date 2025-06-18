# preemptive_priority.py

import time
from print_console import print_console_result

def run_preemptive_priority(processes):
    # 도착 시간 순으로 프로세스 정렬
    processes = sorted(processes, key=lambda p: p.arrival_time) 

    ready_queue = [] 
    completed = []          # 완료 상태 저장 공간
    running_process = None  # 실행 프로세스
    gantt_log = []          # Time Out이나 작업 완료 시에 로그 추가
    current_start = None    # 해당 디스패치의 시작 시간

    sum_waiting_time = 0
    sum_response_time = 0
    sum_return_time = 0

    print("선점 우선순위 시뮬레이션 시작...")

    # 경과 시간 카운트
    elapsed = 0

    # Ready Queue에 아직 프로세스가 남아 있거나 실행중인 프로세스가 있으면 반복
    while processes or ready_queue or running_process:

        print(f"{elapsed}m/s")

        # 새로 도착한 프로세스들을 레디큐에 추가
        while processes and processes[0].arrival_time <= elapsed:
            ready_queue.append(processes.pop(0))

        # 현재 실행 중인 프로세스를 선점할 수 있는 새 프로세스가 도착 했는지 확인
        # 도착한 프로세스들을 후보로
        candidates = [p for p in ready_queue if p.arrival_time <= elapsed]

        # 후보들이 존재한다면(도착한 프로세스가 있다면)
        if candidates:

            # 우선 순위가 가장 높은 프로세스를 선택
            highest = min(candidates, key=lambda p: p.priority)

            # 실행 중인 프로세스가 없다면
            if running_process is None:

                # Dispatch
                ready_queue.remove(highest)
                running_process = highest

                # 처음 디스패치 된 프로세스라면
                if running_process.start_time is None:
                    # 프로세스 시작 시간 기록 
                    running_process.start_time = elapsed
                    running_process.response_time = elapsed - running_process.arrival_time
                
                # 현재 디스패치 과정의 시작 시간 기록
                current_start = elapsed

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} 실행 시작")

            # 실행 중인 프로세스가 있지만, 선점 조건 발동
            elif highest.priority < running_process.priority:
                # 로그 추가
                gantt_log.append((running_process.pid, current_start, elapsed+1))

                # 현재 실행 중인 프로세스를 Ready Queue에 되돌려 보낸다.
                ready_queue.append(running_process)

                # Dispatch
                running_process = highest
                ready_queue.remove(highest)

                # 처음 디스패치 된 프로세스라면
                if running_process.start_time is None:
                    # 프로세스 시작 시간 기록 
                    running_process.start_time = elapsed
                    running_process.response_time = elapsed - running_process.arrival_time

                # 현재 디스패치 과정의 시작 시간 기록
                current_start = elapsed

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} 선점 실행 시작")



        # 실행 중인 프로세스가 있다면
        if running_process is not None:

            # 실행 중인 프로세스의 남은 작업 시간 감소
            running_process.remaining_time -= 1
            
            # 만약 남은 작업시간이 0이라면
            if running_process.remaining_time == 0:

                # 로그 추가
                gantt_log.append((running_process.pid, current_start, elapsed+1))

                # 종료 시간 기록
                running_process.finish_time = elapsed + 1
                # 반환 시간 기록
                running_process.return_time = elapsed + 1 - running_process.arrival_time 
                # 대기 시간 기록
                running_process.waiting_time = running_process.return_time - running_process.service_time


                # 출력
                print(f"{elapsed+1}m/s: {running_process.pid} 실행 종료")
                

                # 평균 시간 계산을 위한 누적 로직
                sum_response_time += running_process.response_time
                sum_return_time += running_process.return_time
                sum_waiting_time += running_process.waiting_time

                # 실행 완료 큐에 추가
                completed.append(running_process)

                # 실행 중인 프로세스를 없앤다.
                running_process = None


        # 1초 경과 (루프 당 1초 씩 증가)
        elapsed += 1
        time.sleep(0.001)

    # 결과 출력
    print_console_result(completed, sum_waiting_time, sum_response_time, sum_return_time)

    return completed, gantt_log