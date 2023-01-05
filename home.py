# home.py
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
    st.sidebar.title("Navigation")
    for domain in listings["dirs"]:
        st.sidebar.header("\t"+domain["root"].replace("_", " ").upper())
        for task in domain["dirs"]:
            # st.sidebar.subheader("\t\t"+task["root"].replace("_", " ").upper())
            st.sidebar.expander("\t\t"+task["root"].replace("_", " ").upper()):
                for subtask in task["dirs"]:
                    st.sidebar.caption("\t\t\t"+subtask["root"].replace("_", " ").upper())
                    if subtask["files"] is not None:
                        from tasks.natural_language_processing.extractions.question_answering.app import app
                        app()


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