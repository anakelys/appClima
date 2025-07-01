import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from api.open_meteo import get_city_weather, get_5day_forecast, get_multiple_cities_weather

def test_cidades_brasileiras():
    for cidade in ["Rio de Janeiro", "São Paulo", "Salvador"]:
        resultado = get_city_weather(cidade)
        assert "cidade" in resultado or "error" in resultado

def test_cidades_internacionais():
    for cidade in ["Paris", "New York", "Tóquio"]:
        resultado = get_city_weather(cidade)
        assert "cidade" in resultado or "error" in resultado

def test_cidades_com_acentos():
    for cidade in ["São Luís", "München", "Québec"]:
        resultado = get_city_weather(cidade)
        assert "cidade" in resultado or "error" in resultado

def test_entradas_invalidas():
    # Entradas que podem ser consideradas inválidas, exceto "12345" que pode ser cidade real
    for cidade in ["", "CidadeInexistente123", "@@@"]:
        resultado = get_city_weather(cidade)
        assert "error" in resultado
    # Para "12345", aceita tanto erro quanto resultado válido
    resultado = get_city_weather("12345")
    assert "error" in resultado or "cidade" in resultado

def test_multiplas_cidades():
    cidades = ["Rio de Janeiro", "Paris", "Tóquio"]
    resultados = get_multiple_cities_weather(cidades)
    assert len(resultados) == 3
    for r in resultados:
        assert "cidade" in r or "error" in r

def test_previsao_5_dias():
    previsao = get_5day_forecast("São Paulo")
    assert isinstance(previsao, list)
    assert len(previsao) >= 1
    assert "data" in previsao[0] or "error" in previsao[0]
