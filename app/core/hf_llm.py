"""
Hugging Face Transformers based LLM implementation
for local model inference in I Ching Divination API.
"""

from typing import Any, Dict, List, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class HuggingFaceLLM:
    """
    LLM implementation using Hugging Face Transformers for local inference
    """
    
    def __init__(
        self, 
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        device: Optional[str] = None,
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        truncate: bool = True,
        **kwargs
    ):
        """
        Initialize the Hugging Face model
        
        Args:
            model_name: The name or path of the Hugging Face model
            device: The device to use (cpu, cuda, mps), if None will auto-detect
            max_length: Maximum length of generated text
            temperature: Temperature for sampling
            top_p: Top p for nucleus sampling
            truncate: Whether to truncate input to max_length
        """
        self.model_name = model_name
        self.max_length = max_length
        self.temperature = temperature
        self.top_p = top_p
        self.truncate = truncate
        
        # Force CUDA if available, otherwise auto-detect
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
                print(f"CUDA detected: {torch.cuda.get_device_name(0)}")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"  # Use MPS for Mac with Apple Silicon
                print("Apple Silicon MPS detected")
            else:
                self.device = "cpu"
                print("No GPU detected, falling back to CPU")
        else:
            self.device = device
            print(f"Using user-specified device: {self.device}")
            
        print(f"Initializing Hugging Face LLM with model: {model_name} on device: {self.device}")
        
        # Load the model and tokenizer with better error handling
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Add default pad token if needed
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            # Load the model with appropriate settings
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto" if self.device == "cuda" else None,
            )
            
            # Move model to device if not using device_map="auto"
            if self.device != "cuda" or not hasattr(self.model, "hf_device_map"):
                self.model.to(self.device)
                
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
              # Create pipeline
        pipeline_kwargs = {
            "model": self.model,
            "tokenizer": self.tokenizer,
        }
        
        # Only specify device if we're not using device_map="auto"
        if self.device == "cuda" and hasattr(self.model, "hf_device_map"):
            # Don't specify device when using device_map="auto"
            print("Using device_map='auto', not specifying device in pipeline")
        else:
            # Otherwise specify the device explicitly
            device_arg = 0 if self.device == "cuda" else (-1 if self.device == "cpu" else "mps")
            pipeline_kwargs["device"] = device_arg
            print(f"Setting pipeline device to: {device_arg}")
            
        self.pipe = pipeline("text-generation", **pipeline_kwargs)
        
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on the provided prompt.
        
        Args:
            prompt: The prompt to generate text from
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            The generated text
        """
        # Get parameters, override with kwargs if provided
        max_length = kwargs.get("max_length", self.max_length)
        temperature = kwargs.get("temperature", self.temperature)
        top_p = kwargs.get("top_p", self.top_p)
        
        try:
            # Generate text with explicit truncation parameter
            result = self.pipe(
                prompt,
                max_length=max_length,
                do_sample=temperature > 0,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=1,
                truncation=True,  # Explicitly enable truncation
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
            )
            
            # Extract generated text
            generated_text = result[0]["generated_text"]
            
            # Remove the prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):]
                
            return generated_text.strip()
        except Exception as e:
            print(f"Error during text generation: {e}")
            raise
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """Make the class callable"""
        return self.generate(prompt, **kwargs)

# Factory function to create a Hugging Face LLM
def create_hf_llm(
    model_name: str = "TheBloke/Llama-2-7B-Chat-GGML", 
    **kwargs
) -> HuggingFaceLLM:
    """
    Create a Hugging Face LLM instance
    
    Args:
        model_name: The name or path of the Hugging Face model
        **kwargs: Additional arguments to pass to the HuggingFaceLLM constructor
        
    Returns:
        A HuggingFaceLLM instance
    """
    return HuggingFaceLLM(model_name=model_name, **kwargs)
