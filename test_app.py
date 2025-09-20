import pytest

def test_header_is_present(dash_duo):
    from app import app
    dash_duo.start_server(app)

    # Header exists
    header = dash_duo.find_element("h1")
    assert "Soul Foods" in header.text


def test_graph_is_present(dash_duo):
    from app import app
    dash_duo.start_server(app)

    # Graph exists
    graph = dash_duo.find_element("#sales-time-chart")
    assert graph is not None


def test_region_picker_is_present(dash_duo):
    from app import app
    dash_duo.start_server(app)

    # Dropdown exists
    dropdown = dash_duo.find_element("#region-dropdown")
    assert dropdown is not None
