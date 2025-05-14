from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class QuestionRequest(BaseModel):
    """Schema for the divination request"""
    question: str = Field(
        ..., 
        description="Câu hỏi của người dùng để giải quẻ",
        examples=["Dự án kinh doanh của tôi có thành công trong năm nay không?", "Tôi có nên bắt đầu mối quan hệ mới không?", "Đây có phải là thời điểm thích hợp để thay đổi nghề nghiệp không?"]
    )

class HexagramInfo(BaseModel):
    """Schema for hexagram information"""
    number: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Kiền (Thuần Dương)"])
    symbol: str = Field(..., examples=["☰"])
    upper_trigram: Optional[str] = Field(None, examples=["Thiên"])
    lower_trigram: Optional[str] = Field(None, examples=["Thiên"])
    general_meaning: Optional[str] = Field(None, examples=["Sức mạnh nguyên thủy, sáng tạo, sức mạnh và kiên trì."])

class DivinationResponse(BaseModel):
    """Schema for the divination response"""
    question: str = Field(..., examples=["Dự án kinh doanh của tôi có thành công trong năm nay không?"])
    hexagram: HexagramInfo
    topic: str = Field(..., examples=["Sự nghiệp/Kinh doanh"])
    interpretation: str = Field(..., examples=[
        "Quẻ Kiền (Thuần Dương) cho thấy dự án kinh doanh của bạn có tiềm năng thành công mạnh mẽ trong năm nay. Giống như năng lượng thuần dương được thể hiện qua sáu hào dương, sáng kiến của bạn mang theo những lực lượng sáng tạo mạnh mẽ có thể hiện thực hóa tầm nhìn của bạn với sự rõ ràng và sức mạnh. Thời điểm này thuận lợi cho hành động táo bạo và khả năng lãnh đạo.\n\nTuy nhiên, Kinh Dịch nhắc nhở bạn rằng thành công sẽ đòi hỏi sự kiên trì và duy trì các nguyên tắc đạo đức trong suốt hành trình của bạn. Con rồng cao quý được tượng trưng trong quẻ này đạt được sự vĩ đại thông qua nỗ lực liên tục và giữ đúng bản chất của nó. Doanh nghiệp của bạn sẽ phát triển khi bạn thể hiện những phẩm chất tương tự - kiên trì trước những thách thức đồng thời duy trì tính chính trực trong mọi giao dịch.\n\nĐây là thời điểm để có tầm nhìn nhưng cũng cần thực tế. Quẻ Kiền nhắc nhở chúng ta rằng sức mạnh của trời hoạt động thông qua kế hoạch cẩn thận và thực hiện có kỷ luật. Tập trung vào việc xây dựng nền tảng vững chắc cho dự án của bạn trong khi giữ tầm nhìn cao. Khi kết hợp khát vọng cao với hành động thực tế, năng lượng của quẻ Kiền hỗ trợ thành tựu đáng kể trong các nỗ lực kinh doanh của bạn năm nay."
    ])
