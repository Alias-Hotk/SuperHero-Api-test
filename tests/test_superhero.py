import pytest
from superhero import get_tallest_hero


@pytest.fixture
def mock_heroes_data():
    return [
        {"name": "Hero1", "appearance": {"gender": "Male", "height": ["", "180 cm"]},
         "work": {"occupation": "Scientist"}},
        {"name": "Hero2", "appearance": {"gender": "Male", "height": ["", "200 cm"]}, "work": {"occupation": ""}},
        {"name": "Hero3", "appearance": {"gender": "Female", "height": ["", "190 cm"]},
         "work": {"occupation": "Agent"}},
    ]


def test_tallest_hero(mock_heroes_data, mocker):
    """Тест поиска самого высокого героя"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_heroes_data

    assert get_tallest_hero("Male", True)["name"] == "Hero1"
    assert get_tallest_hero("Male", False)["name"] == "Hero2"
    assert get_tallest_hero("Female", True)["name"] == "Hero3"
    assert get_tallest_hero("Female", False) is None


def test_no_heroes_found(mocker):
    """Тест на пустой список героев"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    assert get_tallest_hero("Male", True) is None


def test_invalid_height_format(mocker):
    """Тест на некорректные данные о росте"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "HeroX", "appearance": {"gender": "Male", "height": ["", "unknown"]},
         "work": {"occupation": "Engineer"}}
    ]

    assert get_tallest_hero("Male", True) is None


def test_multiple_tallest_heroes(mocker):
    """Тест на случай, когда есть несколько самых высоких героев"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Hero1", "appearance": {"gender": "Male", "height": ["", "200 cm"]},
         "work": {"occupation": "Scientist"}},
        {"name": "Hero2", "appearance": {"gender": "Male", "height": ["", "200 cm"]}, "work": {"occupation": "Doctor"}},
    ]

    result = get_tallest_hero("Male", True)
    assert result["name"] in ["Hero1", "Hero2"]


def test_case_insensitive_gender(mocker):
    """Тест на ввод пола"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Hero1", "appearance": {"gender": "Male", "height": ["", "180 cm"]},
         "work": {"occupation": "Scientist"}},
    ]

    assert get_tallest_hero("male", True)["name"] == "Hero1"
    assert get_tallest_hero("MALE", True)["name"] == "Hero1"


def test_no_working_heroes(mocker):
    """Тест на случай, когда у всех героев нет работы"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Hero1", "appearance": {"gender": "Male", "height": ["", "190 cm"]}, "work": {"occupation": ""}},
        {"name": "Hero2", "appearance": {"gender": "Male", "height": ["", "200 cm"]}, "work": {"occupation": ""}},
    ]

    assert get_tallest_hero("Male", True) is None

def test_hero_with_no_height(mocker):
    """Тест на случай, когда у героя нет информации о росте"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Hero1", "appearance": {"gender": "Male", "height": [""]}, "work": {"occupation": "Scientist"}},
        {"name": "Hero2", "appearance": {"gender": "Male", "height": ["", "180 cm"]}, "work": {"occupation": "Engineer"}},
    ]
