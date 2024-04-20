import openai

class HIPAgent:
    def get_response(self, question, answer_choices):
        """
        Calls the OpenAI 3.5 API to generate a response to the question.
        The response is then matched to one of the answer choices and the index of the
        matching answer choice is returned. If the response does not match any answer choice,
        -1 is returned.

        Args:
            question: The question to be asked.
            answer_choices: A list of answer choices.

        Returns:
            The index of the answer choice that matches the response, or -1 if the response
            does not match any answer choice.
        """

        # Create the prompt.
        answer_str = "\n".join(answer_choices)
        prompt = f"You are a student doing multiple choice question. You are asked to output the correct choice index (0 to 3, inclusive). No other wording is allowed before or after the index.\n\
            {question} \n\n{answer_str}"
        #print(prompt)
        #print("\n\n")

        # Call the OpenAI 3.5 API.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        response_text = response.choices[0].message.content
        if not response_text.isdigit():
            print(prompt)
            print("\n")
            print(f"gpt's response cannot be parsed as option index {response_text}\n")
            return -1
        
        gpts_choice = answer_choices[int(response_text)]

        # Match the response to one of the answer choices.
        for i, answer_choice in enumerate(answer_choices):
            if gpts_choice == answer_choice:
                return i
        
        # If the response does not match any answer choice, return -1.
        print(prompt)
        print("\n")
        print(f"gpt's response does not match any option. GPT's choice index: {response_text}, GPT's choice: {gpts_choice}\n")
        return -1
