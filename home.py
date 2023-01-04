# app.py
import lightning as L
import lightning.app.frontend as frontend
import streamlit as st

import os
import glob 
import logging

TASK_DIR = "tasks"

def parse_dir(directory):
    parent, folder = os.path.split(directory)
    listings = {
        "root": folder, 
        "dirs": [],
        "files": [],
    }
    children = os.listdir(directory)
    for child in children:
        child_path = os.path.join(directory, child)
        if os.path.isdir(child_path):
            listings['dirs'] += [parse_dir( child_path )] # Recursively parsing
        else:
            listings['files'] += [child]
    return listings


def home_app(lightning_app_state):
    # Glob the tasks
    listings = parse_dir(TASK_DIR)

    # st.sidebar.header("Navigation")
    with st.sidebar:
        st.title("Navigation")
        for domain in listings["dirs"]:
            st.header("\t"+domain["root"].replace("_", " ").upper())
            for task in domain["dirs"]:
                # st.subheader("\t\t"+task["root"].replace("_", " ").upper())
                with st.expander("\t\t"+task["root"].replace("_", " ").upper()):
                    for subtask in task["dirs"]:
                        st.caption("\t\t\t"+subtask["root"].replace("_", " ").upper())


class LitStreamlit(L.LightningFlow):
    def configure_layout(self):
        return frontend.StreamlitFrontend(render_fn=home_app)


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