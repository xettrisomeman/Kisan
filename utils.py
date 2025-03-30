import os
import dspy
import json


lm = dspy.LM("cohere/command-r-plus", api_key=os.environ["COHERE_API_KEY"])
dspy.configure(lm=lm)


def ask_ai(message):
    class AskAI(dspy.Signature):
        """You are an expert ai equipped with agricultural and veterinarian knowledge. Answer questions by farmers."""

        questions: str = dspy.InputField()
        answer: str = dspy.OutputField()

    ask_ai = dspy.ChainOfThought(AskAI)
    return ask_ai(questions=message).answer


def save_json_as_list(data, filename, append_if_exists=True):
    if not isinstance(data, list):
        data = [data]

    if os.path.exists(filename) and append_if_exists:
        try:
            with open(filename, "r") as file:
                existing_data = json.load(file)

            if not isinstance(existing_data, list):
                existing_data = [existing_data]

            existing_data.extend(data)
            data_to_save = existing_data
        except (json.JSONDecodeError, FileNotFoundError):
            data_to_save = data
    else:
        data_to_save = data

    with open(filename, "w") as file:
        json.dump(data_to_save, file, indent=4)


def retrieve_json_list(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    if not isinstance(data, list):
        data = [data]

    return data


def find_item_by_key(data_list, key, value):
    results = []
    for item in data_list:
        if key in item and item[key] == value:
            results.append(item)
    return results


# filename = "example.json"

# data1 = {
#     "messages": "hii",
#     "email": "john@example.com",
#     "expert_response": None,
#     "ai_response": "This is ai response for messages: hii",
# }

# # save_json_as_list(data=data1, filename=filename)

# data2 = {
#     "messages": "hum",
#     "email": "john@example.com",
#     "expert_response": "chum",
#     "ai_response": "This is hum.",
# }

# # save_json_as_list(data=data2, filename=filename)


# data = retrieve_json_list(filename=filename)
