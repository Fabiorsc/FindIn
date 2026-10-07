import json
import sys
from pathlib import Path

# Determina o diretório base dinamicamente (Funciona em Debug, Run e .exe compilado)
if getattr(sys, 'frozen', False):
    # Diretório onde o executável .exe está localizado
    BASE_DIR = Path(sys.executable).parent
else:
    # Diretório raiz do projeto em ambiente de desenvolvimento (.py)
    BASE_DIR = Path(__file__).resolve().parents[0]

CONFIG_FILE = BASE_DIR / "config.json"
MAX_HISTORICO = 10

def carregar_historico():
    """Carrega o histórico de buscas a partir do config.json."""
    if not CONFIG_FILE.exists():
        return {"pastas": [], "termos": []}
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return {
                "pastas": dados.get("pastas", []),
                "termos": dados.get("termos", [])
            }
    except Exception:
        return {"pastas": [], "termos": []}

def salvar_busca(pasta, termo):
    """Salva a pasta e o termo pesquisados mantendo o limite de MAX_HISTORICO."""
    historico = carregar_historico()

    pastas = historico.get("pastas", [])
    termos = historico.get("termos", [])

    # Remove duplicadas e insere no topo
    if pasta in pastas:
        pastas.remove(pasta)
    pastas.insert(0, pasta)

    if termo in termos:
        termos.remove(termo)
    termos.insert(0, termo)

    dados = {
        "pastas": pastas[:MAX_HISTORICO],
        "termos": termos[:MAX_HISTORICO]
    }

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar histórico em {CONFIG_FILE}: {e}")


# import json
# from pathlib import Path

# CONFIG_FILE = Path("config.json")
# MAX_HISTORICO = 5

# def carregar_historico():
#     """Lê as últimas buscas do config.json. Se não existir, retorna padrão."""
#     if not CONFIG_FILE.exists():
#         return {"pastas": [], "termos": []}
    
#     try:
#         with open(CONFIG_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception:
#         return {"pastas": [], "termos": []}

# def salvar_busca(pasta, termo):
#     """Salva a nova busca no topo do histórico sem duplicar."""
#     dados = carregar_historico()
    
#     # Atualiza lista de pastas
#     if pasta in dados["pastas"]:
#         dados["pastas"].remove(pasta)
#     dados["pastas"].insert(0, pasta)
#     dados["pastas"] = dados["pastas"][:MAX_HISTORICO]

#     # Atualiza lista de termos
#     if termo in dados["termos"]:
#         dados["termos"].remove(termo)
#     dados["termos"].insert(0, termo)
#     dados["termos"] = dados["termos"][:MAX_HISTORICO]

#     # Escreve de volta no JSON
#     try:
#         with open(CONFIG_FILE, "w", encoding="utf-8") as f:
#             json.dump(dados, f, ensure_ascii=False, indent=2)
#     except Exception:
#         pass  # Falha silenciosa, pois a perda deste dado não é crítica
