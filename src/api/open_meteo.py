import requests
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Função auxiliar para geocodificar o nome da cidade usando Nominatim
# Retorna (latitude, longitude, nome completo) ou None se não encontrar

def _geocode_city(city_name):
    geo_url = "https://nominatim.openstreetmap.org/search"
    geo_params = {"q": city_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "appClima/1.0 (seu-email@exemplo.com)"}
    resp = requests.get(geo_url, params=geo_params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]

# Busca dados atuais do clima para uma cidade
# Retorna dict com cidade, temperatura, umidade, vento, precipitação e código do clima, ou erro

def get_city_weather(city_name):
    """
    Busca os dados atuais do clima para uma cidade informada.
    Retorna dict com cidade, temperatura, umidade, vento, precipitação e código do clima, ou erro.
    """
    try:
        geo = _geocode_city(city_name)
        if not geo:
            return {"error": "Cidade não encontrada."}
        lat, lon, cidade = geo
        # Consulta a API Open-Meteo
        meteo_url = "https://api.open-meteo.com/v1/forecast"
        meteo_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "relative_humidity_2m,precipitation"
        }
        meteo_response = requests.get(meteo_url, params=meteo_params, timeout=10)
        meteo_response.raise_for_status()
        meteo_data = meteo_response.json()
        if "current_weather" not in meteo_data:
            return {"error": "Dados de clima não encontrados."}
        current = meteo_data["current_weather"]
        umidade = precipitacao = None
        # Busca umidade e precipitação para o horário mais próximo
        if "hourly" in meteo_data and "time" in meteo_data["hourly"]:
            now = current.get("time")
            if now and now in meteo_data["hourly"]["time"]:
                idx = meteo_data["hourly"]["time"].index(now)
                umidade = meteo_data["hourly"].get("relative_humidity_2m", [None])[idx]
                precipitacao = meteo_data["hourly"].get("precipitation", [None])[idx]
        return {
            "cidade": cidade,
            "temperatura_celsius": current.get("temperature"),
            "umidade": umidade,
            "vento_kmh": current.get("windspeed"),
            "precipitacao": precipitacao,
            "descricao": current.get("weathercode", "Sem descrição")
        }
    except requests.RequestException:
        return {"error": "Erro de rede ou falha na API."}
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}

# Busca previsão de 5 dias para uma cidade
# Retorna lista de dicts com data, temp_max, temp_min e código do clima, ou erro

def get_5day_forecast(city_name):
    try:
        geo = _geocode_city(city_name)
        if not geo:
            return [{"error": "Cidade não encontrada."}]
        lat, lon, _ = geo
        meteo_url = "https://api.open-meteo.com/v1/forecast"
        meteo_params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "timezone": "auto"
        }
        meteo_response = requests.get(meteo_url, params=meteo_params, timeout=10)
        meteo_response.raise_for_status()
        meteo_data = meteo_response.json()
        if "daily" not in meteo_data:
            return [{"error": "Dados de previsão não encontrados."}]
        dias = meteo_data["daily"]
        previsao = []
        for i in range(min(5, len(dias["time"]))):
            data = datetime.strptime(dias["time"][i], "%Y-%m-%d").strftime("%d/%m/%Y")
            previsao.append({
                "data": data,
                "temp_max": dias["temperature_2m_max"][i],
                "temp_min": dias["temperature_2m_min"][i],
                "descricao": dias["weathercode"][i]
            })
        return previsao
    except Exception as e:
        return [{"error": f"Erro ao buscar previsão: {str(e)}"}]

# Busca clima atual para várias cidades (lista de nomes)
def get_multiple_cities_weather(city_names):
    return [get_city_weather(nome) for nome in city_names]

# Funções de cache para evitar consultas repetidas à API

def get_cache_file():
    # Cria diretório de cache na home do usuário
    cache_dir = Path.home() / '.appclima_cache'
    cache_dir.mkdir(exist_ok=True)
    return str(cache_dir / 'weather_cache.json')

def cache_set(key, value, expire_seconds, cache_file=None):
    if not cache_file:
        cache_file = get_cache_file()
    cache = {}
    # Lê cache existente, se houver
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            try:
                cache = json.load(f)
            except Exception:
                cache = {}
    expire_at = time.time() + expire_seconds
    cache[key] = {'value': value, 'expire_at': expire_at}
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def cache_get(key, cache_file=None):
    if not cache_file:
        cache_file = get_cache_file()
    if not os.path.exists(cache_file):
        return None
    with open(cache_file, 'r') as f:
        try:
            cache = json.load(f)
        except Exception:
            return None
    item = cache.get(key)
    if not item:
        return None
    # Remove do cache se expirado
    if time.time() > item['expire_at']:
        cache.pop(key)
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
        return None
    return item['value']

# Busca clima atual com cache (expiração padrão: 1h)
def get_weather_with_cache(city_name, expire_seconds=3600):
    cache_file = get_cache_file()
    key = city_name.strip().lower()
    cached = cache_get(key, cache_file=cache_file)
    if cached:
        return cached
    resultado = get_city_weather(city_name)
    if 'error' not in resultado:
        cache_set(key, resultado, expire_seconds, cache_file=cache_file)
    return resultado
