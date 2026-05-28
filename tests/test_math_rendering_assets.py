from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def normalize_latex_delimiters(markdown: str) -> str:
    text = str(markdown or "")
    text = re.sub(r"\\\[([\s\S]*?)\\\]", lambda m: f"$${m.group(1)}$$", text)
    text = re.sub(r"\\\(([\s\S]*?)\\\)", lambda m: f"${m.group(1)}$", text)
    return text


def test_katex_assets_have_dedicated_ready_event():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    plugin_js = (ROOT / "app" / "docsify-plugin.js").read_text(encoding="utf-8")

    math_event_index = index_html.index("dpr-math-assets-ready")
    deferred_event_index = index_html.index("dpr-deferred-assets-ready")
    chat_script_index = index_html.index("app/chat.discussion.js")

    assert math_event_index < chat_script_index
    assert math_event_index < deferred_event_index
    assert "document.addEventListener('dpr-math-assets-ready', refreshPageMathRendering)" in plugin_js


def test_latex_delimiters_normalize_real_summary_shapes():
    source = (
        "估计 \\(q^{(i)}(t)\\) 和 \\(f^{(i)}(x,t)\\)。\n"
        "\\[\n"
        "U_0^{(i)}(t)=k_i u^{(i)}(0,t)\n"
        "\\]\n"
    )

    normalized = normalize_latex_delimiters(source)

    assert "\\(" not in normalized
    assert "\\[" not in normalized
    assert "$q^{(i)}(t)$" in normalized
    assert "$f^{(i)}(x,t)$" in normalized
    assert "$$\nU_0^{(i)}(t)=k_i u^{(i)}(0,t)\n$$" in normalized
