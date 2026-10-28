from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

notes = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Notes App - V3</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 750px;
            margin: 40px auto;
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
            box-shadow: 0 2px 5px #ddd;
        }

        input, textarea {
            box-sizing: border-box;
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
        }

        textarea {
            min-height: 80px;
            resize: vertical;
        }

        button {
            background: #2563eb;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 5px;
        }

        button:hover {
            opacity: 0.85;
        }

        .edit-btn {
            background: #16a34a;
        }

        .delete-btn {
            background: #dc2626;
        }

        .note {
            border-left: 5px solid #2563eb;
        }

        .note h3 {
            margin-bottom: 8px;
        }

        .note-content {
            white-space: pre-wrap;
            overflow-wrap: anywhere;
        }

        .empty {
            text-align: center;
            color: #777;
        }
    </style>
</head>

<body>

    <h1>Notes App</h1>

    <p class="version">
        Version 3 - Add, Edit and Delete Notes
    </p>

    <form method="POST" action="/add">
        <h2>Create a Note</h2>

        <input
            type="text"
            name="title"
            placeholder="Enter note title"
            maxlength="150"
            required
        >

        <textarea
            name="content"
            placeholder="Enter note content"
            required
        ></textarea>

        <button type="submit">Add Note</button>
    </form>

    <h2>Saved Notes ({{ notes|length }})</h2>

    {% for note in notes %}

        <div class="note">

            <h3>{{ note.title }}</h3>

            <p class="note-content">{{ note.content }}</p>

            <small>Note ID: {{ note.id }}</small>

            <form method="POST" action="/edit/{{ note.id }}">

                <h4>Edit Note</h4>

                <input
                    type="text"
                    name="title"
                    value="{{ note.title }}"
                    maxlength="150"
                    required
                >

                <textarea
                    name="content"
                    required
                >{{ note.content }}</textarea>

                <button type="submit" class="edit-btn">
                    Save Changes
                </button>

            </form>

            <form
                method="POST"
                action="/delete/{{ note.id }}"
                onsubmit="return confirm('Are you sure you want to delete this note?');"
            >

                <button type="submit" class="delete-btn">
                    Delete Note
                </button>

            </form>

        </div>

    {% else %}

        <p class="empty">No notes available. Create your first note above.</p>

    {% endfor %}

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        notes=notes
    )


@app.route("/add", methods=["POST"])
def add_note():
    global next_id

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        return "Title and content are required.", 400

    if len(title) > 150:
        return "Title must not exceed 150 characters.", 400

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

    if len(title) > 150:
        return "Title must not exceed 150 characters.", 400

    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["content"] = content

            return redirect("/")

    return "Note not found.", 404


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(index)
            return redirect("/")

    return "Note not found.", 404


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)