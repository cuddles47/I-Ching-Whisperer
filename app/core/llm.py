from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from typing import List, Dict, Any, Optional, Protocol, runtime_checkable

from app.core.config import settings
from app.core.hf_llm import create_hf_llm, HuggingFaceLLM

@runtime_checkable
class LLMInterface(Protocol):
    def invoke(self, messages) -> Any:
        ...
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...

class HuggingFaceAdapter:
    """Adapter to make HuggingFaceLLM compatible with LangChain's interface"""
    
    def __init__(self, model: HuggingFaceLLM):
        self.model = model
    
    def invoke(self, messages):
        """Convert LangChain messages to a prompt string and invoke the model"""
        prompt = self._convert_messages_to_prompt(messages)
        response = self.model(prompt)
        
        # Create a simple object with a content attribute to mimic LangChain's response
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(response)
    
    def _convert_messages_to_prompt(self, messages) -> str:
        """Convert LangChain messages to a string prompt format that works with most models"""
        prompt_parts = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                prompt_parts.append(f"# Yêu cầu hệ thống:\n{message.content}\n")
            elif isinstance(message, HumanMessage):
                prompt_parts.append(f"# Câu hỏi:\n{message.content}\n")
            else:
                prompt_parts.append(f"{message.content}\n")
                
        return "\n".join(prompt_parts)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.invoke(*args, **kwds)

class LLMHandler:
    def __init__(self):
        if settings.LLM_PROVIDER == "openai":
            self.llm = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_MODEL_NAME,
                temperature=0.7
            )
        else:  # huggingface
            hf_model = create_hf_llm(
                model_name=settings.HF_MODEL_NAME,
                device=settings.HF_DEVICE,
                max_length=settings.HF_MAX_LENGTH,
                max_new_tokens=settings.HF_MAX_NEW_TOKENS,
                temperature=settings.HF_TEMPERATURE,
                top_p=settings.HF_TOP_P
            )
            self.llm = HuggingFaceAdapter(hf_model)
    
    def get_topic_from_question(self, question: str) -> str:
        """Extract the topic from the user's question"""
        system_prompt = (
            "Bạn là một chuyên gia giải quẻ Kinh Dịch. "
            "Nhiệm vụ của bạn là xác định chủ đề chính hoặc chủ điểm của câu hỏi người dùng. "
            "Các chủ đề có thể là: Sự nghiệp/Kinh doanh, Tình yêu/Mối quan hệ, Sức khỏe, "
            "Phát triển bản thân, Gia đình, Giáo dục, Tài chính, Du lịch, Tâm linh, Định hướng cuộc sống, hoặc Khác. "
            "Chỉ trả lời một trong những chủ đề này mà không có bất kỳ lời giải thích hay văn bản bổ sung nào."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
        
        response = self.llm.invoke(messages)
        return response.content.strip()
    
    def generate_interpretation(self, question: str, hexagram: Dict[str, Any], topic: str) -> str:
        """Generate a personalized interpretation based on the question, hexagram and topic"""
        system_prompt = (
            "Bạn là một bậc thầy giải quẻ Kinh Dịch với kiến thức sâu rộng về truyền thống cổ xưa này. "
            "Hãy đưa ra lời giải quẻ được cá nhân hóa cho câu hỏi của người dùng dựa trên quẻ đã được bốc. "
            "Lời giải của bạn nên tôn trọng truyền thống Kinh Dịch đồng thời mang tính thực tiễn và hữu ích. "
            "Hãy tham chiếu đến các khía cạnh cụ thể của quẻ và ý nghĩa của nó, kết nối với câu hỏi của người dùng và chủ đề đã xác định. "
            "Lời giải nên dài 3-5 đoạn văn, sâu sắc, và đưa ra hướng dẫn hơn là một dự đoán cụ thể. "
            "Sử dụng giọng điệu từ bi, khôn ngoan và cân nhắc các sắc thái tinh tế trong ý nghĩa của quẻ. "
            "Hãy trả lời bằng tiếng Việt."
        )
        
        hex_info = (
            f"Hexagram: {hexagram['number']} - {hexagram['name']}\n"
            f"Symbol: {hexagram['symbol']}\n"
            f"Upper trigram: {hexagram.get('upper_trigram', '')}\n"
            f"Lower trigram: {hexagram.get('lower_trigram', '')}\n"
            f"General meaning: {hexagram.get('general_meaning', '')}\n"
        )
        
        human_prompt = (
            f"Câu hỏi của người dùng: {question}\n"
            f"Chủ đề đã xác định: {topic}\n"
            f"{hex_info}\n"
            "Vui lòng đưa ra lời giải quẻ Kinh Dịch được cá nhân hóa."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content.strip()

# Create a singleton instance
llm_handler = LLMHandler()
