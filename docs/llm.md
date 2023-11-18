# LLM

## AGI

- transformers cannot be used in AGI because it cannot learn and infer new tokens from unseen data. It generalize better from large datasets, and cannot generalize far from unexplored data.

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