from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

notes = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Notes App - V1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 50px auto;
            background: #f4f6f9;
            padding: 20px;
        }

        h1 {
            color: #2563eb;
            text-align: center;
        }

        form, .note {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
        }

        input, textarea {
            width: 95%;
            padding: 10px;
            margin: 8px 0;
        }

        button {
            background: #2563eb;
            color: white;
            padding: 10px 18px;
            border: none;
            cursor: pointer;
        }

        .note h3 {
            margin-bottom: 5px;
        }
    </style>
</head>

<body>
    <h1>Notes App</h1>
    <p style="text-align:center">Version {{ version }}</p>

    <form method="POST" action="/add">
        <h2>Add a Note</h2>

        <input
            type="text"
            name="title"
            placeholder="Enter note title"
            required
        >

        <textarea
            name="content"
            placeholder="Enter note content"
            required
        ></textarea>

        <button type="submit">Add Note</button>
    </form>

    <h2>Saved Notes</h2>

    {% for note in notes %}
        <div class="note">
            <h3>{{ note.title }}</h3>
            <p>{{ note.content }}</p>
            <small>Note ID: {{ note.id }}</small>
        </div>
    {% else %}
        <p>No notes available.</p>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        notes=notes,
        version=app.config.get("APP_VERSION", "V1")
    )


@app.route("/add", methods=["POST"])
def add_note():
    global next_id

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if title and content:
        notes.append({
            "id": next_id,
            "title": title,
            "content": content
        })
        next_id += 1

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)