from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from app.core.llm import llm_handler
from app.models.schemas import QuestionRequest, DivinationResponse, HexagramInfo
from app.utils.i_ching import IChing

router = APIRouter()

@router.post("/", response_model=DivinationResponse, summary="Tạo lời giải quẻ Kinh Dịch")
async def create_divination(request: QuestionRequest):
    """
    Tạo lời giải quẻ Kinh Dịch dựa trên câu hỏi của người dùng.
    
    - **question**: Câu hỏi của người dùng để giải quẻ (bắt buộc)
    
    Trả về lời giải quẻ Kinh Dịch được cá nhân hóa bao gồm:
    - Câu hỏi gốc
    - Quẻ được bốc (số, tên, biểu tượng)
    - Chủ đề được xác định từ câu hỏi
    - Lời giải được cá nhân hóa dựa trên quẻ và ngữ cảnh của câu hỏi
    """
    try:
        # Extract the question
        question = request.question
        
        # Generate a random hexagram
        hexagram = IChing.cast_divination()
        
        # Convert hexagram to the expected schema format
        hexagram_info = HexagramInfo(
            number=hexagram["number"],
            name=hexagram["name"],
            symbol=hexagram["symbol"],
            upper_trigram=hexagram.get("upper_trigram"),
            lower_trigram=hexagram.get("lower_trigram"),
            general_meaning=hexagram.get("general_meaning")
        )
        
        # Identify the topic of the question
        topic = llm_handler.get_topic_from_question(question)
        
        # Generate personalized interpretation
        interpretation = llm_handler.generate_interpretation(question, hexagram, topic)
          # Create and return the response
        return DivinationResponse(
            question=question,
            hexagram=hexagram_info,
            topic=topic,
            interpretation=interpretation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo lời giải quẻ: {str(e)}")

@router.get("/hexagrams/{hexagram_id}", summary="Lấy thông tin về quẻ cụ thể")
async def get_hexagram(hexagram_id: int):
    """
    Lấy thông tin về một quẻ Kinh Dịch cụ thể theo số (1-64).
    """
    from app.data.hexagrams import get_hexagram_by_number
    hexagram = get_hexagram_by_number(hexagram_id)
    if not hexagram:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy quẻ số {hexagram_id}")
    
    return hexagram
