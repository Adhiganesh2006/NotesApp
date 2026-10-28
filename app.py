from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

notes = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Notes App - V2</title>

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

        .version {
            text-align: center;
            color: #555;
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
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            background: #2563eb;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .edit-btn {
            background: #16a34a;
        }

        .edit-btn:hover {
            background: #15803d;
        }

        .note h3 {
            margin-bottom: 5px;
        }

        .note {
            border-left: 5px solid #2563eb;
        }
    </style>
</head>

<body>

    <h1>Notes App</h1>

    <p class="version">Version 2 - Add and Edit Notes</p>

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

            <h4>Edit Note</h4>

            <form method="POST" action="/edit/{{ note.id }}">

                <input
                    type="text"
                    name="title"
                    value="{{ note.title }}"
                    required
                >

                <textarea
                    name="content"
                    required
                >{{ note.content }}</textarea>

                <button
                    type="submit"
                    class="edit-btn"
                >
                    Save Changes
                </button>

            </form>

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
        version="V2"
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


@app.route("/edit/<int:note_id>", methods=["POST"])
def edit_note(note_id):

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        return "Title and content are required.", 400

    for note in notes:

        if note["id"] == note_id:

            note["title"] = title
            note["content"] = content

            return redirect("/")

    return "Note not found.", 404


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)