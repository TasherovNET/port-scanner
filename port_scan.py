import socket
import threading

# Список для хранения открытых портов
open_ports = {
    'TCP': [],
    'UDP': []
}

# Функция для проверки TCP порта
def check_tcp_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
    try:
        sock.connect((ip, port))
        print(f"TCP PORT {port} is OPEN")
        open_ports['TCP'].append(port)  # Сохраняем открытый порт
    except (socket.timeout, socket.error):
        print(f"TCP PORT {port} is CLOSED")
    finally:
        sock.close()

# Функция для проверки UDP порта
def check_udp_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
    try:
        sock.sendto(b'', (ip, port))
        # Если получен ответ, порт открыт
        sock.recvfrom(1024)
        print(f"UDP PORT {port} is OPEN")
        open_ports['UDP'].append(port)  # Сохраняем открытый порт
    except socket.timeout:
        print(f"UDP PORT {port} is CLOSED or FILTERED")
    except socket.error:
        print(f"UDP PORT {port} is CLOSED or FILTERED")
    finally:
        sock.close()

# Основная функция для проверки портов
def check_ports(ip, ports):
    threads = []
    for port in ports:
        # Создаем потоки для проверки TCP и UDP
        tcp_thread = threading.Thread(target=check_tcp_port, args=(ip, port))
        udp_thread = threading.Thread(target=check_udp_port, args=(ip, port))
        threads.append(tcp_thread)
        threads.append(udp_thread)
        tcp_thread.start()
        udp_thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

def save_open_ports_to_file(filename):
    with open(filename, 'w') as f:
        if open_ports['TCP']:
            f.write("Open TCP Ports:\n")
            for port in open_ports['TCP']:
                f.write(f"{port}\n")
        else:
            f.write("No open TCP ports found.\n")

        if open_ports['UDP']:
            f.write("Open UDP Ports:\n")
            for port in open_ports['UDP']:
                f.write(f"{port}\n")
        else:
            f.write("No open UDP ports found.\n")

if __name__ == "__main__":
    target_ip = input("Enter the IP address or hostname to scan: ")
    port_range = range(1, 1025)  # Порты от 1 до 1024

    check_ports(target_ip, port_range)

    # Сохранение открытых портов в файл
    save_open_ports_to_file("open_ports.txt")

    # Вывод открытых портов в конце программы
    print("\nOpen Ports Summary:")
    if open_ports['TCP']:
        print("Open TCP Ports:", open_ports['TCP'])
    else:
        print("No open TCP ports found.")

    if open_ports['UDP']:
        print("Open UDP Ports:", open_ports['UDP'])
    else:
        print("No open UDP ports found.")
