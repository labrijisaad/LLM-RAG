import requests



class ModelInferenceManager:
    def __init__(self, api_key, models_config):
        self.api_key = api_key
        self.models_config = models_config
        self.model = None
        self.input_token_price = None
        self.output_token_price = None

    def set_model(self, model_name):
        for group in self.models_config["models"]:
            for variant in group["variants"]:
                if variant["model"] == model_name:
                    self.model = model_name
                    self.input_token_price = variant["input_price_per_token"]
                    self.output_token_price = variant["output_price_per_token"]
                    return
        raise ValueError(f"Model {model_name} not found in configuration.")

    def query_openai(self, prompt_text, max_completion_tokens=100, temperature=0.7):
        if not self.model:
            raise ValueError(
                "Model not set. Please use set_model() to set a model before querying."
            )
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": max_completion_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data["usage"]
                return content, usage
            else:
                return (
                    f"HTTP Error {response.status_code}: {response.json().get('error', {}).get('message', 'An unspecified error occurred')}",
                    None,
                )
        except requests.RequestException as e:
            return f"Connection error: {e}", None

    def calculate_cost(self, usage):
        if usage:
            total_price = (usage["prompt_tokens"] * self.input_token_price) + (
                usage["completion_tokens"] * self.output_token_price
            )
            return total_price
        else:
            return None

    def determine_expertise_area(
        self, user_question, max_completion_tokens, temperature
    ):
        prompt_text = f"""Based on the question provided, identify the relevant expertise area(s). Return your answer in the format: 
        'expertise1, expertise2, ...'. Provide only the expertise areas as a comma-separated list, no additional explanations are needed.
        Here is the user Question:
        {user_question}
        """
        response, usage = self.query_openai(
            prompt_text, max_completion_tokens, temperature
        )
        return response.strip(), (
            usage if response else "Error determining expertise area."
        )

    def prepare_prompt_for_llm(self, expertise_area, user_question, context_documents):
        prompt = (
            f"You are an expert in '{expertise_area}'. A user has asked for help with the following question: "
            f"'{user_question}'. Please provide insights using only the information from the provided documents. "
            "If certain aspects are ambiguous or the documents do not fully address the question, please make educated inferences based on your expertise.\n\n"
            "Here are the documents provided:\n\n"
        )
        for i, document in enumerate(context_documents, start=1):
            prompt += f'Document {i}:\n"""\n{document}\n"""\n\n'
        prompt += "Given your expertise and the information provided in these documents, synthesize the key insights to craft a detailed and relevant response to the above question.\n\n"
        prompt += "Start your response below:\n\n"
        return prompt