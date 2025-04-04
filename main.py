from openai import OpenAI
import crawl_the_site
import create_database

api_key = "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"

start = input("enter the documentation link : ")
limit = int(input("enter the limit for crawling (how many links before stopping) : "))

print("")
txt = crawl_the_site.crawl(start,limit)
collection = create_database.create_database(txt)

openai_client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api_key)

prompt_template = """Answer the question based only on the information provided below.Instead of directing the user to resources, answer the user using the content of the resources.And dont say anything like "Based on the provided information" etc. in the answer.Provide examples based on the users question.For example, when he says "how do i create a slash command" , provide him with an example.
## Information : 
{}

## Question : 
# {}"""

while True:
    q = input("prompt : ")

    results = collection.query(query_texts=[q],n_results=10)
    infos = results["documents"][0]

    info_text = ""
    for info in infos:
        info_text += info + "\n---\n"
    info_text = info_text.strip()

    prompt = prompt_template.format(info_text,q)

    completion = openai_client.chat.completions.create(
    extra_headers={},
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[{"role":"user","content":prompt}])

    print((completion.choices[0].message.content)[7:-1])
