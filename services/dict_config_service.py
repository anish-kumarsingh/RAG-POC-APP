from gens import gen
import ast

class DictConfigService:
    def __init__(self, llm_model:str):
        self.gen_service=gen.GeneratorService(model_id=llm_model)

    def generate_config(self, headers: list[str]) -> dict:
        """
        Sends DataFrame headers to the LLM and returns a parsed chart config.
        :param headers: list of column names
        :return: dictionary with chart configs
        """
        instruction_prompt = """
        You are a data visualization assistant.
        I will give you dataframe column headers.
        Your task is to generate a Python dictionary configuration
        that specifies graph types I can create using Streamlit's
        st.line_chart, st.bar_chart, and st.scatter_chart.

        The config must:
        - Map column names to roles (x, y, color if relevant)
        - Suggest recommended chart types (line, bar, scatter)
        - Return ONLY a valid Python dict (no explanations, no markdown).
        """

        input_query = f"My dataframe has these columns: {headers}"

        response = self.gen_service.generateResponse(input_query, instruction_prompt)

        config_text = response.content

        try:
            config = ast.literal_eval(config_text)
        except Exception:
            config = {}

        return config