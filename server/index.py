import flask
from flask import request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import markdown
from bs4 import BeautifulSoup
import openai
import os
import time
import requests
import tiktoken

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["500 per day"]
)

app = flask.Flask(__name__)
limiter.init_app(app)
CORS(app)

glossary = open('./training-data/docs/Farmers-Almanac/protocol/glossary.md', 'r').read()
additional_glossary = [{'word': 'yield', 'line': 'Volatility and yield are baked into the Bean token itself—when the Bean price is too high, Beanstalk mints new Beans and distributes them to various ecosystem participants in a deterministic fashion. This seigniorage is the positive carry that the Beanstalk economy is based on.'}]

def md_to_text(md):
    """
    Convert markdown to text
    """
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()

def process_glossary(str):
    result = str.split("###")

    for index, line in enumerate(result):
        if len(line) == 0:
            continue

        chunk = line.split("\n")

        title = md_to_text(chunk[0])
        processed_line = md_to_text(chunk[2])

        result[index] = {
            "word": title,
            "line": processed_line
        }

    return result[1:] # first result is empty line


def get_acronym(str):
    if "(" in str:
        return str.split("(")[1].split(")")[0]
    return None


def get_glossary_context(str):
    str = str.lower()
    contexts = []

    for definition in glossary:
        word = definition['word'].lower()
        acronym = get_acronym(word)

        if acronym:
            word = word.replace(f"({acronym})", "")

        if word.strip() in str or (acronym and acronym in str):
            contexts.append(f"{definition['word']}: {definition['line']}")

    return "\n".join(contexts)


def get_gpt_answer(prompt, max_tokens):
    max_retries = 3
    retries = 0
    wait_time = 2  # initial wait time in seconds
    while retries < max_retries:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.0,
            )
            return response.choices[0].text
        except Exception as e:
            retries += 1
            print(f"Error: {str(e)}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2  # exponential back-off
    raise Exception(f"Failed after {max_retries} retries.")


def get_doc_for_question_helper(question, doc):
    with open(doc, "r") as f:
        lookup = f.read()
    prompt = f"""Instructions: You are tasked with selecting the correct document relevant to answering a question.
Pick the document that most closely matches the question by matching words in the question to the document keywords.
The list is formatted as title: keywords.
If the question is about:
- price, the document is 15.
- seeds or stalk, the document is 3 or 14.
- general info, the document is 13.
Documents:
{lookup}
Question: {question}
Document number to read:"""
    answer = get_gpt_answer(prompt, 1).strip()
    return answer


def get_doc_line(line_number):
    with open("lookup1.txt", "r") as f:
        lookup1 = f.read().split('\n')
    with open("lookup2.txt", "r") as f:
        lookup2 = f.read().split('\n')

    lines = lookup1 + lookup2

    return lines[line_number-1]


def get_doc_number_for_question(question):
    if 'audit' in question.lower():
        return '22'
    doc1 = get_doc_for_question_helper(question, "lookup1.txt")
    doc2 = get_doc_for_question_helper(question, "lookup2.txt")

    # Handle none being returned
    try:
        doc1_line = get_doc_line(int(doc1))
    except ValueError:
        return doc2.strip()

    try:
        doc2_line = get_doc_line(int(doc2))
    except ValueError:
        return doc1.strip()

    lookup = f'{doc1_line}\n{doc2_line}'
    print(f'Deciding between the following 2 documents:\n{doc1_line}\n{doc2_line}')

    prompt = f"""Instructions: You are tasked with selecting the correct document relevant to answering a question. Try to match words in the question to the document keywords.
    Documents:
    {lookup}
    Question: {question}
    Document number to read:"""
    return get_gpt_answer(prompt, 1).strip()


def get_doc(doc_number):
    """
    Use the doc_number to get the document from the lookup-paths.txt file
    """
    with open("lookup-paths.txt") as f:
        doc_path = f.read().split('\n')[doc_number-1]
    print(f'Reading document from {doc_path}...')

    source = doc_path.split('/')[4:]
    source = 'https://raw.githubusercontent.com/BeanstalkFarms/Farmers-Almanac/master/' + '/'.join(source)
    doc = requests.get(source).text

    return md_to_text(doc), doc_path


def split_lookup():
    """
    Split lookup.txt into 2 files for GPT-3 to read (Due to 4k token limitation)
    """
    with open("lookup.txt", "r") as f:
        lookup = f.read()

    lines = lookup.split('\n')
    lines = [l for l in lines if len(l) > 0]

    for i, l in enumerate(lines):
        line_without_number = l.split(':', 1)[1]
        line_with_number = f"{i+1}: {line_without_number}"
        lines[i] = line_with_number

    lookup1 = lines[:len(lines)//2]
    lookup2 = lines[len(lines)//2:]

    with open("lookup1.txt", "w") as f:
        f.write('\n'.join(lookup1))

    with open("lookup2.txt", "w") as f:
        f.write('\n'.join(lookup2))


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_formatted_prompt(question, history, glossary_context, doc_context):
    return f"""Instructions: You are a chat bot. Answer only questions about Beanstalk as truthfully as possible using the provided text, and if the answer is not contained within the text below, say "I'm not sure". Otherwise, chat freely.

Context:
{glossary_context}
{doc_context}
History: {history}
Question: {question}
Answer:"""

def get_answer_with_context(question, history, glossary_context, doc_context):
    prompt = get_formatted_prompt(question, history, glossary_context, doc_context)
    num_tokens = num_tokens_from_string(prompt, "p50k_base")
    print(f'Num tokens: {num_tokens}')
    # truncate prompt correctly as needed
    if num_tokens > 3500:
        num_token_excess = num_tokens - 3500
        doc_context_num_tokens = num_tokens_from_string(doc_context, "p50k_base")
        max_doc_context_len = int((1 - num_token_excess / doc_context_num_tokens) * len(doc_context))
        doc_context = doc_context[:max_doc_context_len]
        prompt = get_formatted_prompt(question, history, glossary_context, doc_context)
        print(f'Truncated query. New num tokens: {num_tokens_from_string(prompt, "p50k_base")}')

    return get_gpt_answer(prompt, 500).strip()

def answer_question(question, history):
    start = time.time()
    doc_number = get_doc_number_for_question(question)
    print(f'Took {time.time()-start} seconds to get doc number')
    print(f'Chose document number {doc_number}')

    portion_time = time.time()
    try:
        doc_context, doc_path = get_doc(int(doc_number))
    except ValueError:
        # could not get a document relevant to query
        doc_context = get_doc(13)
        doc_path = './training-data/docs/Farmers-Almanac/introduction/why-beanstalk.md'
    print(f'Took {time.time()-portion_time} seconds to get document')

    glossary_context = get_glossary_context(question+' '+history[-1000:])

    portion_time = time.time()
    answer = get_answer_with_context(question, history, glossary_context, doc_context)
    print(f'Took {time.time()-portion_time} seconds to get answer.')
    end = time.time()
    print(f"Time taken: {end-start} seconds")
    return answer, doc_path

@app.route('/ask', methods=['GET'])
@limiter.limit("30 per minute")
def ask():
  history = request.args.get('history')
  query = request.args.get('query')

  num_tokens_in_query = num_tokens_from_string(query, "p50k_base")
  if num_tokens_in_query > 250:
    return jsonify({
      'answer': 'Please shorten your question.'
    })

  print(f'Question: {query}')
  answer, doc_path = answer_question(query, history)
  print('\n\n\n\n\n')

  source = doc_path.replace('README.md', '').replace('.md', '').split('/')[4:]
  source = 'https://docs.bean.money/almanac/' + '/'.join(source)

  return jsonify({
    'answer': answer,
    'source': source,
  })

def create_app():
  return app

split_lookup()
glossary = process_glossary(glossary)
glossary = glossary + additional_glossary