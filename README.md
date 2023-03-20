# OpenAI Embeddings for Procore Help Docs

This Python project scrapes Procore's help docs and runs each help doc through the OpenAI embeddings model. The output csv file contains the title, content, url, and embeddings value.

## Setup

1. Clone the repository:
  ```shell
  git clone https://github.com/frankolson/procore-help-docs-embeddings.git
  ```
2. Install the project dependencies with Poetry:
  ```shell
  poetry install
  ```
3. Ensure that you have an OpenAI API key stored in a `OPENAI_API_KEY` variable.
4. Also, OpenAI has a rate limitter of 60 req/sec, so this project handles this (ineloquently) by just adding a `time.wait(1)` call for each embedding. This means you need to make sure your replit is configured to stay awake, because the code will take 13+ minutes to run. You can find instructions for that here: https://docs.replit.com/hosting/enabling-always-on.

## Quirks

Procore uses a service to host help docs that uses JavaScript actions to load tabs and tab content asynchronously. So I used Chrome's inspector to manually grab the HTML returned from that async call and saved it to a variable in the `vardata.py` file. If you want to use the most up to date help docs, you will have to repeat that process and replace the contents of the `source_html` in the `vardata.py` file.

In the future this could be automated by hooking up the helpdocs hosting service to sync up with a vector storage system like [Pinecone](https://www.pinecone.io/) or [Weaviate](https://weaviate.io/).

## Running

To run, uncomment out lines 5 and 6 in `main.py` and run the replit. It can be run manually in a shell with the following:

```shell
python3 main.py
```

Those lines were commented out so they don't get automatically run (they are long-running processes) by Replit's REPL system.