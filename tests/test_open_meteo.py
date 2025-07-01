import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from api.open_meteo import get_city_weather
from unittest.mock import patch


def test_get_city_weather_sucesso():
    resultado = get_city_weather("Rio de Janeiro")
    assert "cidade" in resultado
    assert "temperatura_celsius" in resultado
    assert "descricao" in resultado
    assert resultado["cidade"].lower().startswith("rio de janeiro")
    assert isinstance(resultado["temperatura_celsius"], (int, float))


def test_get_city_weather_cidade_invalida():
    resultado = get_city_weather("CidadeInexistenteParaTeste123456")
    assert "error" in resultado
    assert resultado["error"] == "Cidade não encontrada."


def test_get_city_weather_entrada_vazia():
    resultado = get_city_weather("")
    assert "error" in resultado


def test_get_city_weather_nome_com_acentos():
    resultado = get_city_weather("São Paulo")
    assert "cidade" in resultado or "error" in resultado


def test_get_city_weather_nome_numerico():
    resultado = get_city_weather("12345")
    # Aceita tanto erro quanto resultado válido, pois a API pode retornar cidades para números
    assert "cidade" in resultado or "error" in resultado


def test_get_city_weather_nome_com_caracteres_especiais():
    resultado = get_city_weather("@@@!!!")
    assert "error" in resultado


def test_get_city_weather_nome_longo():
    nome_longo = "Cidade" * 50
    resultado = get_city_weather(nome_longo)
    assert "error" in resultado

# Simula erro de rede
@patch('api.open_meteo.requests.get', side_effect=Exception('Erro de rede simulado'))
def test_get_city_weather_erro_de_rede(mock_get):
    resultado = get_city_weather("Rio de Janeiro")
    assert "error" in resultado
    assert "Erro inesperado" in resultado["error"] or "Erro de rede" in resultado["error"]

# Simula resposta inesperada da API
@patch('api.open_meteo.requests.get')
def test_get_city_weather_resposta_inesperada(mock_get):
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return {"foo": "bar"}
    mock_get.return_value = MockResponse()
    resultado = get_city_weather("Rio de Janeiro")
    assert "error" in resultado

# Simula limite de requisições excedido (HTTP 429)
@patch('api.open_meteo.requests.get')
def test_get_city_weather_limite_excedido(mock_get):
    class MockResponse:
        def raise_for_status(self):
            raise Exception("429 Too Many Requests")
        def json(self): return {}
    mock_get.return_value = MockResponse()
    resultado = get_city_weather("Rio de Janeiro")
    assert "error" in resultado


def test_get_city_weather_docstring_exemplo():
    """
    Testa o exemplo de uso fornecido na docstring da função get_city_weather.
    Garante que o retorno segue o formato documentado.
    """
    resultado = get_city_weather('Rio de Janeiro')
    if 'error' in resultado:
        assert isinstance(resultado['error'], str)
    else:
        assert 'cidade' in resultado
        assert 'temperatura_celsius' in resultado
        assert 'descricao' in resultado
        assert isinstance(resultado['cidade'], str)
        assert isinstance(resultado['temperatura_celsius'], (int, float))
