# LLM

## AGI

- transformers cannot be used in AGI because it cannot learn and infer new tokens from unseen data. It generalize better from large datasets, and cannot generalize far from unexplored data.

## Prompting

| #Principle | Prompt Principle for Instructions |
|------------|-----------------------------------|
| 1          | If you prefer more concise answers, no need to be polite with LLM so there is no need to add phrases like "please", "if you don't mind", "thank you", "I would like to", etc., and get straight to the point. |
| 2          | Integrate the intended audience in the prompt, e.g., the audience is an expert in the field. |
| 3          | Break down complex tasks into a sequence of simpler prompts in an interactive conversation. |
| 4          | Employ affirmative directives such as 'do', while steering clear of negative language like 'don't'. |
| 5          | When you need clarity or a deeper understanding of a topic, idea, or any piece of information, utilize the following prompts: |
|            | o Explain [insert specific topic] in simple terms. |
|            | o Explain to me like I'm 11 years old. |
|            | o Explain to me as if I'm a beginner in [field]. |
|            | o Write the [essay/text/paragraph] using simple English like you're explaining something to a 5-year-old. |
| 6          | Add "I'm going to tip $$xx for a better solution!" |
| 7          | Implement example-driven prompting (Use few-shot prompting). |
| 8          | When formatting your prompt, start with "###Instruction###", followed by '###Example###' or '###Question###' if relevant. Subsequently, present your content. Use one or more line breaks to separate instructions, examples, questions, context, and input data. |
| 9          | Incorporate the following phrases: "Your task is" and "You MUST". |
| 10         | Incorporate the following phrases: "You will be penalized". |
| 11         | Use the phrase "Answer a question given in a natural, human-like manner" in your prompts. |
| 12         | Use leading words like writing "think step by step". |
| 13         | Add to your prompt the following phrase "Ensure that your answer is unbiased and avoids relying on stereotypes." |
| 14         | Allow the model to elicit precise details and requirements from you by asking you questions until he has enough information to provide the needed output (for example, "From now on, I would like you to ask me questions to ..."). |
| 15         | To inquire about a specific topic or idea or any information and you want to test your understanding, you can use the following phrase: "Teach me any [theorem/topic/rule name] and include a test at the end, and let me know if my answers are correct after I respond, without providing the answers beforehand." |
| 16         | Assign a role to the large language models. |
| 17         | Use Delimiters. |
| 18         | Repeat a specific word or phrase multiple times within a prompt. |
| 19         | Combine Chain-of-thought (CoT) with few-Shot prompts. |
| 20         | Use output primers, which involve concluding your prompt with the beginning of the desired output. Utilize output primers by ending your prompt with the start of the anticipated response. |
| 21         | To write an essay /text /paragraph /article or any type of text that should be detailed: "Write a detailed [essay/text /paragraph] for me on [topic] in detail by adding all the information necessary". |
| 22         | To correct/change specific text without changing its style: "Try to revise every paragraph sent by users. You should only improve the user's grammar and vocabulary and make sure it sounds natural. You should maintain the original writing style, ensuring that a formal paragraph remains formal." |
| 23         | When you have a complex coding prompt that may be in different files: "From now and on whenever you generate code that spans more than one file, generate a [programming language] script that can be run to automatically create the specified files or make changes to existing files to insert the generated code. [your question]". |
| 24         | When you want to initiate or continue a text using specific words, phrases, or sentences, utilize the following prompt: |
|            | o I'm providing you with the beginning [song lyrics/story/paragraph/essay...]: [Insert lyrics/words/sentence]. |
|            | Finish it based on the words provided. Keep the flow consistent. |
| 25         | Clearly state the requirements that the model must follow in order to produce content, in the form of the keywords, regulations, hint, or instructions |
| 26         | To write any text, such as an essay or paragraph, that is intended to be similar to a provided sample, include the following instructions: |
|            | o Use the same language based on the provided paragraph/title/text/essay/answer. |

## LLMChain

```python
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline

import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoModelForSeq2SeqLM

import torch
from torch import cuda, bfloat16

#In a MAC Silicon the device must be 'mps'
# device = torch.device('mps') #to use with MAC Silicon
device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

#You can try with any llama model, but you will need more GPU and memory as you increase the size of the model.
model_id = "meta-llama/Llama-2-7b-chat-hf"
#model_id = "meta-llama/Llama-2-7b-hf"

# begin initializing HF items, need auth token for these
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_key
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    device_map='auto',
    use_auth_token=hf_key
)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(model_id,
                                          use_aut_token=hf_key) 

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
    temperature=0.3,
    repetition_penalty=1.1,
    return_full_text=True,
    device_map='auto'
)

assistant_llm = HuggingFacePipeline(pipeline=pipe)

# Instruction how the LLM must respond the comments,
assistant_template = """
You are {sentiment} social media post commenter, you will respond to the following post
Post: "{customer_request}"
Comment:
"""

#Create the prompt template to use in the Chain for the first Model.
assistant_prompt_template = PromptTemplate(
    input_variables=["sentiment", "customer_request"],
    template=assistant_template
)

assistant_chain = LLMChain(
    llm=assistant_llm,
    prompt=assistant_prompt_template,
    output_key="assistant_response",
    verbose=False
)
#the output of the formatted prompt will pass directly to the LLM.

# This the customer comment in the forum moderated by the agent.
# feel free to update it.
customer_request = """Your product is a piece of shit. I want my money back!"""

# Our assistatnt working in 'nice' mode.
assistant_response=create_dialog(customer_request, "nice")
print(f"assistant response: {assistant_response}")

#Our assistant running in rude mode.
assistant_response = create_dialog(customer_request, "rude")
print(f"assistant response: {assistant_response}")

#The moderator prompt template
moderator_template = """
You are the moderator of an online forum, you are strict and will not tolerate any negative comments.
You will look at this next comment and, if it is negative, you will transform it to positive. Avoid any negative words.
If it is nice, you will let it remain as is and repeat it word for word.
###
Original comment: {comment_to_moderate}
###
Edited comment:"""

# We use the PromptTemplate class to create an instance of our template that will use the prompt from above and store variables we will need to input when we make the prompt.
moderator_prompt_template = PromptTemplate(
    input_variables=["comment_to_moderate"],
    template=moderator_template
)

moderator_llm = assistant_llm

#We build the chain for the moderator.
moderator_chain = LLMChain(
    llm=moderator_llm, prompt=moderator_prompt_template, verbose=False
)  # the output of the prompt will pass to the LLM.

# To run our chain we use the .run() command
moderator_says = moderator_chain.run({"comment_to_moderate": assistant_response})

print(f"moderator_says: {moderator_says}")

#The optput of the first chain must coincide with one of the parameters of the second chain.
#The parameter is defined in the prompt_template.
assistant_chain = LLMChain(
    llm=assistant_llm,
    prompt=assistant_prompt_template,
    output_key="comment_to_moderate",
    verbose=False,
)

#verbose True because we want to see the intermediate messages.
moderator_chain = LLMChain(
    llm=moderator_llm,
    prompt=moderator_prompt_template,
    verbose=True
)

from langchain.chains import SequentialChain

# Creating the SequentialChain class indicating chains and parameters.
assistant_moderated_chain = SequentialChain(
    chains=[assistant_chain, moderator_chain],
    input_variables=["sentiment", "customer_request"],
    verbose=True,
)

# We can now run the chain.
assistant_moderated_chain.run({"sentiment": "rude", "customer_request": customer_request})


```

## Optimizing Inference on Large Language Models with NVIDIA TensorRT-LLM

https://developer.nvidia.com/blog/optimizing-inference-on-llms-with-tensorrt-llm-now-publicly-available/

https://github.com/furyhawk/TensorRT-LLM