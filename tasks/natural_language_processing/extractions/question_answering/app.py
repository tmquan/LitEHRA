import os 
import lightning as L
import gradio as gr

from functools import partial
from lightning_app.utilities.state import AppState
from lightning.app.components.serve import ServeGradio

from transformers import (
    AutoConfig, 
    AutoTokenizer, 
    AutoModelForQuestionAnswering, 
)

from lightning_transformers.task.nlp.question_answering import (
    QuestionAnsweringTransformer,
)

class QuestionAnsweringServeGradio(ServeGradio):
    inputs = [
        gr.inputs.Textbox(lines=10, label="Context", placeholder="Type a sentence or paragraph here."), 
        gr.inputs.Textbox(lines=2, label="Question", placeholder="Ask a question based on the context."),
    ]
    outputs = [
        # gr.outputs.Textbox(label="Answer"),
        # gr.outputs.Label(label="Score"),
        gr.JSON(label="JSON"),
    ]
    enable_queue = True
    examples = [
        ["Harry James Potter (DOB: 31 July, 1980) was a half-blood wizard, and one of the most famous wizards of modern times. He was the only child and son of James and Lily Potter, both members of the original Order of the Phoenix. Harry's birth was overshadowed by a prophecy, naming either himself or Neville Longbottom as the one with the power to vanquish Lord Voldemort. After half of the prophecy was reported to Voldemort, courtesy of Severus Snape, Harry was chosen as the target due to his many similarities with the Dark Lord. This caused the Potter family to go into hiding. Voldemort made his first vain attempt to circumvent the prophecy when Harry was a year and three months old. During this attempt he murdered Harry's parents as they tried to protect him, but this unsuccessful attempt to kill Harry led to Voldemort's first downfall. This downfall marked the end of the First Wizarding War, and to Harry henceforth being known as the \"Boy Who Lived\".", 
        "What is the first character's name?"],
        ["Hermione Jean Granger (DOB 19 September, 1979) was an English Muggle-born witch born to Mr and Mrs Granger. At the age of eleven, she learned about her magical nature and was accepted into Hogwarts School of Witchcraft and Wizardry. Hermione began attending Hogwarts in 1991 and was Sorted into Gryffindor House. She possessed a brilliant academic mind and proved to be a gifted student in almost every subject that she studied, to the point where she was nearly made a Ravenclaw by the Sorting Hat.", 
        "What is the first character's gender?"],
    ]
    title = __name__
    description = ""

    def __init__(self, cloud_compute, *args, **kwargs):
        super().__init__(*args, cloud_compute=cloud_compute, **kwargs)
        self.ready = False  # required

    # # Override original implementation to pass the custom css highlightedtext
    # def run(self, *args, **kwargs):
    #     if self._model is None:
    #         self._model = self.build_model()

    #     fn = partial(self.predict, *args, **kwargs)
    #     fn.__name__ = self.predict.__name__
    #     gr.Interface(
    #         fn=fn, 
    #         css="#htext span {white-space: pre-wrap; word-wrap: normal}", # Override here
    #         inputs=self.inputs, 
    #         outputs=self.outputs, 
    #         examples=self.examples
    #     ).launch(
    #         server_name=self.host,
    #         server_port=self.port,
    #         enable_queue=self.enable_queue,
    #     )

    def build_model(self, pretrained_model_name_or_path="deepset/roberta-base-squad2"):
        model = QuestionAnsweringTransformer(
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            tokenizer=AutoTokenizer.from_pretrained(pretrained_model_name_or_path=pretrained_model_name_or_path),
        )
        return model
        
    def predict(self, contexts, questions):
        return self._model.hf_predict(dict(context=contexts, question=questions))
        

class LitRootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.qas = QuestionAnsweringServeGradio(L.CloudCompute("cpu"))

    def configure_layout(self):
        tabs = []
        tabs.append({"name": "Question Answering", "content": self.qas})
        return tabs

    def run(self):
        self.qas.run()
    
app = L.LightningApp(LitRootFlow())