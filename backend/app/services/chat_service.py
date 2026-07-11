def generate_reply(message: str) -> str:
    """Resposta placeholder da Sprint 01.

    Na Sprint 02 esta função passa a invocar o grafo LangGraph com o LLM.
    """
    return (
        f"Recebi a tua mensagem: “{message}”. "
        "Sou o TurismoConnect e em breve vou poder guiar-te por Angola. 🇦🇴"
    )
