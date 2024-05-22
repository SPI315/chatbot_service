from transformers import GPT2LMHeadModel, GPT2Tokenizer


class OperModel:
    def __init__(
        self,
        model=GPT2LMHeadModel.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2"),
        tokenizer=GPT2Tokenizer.from_pretrained(
            "sberbank-ai/rugpt3small_based_on_gpt2"
        ),
    ) -> None:
        self.model = model
        self.tokenizer = tokenizer

    # метод для генерации ответа
    def response(self, data):
        data = self.encoder(data)
        data = self.model.generate(
            data,
            max_length=50,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        data = self.decoder(data)
        return data.strip()

    # метод для кодирования данных
    def encoder(self, data):
        return self.tokenizer.encode(data, return_tensors="pt")

    # метод для декодирования данных
    def decoder(self, data):
        return self.tokenizer.decode(data[0], skip_special_tokens=True)
