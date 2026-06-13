import comptext_mcp.server as server


def test_server_exports_main() -> None:
    assert callable(server.main)


def test_tools_exist() -> None:
    for name in [
        "comptext_status",
        "comptext_pack_context",
        "comptext_rust_audit",
        "comptext_replay_digest",
        "comptext_contract_check",
        "comptext_github_pack",
        "comptext_hf_export_pack",
    ]:
        assert hasattr(server, name)
