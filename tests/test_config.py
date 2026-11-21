from rdr2_modmenu.config.loader import load_config


def test_missing_config_returns_defaults(tmp_path):
    cfg = load_config(tmp_path / "nope.toml")
    assert cfg.process_name == "RDR2.exe"
    assert cfg.game_build == "1491.50"