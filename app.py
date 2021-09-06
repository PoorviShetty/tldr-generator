from flask import Flask, request, render_template, flash, redirect, url_for
from collections import Counter
import spacy

app = Flask(__name__)
app.secret_key = "super secret key"
nlp = spacy.load('en_core_web_sm')


def smmry(text):
    # 1) Associate words with their grammatical counterparts. (e.g. “city” and “cities”)

    # 2) Calculate the occurrence of each word in the text.
    # 3) Assign each word with points depending on their popularity.
    freq = Counter(text.split())

    # 4) Detect which periods represent the end of a sentence. (e.g “Mr.” does not).
    # 5) Split up the text into individual sentences.
    sentences = [i for i in nlp(text).sents]

    # 6) Rank sentences by the sum of their words’ points.
    points = {}
    for i in sentences:
        score = 0
        for j in i:
            score += freq[str(j)]
        points[i] = score
    #print(points, flush=True)
    ranked = dict(
        sorted(points.items(), key=lambda item: item[1], reverse=True))

    # 7) Return X of the most highly ranked sentences in chronological order.
    index = list()
    if len(sentences) > 5:
        for i in range(5):
            index.append(sentences.index(list(ranked)[i]))
    else:
        for i in range(len(sentences)):
            index.append(sentences.index(list(ranked)[i]))

    result = list()
    for i in sorted(index):
        result.append(str(sentences[i]))

    return (" ".join(result))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input = (request.form['input'])
        output = smmry(input)
        flash(input, 'input')
        flash(output, 'output')
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
