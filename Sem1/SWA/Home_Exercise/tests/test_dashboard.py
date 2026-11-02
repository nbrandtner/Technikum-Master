"""Exercise the actual Streamlit controls using genuine saved experiment evidence."""
import pytest
from streamlit.testing.v1 import AppTest

from earlybird.data import ROOT


def test_all_views_and_scenario_controls_render_without_exceptions():
    if not (ROOT / "experiments" / "latest.json").exists():
        pytest.skip("Run the genuine database experiment first")
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    assert not app.exception
    assert app.selectbox[1].value == 7
    app.selectbox[1].set_value(2).run()
    assert not app.exception
    app.selectbox[1].set_value(7).run()
    assert not app.exception
    for view in ["Stability", "Inspect", "Challenge", "Sources", "Discover"]:
        app.radio[0].set_value(view).run()
        assert not app.exception, f"Failed view: {view}"
        if view == "Challenge":
            for scenario in app.selectbox[0].options:
                app.selectbox[0].select(scenario).run()
                assert not app.exception
                app.slider[0].set_value(3).run()
                assert not app.exception
        if view == "Sources":
            app.text_input[0].set_value("R43").run()
            assert not app.exception
            assert any("R43" in item.label for item in app.expander)
