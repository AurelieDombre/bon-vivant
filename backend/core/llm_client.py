import ollama


class LLMClient:

    def complete(self, prompt: str):
        try:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except Exception:
            return (
                "Je n'ai pas pu joindre le modele local Ollama. "
                "Verifie que le service Ollama tourne et que le modele "
                "'llama3' est installe."
            )

        return response["message"]["content"]
