from streamlit.components.v1 import html

def switch_tab(tab_text):
    html(f"""<script>
    (() => {{
        const tabGroup = window.parent.document.querySelector(".stTabs");
        if (!tabGroup) {{
            console.log("Tab group not found");
            return;
        }}
        
        const tabButton = [...tabGroup.querySelectorAll("button")].find(button => {{
            return button.innerText.includes("{tab_text}");
        }});
        
        if(tabButton) {{
            tabButton.click();
        }} else {{
            console.log("Tab button '{tab_text}' not found");
        }}
    }})();
    </script>""", height=0)