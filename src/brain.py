from time import sleep
import logging
import conversation
import utils
import llm
import env

def get(thing, color=None, localization=None):

    if color is not None and localization is not None:
        definition = llm.get(env.OLLAMA_LANGUAGE_MODEL, env.OLLAMA_EN_SEARCH_PROMPT + f"{localization} {color} {thing}")
    
    elif color is not None and localization is None:
        thing_name = f"{color} {thing}"
        definition = utils.accessMemory(thing_name, 'info')
        if definition is None:
            definition = llm.get(env.OLLAMA_LANGUAGE_MODEL, env.OLLAMA_EN_SEARCH_PROMPT + thing_name)
            utils.addMemory(thing_name, definition, 'info')
    
    elif color is None and localization is not None:
        thing_name = f"{localization} {thing}"
        definition = utils.accessMemory(thing_name, 'info')
        if definition is None:
            definition = llm.get(env.OLLAMA_LANGUAGE_MODEL, env.OLLAMA_EN_SEARCH_PROMPT + thing_name)
            utils.addMemory(thing_name, definition, 'info')
    
    else:
        definition = utils.accessMemory(thing, 'info')
        if definition is None:
            definition = llm.get(env.OLLAMA_LANGUAGE_MODEL, env.OLLAMA_EN_SEARCH_PROMPT + thing)
            utils.addMemory(thing, definition, 'info')
            
    return definition
