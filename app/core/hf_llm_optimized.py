"""
Hugging Face Transformers based LLM implementation
for local model inference in I Ching Divination API.
With optimized performance for GPU usage.
"""

import platform
import importlib.util
from typing import Any, Dict, List, Optional
import torch
import pkg_resources
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

# Kiểm tra phiên bản transformers
try:
    transformers_version = pkg_resources.get_distribution("transformers").version
    print(f"Transformers version: {transformers_version}")
except Exception:
    transformers_version = "unknown"

# Kiểm tra các gói tăng tốc có sẵn
HAVE_BITSANDBYTES = importlib.util.find_spec("bitsandbytes") is not None
HAVE_OPTIMUM = False  # Default to False to avoid issues

# Check if optimum is compatible with current transformers version
if importlib.util.find_spec("optimum.bettertransformer") is not None:
    try:
        from packaging import version
        if version.parse(transformers_version) < version.parse("4.49.0"):
            HAVE_OPTIMUM = True
        else:
            print("⚠️ BetterTransformer is not compatible with transformers >= 4.49.0")
            print("   Disabling BetterTransformer optimization")
    except ImportError:
        print("⚠️ Can't check transformers version compatibility, disabling BetterTransformer")

HAVE_FLASH_ATTN = importlib.util.find_spec("flash_attn") is not None

def check_accelerators():
    """Kiểm tra và hiển thị thông tin về các gói tăng tốc"""
    accelerators = {
        "flash_attn": "Flash Attention (tăng tốc 2-3x)",
        "bitsandbytes": "8-bit quantization (giảm sử dụng bộ nhớ)",
        "xformers": "Optimized attention mechanisms",
        "optimum": "BetterTransformer optimization"
    }
    
    missing = []
    for lib, description in accelerators.items():
        if importlib.util.find_spec(lib) is None:
            missing.append(f"- {lib}: {description}")
    
    if missing:
        print("\n⚠️ CẢNH BÁO: Các bộ tăng tốc sau đây chưa được cài đặt:")
        print("\n".join(missing))
        print("\nĐể cải thiện hiệu năng, hãy cài đặt: pip install flash-attn xformers bitsandbytes optimum\n")
    else:
        print("✅ Tất cả các gói tăng tốc đã được cài đặt.")

class HuggingFaceLLM:
    """
    LLM implementation using Hugging Face Transformers for local inference
    with optimized performance settings
    """
    def __init__(
        self, 
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        device: Optional[str] = None,
        max_length: int = 2048,
        max_new_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
        truncate: bool = True,
        use_better_transformer: bool = True,
        use_flash_attention: bool = True,
        use_8bit: bool = True,
        use_4bit: bool = False,
        batch_size: int = 1,
        **kwargs
    ):
        """
        Initialize the Hugging Face model
        
        Args:
            model_name: The name or path of the Hugging Face model
            device: The device to use (cpu, cuda, mps), if None will auto-detect
            max_length: Maximum length of input tokens
            max_new_tokens: Maximum number of new tokens to generate
            temperature: Temperature for sampling
            top_p: Top p for nucleus sampling
            truncate: Whether to truncate input to max_length
        """
        self.model_name = model_name
        self.max_length = max_length
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.truncate = truncate
        
        # Kiểm tra các bộ tăng tốc có sẵn
        check_accelerators()
        
        # Thiết lập thiết bị và hiển thị thông tin chi tiết
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
                device_name = torch.cuda.get_device_name(0)
                device_cap = torch.cuda.get_device_capability(0)
                total_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"🚀 GPU detected: {device_name}")
                print(f"   Compute capability: {device_cap}")
                print(f"   Total memory: {total_mem:.2f} GB")
                
                # Thiết lập tăng tốc CUDA
                torch.backends.cudnn.benchmark = True
                print("   CUDA optimization: Enabled")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"
                print("🍎 Apple Silicon MPS detected")
            else:
                self.device = "cpu"
                print("⚠️ No GPU detected, falling back to CPU")
                print(f"   CPU: {platform.processor()}")
        else:
            self.device = device
            print(f"Using user-specified device: {self.device}")            
        print(f"Initializing Hugging Face LLM with model: {model_name} on device: {self.device}")
        
        # Store optimization parameters
        self.use_better_transformer = kwargs.get('use_better_transformer', True)
        self.use_flash_attention = kwargs.get('use_flash_attention', True)
        self.use_8bit = kwargs.get('use_8bit', True)
        self.use_4bit = kwargs.get('use_4bit', False)
        self.batch_size = kwargs.get('batch_size', 1)
        
        # Tải model và tokenizer với các thiết lập tối ưu
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Thêm pad token nếu cần
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                  # Cấu hình tối ưu cho mô hình
            model_kwargs = {
                "torch_dtype": torch.float16,  # Luôn dùng FP16 khi có thể để tăng tốc
                "low_cpu_mem_usage": True,
            }
            
            # Thêm cấu hình đặc biệt cho GPU
            if self.device == "cuda":
                model_kwargs["device_map"] = "auto"
                
                # Sử dụng quantization nếu được yêu cầu và có bitsandbytes
                if HAVE_BITSANDBYTES:
                    # Modern way to use quantization with BitsAndBytesConfig
                    if self.use_4bit:
                        print("🔥🔥 Using 4-bit quantization for maximum memory savings")
                        model_kwargs["quantization_config"] = BitsAndBytesConfig(
                            load_in_4bit=True,
                            bnb_4bit_compute_dtype=torch.float16,
                            bnb_4bit_use_double_quant=True,
                            bnb_4bit_quant_type="nf4"
                        )
                    elif self.use_8bit:
                        print("🔥 Using 8-bit quantization to reduce memory usage")
                        model_kwargs["quantization_config"] = BitsAndBytesConfig(
                            load_in_8bit=True
                        )
                        
                # Sử dụng FlashAttention nếu được yêu cầu và có thư viện
                if self.use_flash_attention and HAVE_FLASH_ATTN:
                    model_kwargs["attn_implementation"] = "flash_attention_2"
                    print("⚡ Using FlashAttention for faster processing")
                    
            # Tải mô hình với cache để tăng tốc lần sau
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                **model_kwargs
            )
              # Áp dụng BetterTransformer nếu được yêu cầu và có thư viện
            if self.use_better_transformer and HAVE_OPTIMUM and self.device == "cuda":
                try:
                    from optimum.bettertransformer import BetterTransformer
                    self.model = BetterTransformer.transform(self.model)
                    print("📈 Using BetterTransformer for improved performance")
                except (ImportError, RuntimeError) as e:
                    print(f"Could not apply BetterTransformer: {e}")
                    print("Continuing without BetterTransformer optimization")
            
            # Di chuyển mô hình đến thiết bị nếu không sử dụng device_map="auto"
            if self.device != "cuda" or not hasattr(self.model, "hf_device_map"):
                self.model.to(self.device)
                
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
            
        # Tạo pipeline với thiết lập tối ưu
        pipeline_kwargs = {
            "model": self.model,
            "tokenizer": self.tokenizer,
            "return_full_text": False,
            "batch_size": self.batch_size,
        }
        
        # Chỉ chỉ định thiết bị khi không sử dụng device_map="auto"
        if self.device == "cuda" and hasattr(self.model, "hf_device_map"):
            print("Using device_map='auto', not specifying device in pipeline")
        else:
            device_arg = 0 if self.device == "cuda" else (-1 if self.device == "cpu" else "mps")
            pipeline_kwargs["device"] = device_arg
            print(f"Setting pipeline device to: {device_arg}")
            
        self.pipe = pipeline("text-generation", **pipeline_kwargs)
        print("✅ Model initialization complete")
        
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The prompt to generate text from
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            The generated text
        """
        # Lấy tham số, ghi đè bằng kwargs nếu có
        max_new_tokens = kwargs.get("max_new_tokens", self.max_new_tokens)
        temperature = kwargs.get("temperature", self.temperature)
        top_p = kwargs.get("top_p", self.top_p)
        
        try:
            # Kiểm tra độ dài prompt
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
            input_length = input_ids.shape[1]
            
            if input_length > self.max_length - 100 and self.truncate:
                print(f"⚠️ Warning: Input length ({input_length} tokens) is very long. Truncating prompt.")
                # Cắt bớt từ đầu, giữ lại phần cuối quan trọng hơn
                truncated_prompt = self.tokenizer.decode(
                    input_ids[0, -(self.max_length - 100):],
                    skip_special_tokens=True
                )
                prompt = f"[Context truncated]... {truncated_prompt}"
                
            # Sinh văn bản với thiết lập tối ưu
            result = self.pipe(
                prompt,
                do_sample=temperature > 0,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                num_return_sequences=1,
                truncation=True,
                repetition_penalty=1.1,  # Tránh lặp lại
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
            )
            
            # Trích xuất văn bản đã sinh
            generated_text = result[0]["generated_text"]
            
            # Loại bỏ prompt từ văn bản đã sinh
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):]
                
            return generated_text.strip()
        except Exception as e:
            print(f"Error during text generation: {e}")
            return f"Lỗi khi sinh văn bản: {e}"
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """Make the class callable"""
        return self.generate(prompt, **kwargs)

# Factory function to create a Hugging Face LLM
def create_hf_llm(
    model_name: str = "TheBloke/Llama-2-7B-Chat-GGML",
    device: Optional[str] = None,
    max_length: int = 2048,
    max_new_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    truncate: bool = True,
    use_better_transformer: bool = True,
    use_flash_attention: bool = True,
    use_8bit: bool = True,
    use_4bit: bool = False,
    batch_size: int = 1,
    **kwargs
) -> HuggingFaceLLM:
    """
    Create a Hugging Face LLM instance with optimizations
    
    Args:
        model_name: The name or path of the Hugging Face model
        device: Which device to use (cuda, cpu, mps)
        max_length: Maximum token length for context
        max_new_tokens: Maximum new tokens to generate
        temperature: Temperature for generation (randomness)
        top_p: Top-p sampling parameter
        truncate: Whether to truncate long inputs
        use_better_transformer: Whether to use BetterTransformer optimizations
        use_flash_attention: Whether to use Flash Attention 2
        use_8bit: Whether to use 8-bit quantization
        use_4bit: Whether to use more aggressive 4-bit quantization
        batch_size: Batch size for inference
        **kwargs: Additional arguments to pass to the HuggingFaceLLM constructor
        
    Returns:
        A HuggingFaceLLM instance with optimizations enabled
    """
    return HuggingFaceLLM(
        model_name=model_name,
        device=device,
        max_length=max_length,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        truncate=truncate,
        use_better_transformer=use_better_transformer,
        use_flash_attention=use_flash_attention,
        use_8bit=use_8bit,
        use_4bit=use_4bit,
        batch_size=batch_size,
        **kwargs
    )
