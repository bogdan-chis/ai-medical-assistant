import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000/rag"

# In-memory chat history
messages = []
def add_message(role, text):
    messages.append({"role": role, "text": text})

def chat_interface(user_input, name, age, gender, uploaded_file):
    if not user_input:
        return ""

    # match your RAGRequest schema exactly
    payload = {"query": user_input, "chunks": []}

    # call FastAPI
    resp = requests.post(BACKEND_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()

    answer = data.get("answer", "")

    add_message("user", user_input)
    add_message("assistant", answer)

    return "\n".join(
        f"{'🧑‍⚕ You' if m['role']=="user" else '🤖 Assistant'}: {m['text']}"
        for m in messages
    )

with gr.Blocks(title="🩺 AI Medical Assistant") as app:
    gr.Markdown("# 🩺 AI Medical Assistant")
    gr.Markdown("Describe your symptoms and let the assistant help you understand possible conditions or next steps.")

    with gr.Row():
        with gr.Column(scale=3):
            user_input    = gr.Textbox(label="Enter your symptoms or a medical question:", lines=5)
            name_input    = gr.Textbox(label="Patient Name")
            age_input     = gr.Number(label="Patient Age", value=30)
            gender_input  = gr.Dropdown(label="Patient Gender", choices=["Male","Female","Other"], value="Other")
            uploaded_file = gr.File(label="Upload any relevant file (optional)")
            submit_btn    = gr.Button("Ask")
            chat_history  = gr.Textbox(label="🧠 Chat History", interactive=False, lines=15)

            gr.Markdown("---")
            gr.Markdown("⚠ *Disclaimer*: This assistant is for informational purposes only and does not provide medical advice. Always consult a licensed physician.")

    submit_btn.click(
        fn=chat_interface,
        inputs=[user_input, name_input, age_input, gender_input, uploaded_file],
        outputs=[chat_history]
    )

if __name__ == "__main__":
    app.launch(share=True)