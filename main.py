import os
import numpy as np
import rasterio
from scipy.ndimage import generic_filter
from scipy.ndimage import label

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

raster_path = r"D:D:\Mestrado\DeteccaoObj\Anomalias\ndvi.tif"
output_dir = r"D:\Mestrado\DeteccaoObj\Anomalias\result"

window_size = 5
iqr_factor = 1.5

os.makedirs(output_dir, exist_ok=True)

# ==========================================================
# LEITURA DO RASTER
# ==========================================================

with rasterio.open(raster_path) as src:

    ndvi = src.read(1).astype(np.float32)

    profile = src.profile.copy()

    nodata = src.nodata

if nodata is not None:
    ndvi[ndvi == nodata] = np.nan

# ==========================================================
# MÉDIA DOS VIZINHOS
# ==========================================================

def local_mean(window):

    center = len(window) // 2

    neighbors = np.delete(window, center)

    neighbors = neighbors[~np.isnan(neighbors)]

    if len(neighbors) == 0:
        return np.nan

    return np.mean(neighbors)

print("Calculando média local 5x5...")

mean_local = generic_filter(
    ndvi,
    local_mean,
    size=window_size,
    mode="nearest"
)


# ==========================================================
# Calculo do erro
# ==========================================================

print("Calculando erro normalizado...")

erro = (ndvi - mean_local) ** 2

print("Erro mínimo:", np.nanmin(erro))
print("Erro máximo:", np.nanmax(erro))
print("Erro médio:", np.nanmean(erro))

erro_normalizado = (
    (erro - np.nanmin(erro))
    /
    (np.nanmax(erro) - np.nanmin(erro))
) * 100

erro_normalizado[np.isnan(ndvi)] = np.nan


# ==========================================================
# IQR
# ==========================================================

valid = erro_normalizado[~np.isnan(erro_normalizado)]

Q1 = np.percentile(valid, 25)
Q3 = np.percentile(valid, 75)

IQR = Q3 - Q1

upper_limit = Q3 + iqr_factor * IQR

print(f"Q1 = {Q1}")
print(f"Q3 = {Q3}")
print(f"IQR = {IQR}")
print(f"Limite = {upper_limit}")

# ==========================================================
# ANOMALIAS
# ==========================================================

anomalies = np.where(erro_normalizado > upper_limit, 1, 0)

# =====================================================
# REMOVER REGIÕES PEQUENAS
# =====================================================

min_pixels = 25

labeled, num_features = label(anomalies)

sizes = np.bincount(labeled.ravel())

remove_mask = sizes < min_pixels

remove_mask[0] = False

anomalies_clean = anomalies.copy()

anomalies_clean[remove_mask[labeled]] = 0

anomalies = anomalies_clean

print(f"Regiões encontradas: {num_features}")
print(f"Tamanho mínimo: {min_pixels} pixels")

# ==========================================================
# ESTATÍSTICAS
# ==========================================================

total_pixels = np.sum(~np.isnan(ndvi))

anomaly_pixels = np.sum(anomalies == 1)

percentage = anomaly_pixels / total_pixels * 100

std_gli = np.nanstd(ndvi)

print("\n===== RESULTADOS =====")
print(f"Desvio padrão GLI: {std_gli:.6f}")
print(f"Pixels totais: {total_pixels}")
print(f"Pixels anômalos: {anomaly_pixels}")
print(f"% anomalias: {percentage:.2f}")

# ==========================================================
# EXPORTAR O ERRO NORMALIZADO
# ==========================================================

profile.update(
    dtype=rasterio.float32,
    count=1,
    compress='lzw',
    nodata=-9999
)

z_export = np.where(
    np.isnan(erro_normalizado),
    -9999,
    erro_normalizado
).astype(np.float32)

z_path = os.path.join(
    output_dir,
    "erro_normalizado.tif"
)

with rasterio.open(z_path, "w", **profile) as dst:
    dst.write(z_export, 1)

# ==========================================================
# EXPORTAR ANOMALIAS
# ==========================================================

profile.update(
    dtype=rasterio.uint8,
    nodata=255
)

anom_export = np.where(
    np.isnan(ndvi),
    255,
    anomalies
).astype(np.uint8)

anom_path = os.path.join(
    output_dir,
    "anomalias.tif"
)

with rasterio.open(anom_path, "w", **profile) as dst:
    dst.write(anom_export, 1)

# ==========================================================
# RELATÓRIO
# ==========================================================

report_path = os.path.join(
    output_dir,
    "estatisticas.txt"
)

with open(report_path, "w", encoding="utf-8") as f:

    f.write("DETECÇÃO DE ANOMALIAS\n")
    f.write("=====================\n\n")

    f.write(f"Janela: {window_size}x{window_size}\n")
    f.write(f"Q1: {Q1}\n")
    f.write(f"Q3: {Q3}\n")
    f.write(f"IQR: {IQR}\n")
    f.write(f"Limite: {upper_limit}\n\n")

    f.write(f"Desvio padrão GLI: {std_gli}\n")
    f.write(f"Pixels totais: {total_pixels}\n")
    f.write(f"Pixels anômalos: {anomaly_pixels}\n")
    f.write(f"% anomalias: {percentage:.2f}\n")

print("\nProcessamento concluído!")
print(f"Resultados salvos em: {output_dir}")