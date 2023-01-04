# app.py
import lightning as L
import lightning.app.frontend as frontend
import streamlit as st

def hello_world_streamlit_app(lightning_app_state):
    st.write('Hello World')

class LitStreamlit(L.LightningFlow):
    def configure_layout(self):
        return frontend.StreamlitFrontend(render_fn=hello_world_streamlit_app)

class LitApp(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.lit_streamlit = LitStreamlit()

    def run(self):
        self.lit_streamlit.run()

    def configure_layout(self):
        tab1 = {"name": "home", "content": self.lit_streamlit}
        return tab1

app = L.LightningApp(LitApp())