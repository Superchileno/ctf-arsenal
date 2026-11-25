import os
from PIL import Image

W = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/6puntos/work"
O = W + "/zoom"
os.makedirs(O, exist_ok=True)

recortes = [
    ("IMG_2E8C.jpg", (980, 520, 1330, 680), "2E8C_cartel_municipal"),
    ("IMG_2E8C.jpg", (770, 520, 900, 700), "2E8C_estatua"),
    ("IMG_7C2E.jpg", (1130, 90, 1440, 330), "7C2E_cartel_maranatha"),
    ("IMG_7C2E.jpg", (1330, 380, 1440, 700), "7C2E_nissan"),
    ("IMG_A91F.jpg", (930, 210, 1180, 300), "A91F_escuelas"),
    ("IMG_A91F.jpg", (560, 400, 760, 500), "A91F_patente"),
    ("IMG_19B7.jpg", (150, 700, 400, 830), "19B7_patente"),
    ("IMG_19B7.jpg", (500, 300, 700, 700), "19B7_casa_azul"),
    ("IMG_F03A.jpg", (600, 430, 730, 510), "F03A_kunstmann"),
    ("IMG_F03A.jpg", (1020, 320, 1300, 420), "F03A_maka"),
    ("IMG_F03A.jpg", (840, 450, 960, 530), "F03A_placa"),
    ("IMG_D440.jpg", (250, 380, 480, 540), "D440_islote"),
]

for archivo, caja, nombre in recortes:
    img = Image.open(os.path.join(W, archivo))
    sub = img.crop(caja)
    escala = 4 if max(sub.size) < 400 else 3
    sub = sub.resize((sub.width * escala, sub.height * escala), Image.LANCZOS)
    salida = os.path.join(O, nombre + ".png")
    sub.save(salida)
    print(f"{salida}  ({sub.width}x{sub.height})")
