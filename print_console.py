# print_console.py
# 콘솔에 프로세스 성능 지표를 출력하는 함수

def print_console_result(completed, sum_waiting_time, sum_response_time, sum_return_time):

    # 프로세스 도착 순으로 정렬
    completed = sorted(completed, key=lambda p: p.arrival_time)

    # 전체 프로세스 수
    process_count = len(completed)

    print("\n모든 프로세스 종료")

    print("\n---------각 프로세스 별 대기 시간----------")
    for p in completed:
        print(f"{p.pid}  대기시간: {p.waiting_time}m/s")
    print("-------------------------------------------")
    print(f"--> 평균 대기 시간: {sum_waiting_time / process_count}m/s")

    print("\n---------각 프로세스 별 응답 시간----------")
    for p in completed:
        print(f"{p.pid}  응답시간: {p.response_time}m/s")
    print("-------------------------------------------")
    print(f"--> 평균 응답 시간: {sum_response_time / process_count}m/s")

    print("\n---------각 프로세스 별 반환 시간----------")
    for p in completed:
        print(f"{p.pid}  반환시간: {p.return_time}m/s")
    print("-------------------------------------------")
    print(f"--> 평균 반환 시간: {sum_return_time / process_count}m/s")