from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil
import time

# 1. Pixhawk bağlantısı
pixhawk = mavutil.mavlink_connection('/dev/ttyACM1', baud=115200)
pixhawk.wait_heartbeat()
print('Pixhawk’a bağlanıldı.')

# 2. Mevcut görevleri temizle
pixhawk.mav.mission_clear_all_send(
    pixhawk.target_system,
    pixhawk.target_component
)
time.sleep(1)

# 3. Görev tanımla (2 nokta)
mission_count = 2
pixhawk.mav.mission_count_send(
    pixhawk.target_system,
    pixhawk.target_component,
    mission_count
)

# Nokta 0 – TAKEOFF
pixhawk.mav.mission_item_send(
    pixhawk.target_system,
    pixhawk.target_component,
    0,
    mavlink2.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavlink2.MAV_CMD_NAV_TAKEOFF,
    0, 1,
    0, 0, 0, 0,
    40.0000, 32.0000, 10
)

# Nokta 1 – WAYPOINT
pixhawk.mav.mission_item_send(
    pixhawk.target_system,
    pixhawk.target_component,
    1,
    mavlink2.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavlink2.MAV_CMD_NAV_WAYPOINT,
    0, 1,
    0, 0, 0, 0,
    40.0001, 32.0001, 10
)

# 4. ARM komutu
pixhawk.mav.command_long_send(
    pixhawk.target_system,
    pixhawk.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0  # Doğru: toplam 7 parametre
)
print("ARM komutu gönderildi.")
time.sleep(2)

# 5. Uçuş modunu 'MISSION' yap
mode = "MISSION"
mode_mapping = pixhawk.mode_mapping()

if mode in mode_mapping:
    main_mode, custom_mode, sub_mode = mode_mapping[mode]
    pixhawk.set_mode_px4(main_mode, custom_mode, sub_mode)
    print(f"Uçuş modu {mode} olarak ayarlandı.")
else:
    print(f" '{mode}' modu mevcut değil. Kullanılabilir modlar: {mode_mapping}")

time.sleep(1)

# 6. Görevi başlat 
pixhawk.mav.command_long_send(
    pixhawk.target_system,
    pixhawk.target_component,
    mavutil.mavlink.MAV_CMD_MISSION_START,
    0,
    0, 0, 0, 0, 0, 0, 0
)
print("Görev başlatıldı.")

# 7. (İsteğe Bağlı) Görev sonunda iniş komutu göndermek istersen
# Aşağıdaki kodu yorum satırı yapabilir ya da geç gönderebilirsin

time.sleep(10)  # Görev tamamlanana kadar bekle
pixhawk.mav.command_long_send(
    pixhawk.target_system,
    pixhawk.target_component,
    mavutil.mavlink.MAV_CMD_NAV_LAND,
    0,
    0, 0, 0, 0, 0, 0, 0
)
print("İniş komutu gönderildi.")

