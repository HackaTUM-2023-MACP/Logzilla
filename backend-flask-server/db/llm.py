# For summarization
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document
from langchain.prompts import PromptTemplate
from langchain import LLMChain

# for parsing logs
from .log_parser import parse_log

def generate_summary(log_data, llm=None, use_mistral=True):
    # Parse entries as a list of LogEntry objects
    entries = parse_log(log_data)

    # Get string to summarize
    text = ""

    # Initialize previous date to get headers of execution times
    prev_datetime = None

    # Go over all entries
    for entry in entries:
        # Add header for timestamp to avoid duplicates
        if prev_datetime != entry.timestamp:
            text.append(f"TIMESTAMP: {entry.timestamp.strftime('%b %d %H:%M:%S')}\n----------\n")
            prev_datetime = entry.timestamp

        # Add layer and message information to text to summarize
        text.append(entry.layer + "" + entry.message + "\n")

    if use_mistral == True: 
        # Load the text as langchain document object, langchain wants list of Documents
        docs = [Document(page_content=text)]

        # Define prompt template and chains for mapping and reducing

        # map template: used for getting a summary of a single chunk
        map_template = """The following is a set of entries from a system log file:
        {docs}
        Based on this snippet of a system log file, please identify the main events that
        has happened during the log. 

        Answer in less than 3 sentences. 

        Helpful Answer:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        # reduce template: used to combine multiple summaries into one
        reduce_template = """The following is set of summaries of events that happened in a log file:
        {doc_summaries}
        Take these and distill it into a final, consolidated summary of the main events that
        happened within the log.

        Answer in less than 3 sentences.

        Helpful Answer:"""
        reduce_prompt = PromptTemplate.from_template(reduce_template)

        # Run chain
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        # StuffDocuments means that we take all the text and put it in a single string (no chunking)
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="doc_summaries"
        )

        # Combines and iteravely reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=True,
            verbose=True,
        )

        # Separator is important, it is by default `\n\n` (probably)
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1500, chunk_overlap=10, separator="\n"
        )
        split_docs = text_splitter.split_documents(docs)
        print(f"Number of chunks: {len(split_docs)}")

        summary = map_reduce_chain(split_docs)

        return summary
    else:
        raise NotImplementedError
