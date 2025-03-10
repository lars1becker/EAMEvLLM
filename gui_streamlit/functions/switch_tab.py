from streamlit.components.v1 import html

def switch_tab(tab):
    html(f"""<script>
    (() => {{
        var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
        var tab = tabGroup.getElementsByTagName("button")
        tab[{tab}].click()

    }})();
    </script>""", height=0)