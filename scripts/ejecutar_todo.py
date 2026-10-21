"""
Ejecuta el análisis completo en orden (pasos 1 a 5).

Uso:
    python scripts/ejecutar_todo.py
    python scripts/ejecutar_todo.py --config otra_config.yaml
    python scripts/ejecutar_todo.py --sin-segunda-capa
"""
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASOS = ["01_matriz_tasas.py", "02_grafo_comunidades.py", "03_sensibilidad.py",
         "04_segunda_capa.py", "05_figuras.py"]


def main():
    extra = [a for a in sys.argv[1:] if a != "--sin-segunda-capa"]
    pasos = [p for p in PASOS if not ("--sin-segunda-capa" in sys.argv and p.startswith("04"))]
    for paso in pasos:
        r = subprocess.run([sys.executable, str(AQUI / paso), *extra])
        if r.returncode != 0:
            sys.exit(f"\nSe detuvo en {paso}. Revise el mensaje anterior.")
    print("\nAnálisis completo. Tablas y figuras en resultados/.")


if __name__ == "__main__":
    main()
