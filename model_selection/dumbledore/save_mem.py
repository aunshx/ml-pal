import json

class MemoryDataSerializer:
    def __init__(self):
        pass

    def separate_conversation(self, conversation):
        # Initialize empty lists for Human and AI messages
        messages = []
        
        # Split conversation by newlines and process each line
        lines = conversation.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith('Human:'):
                messages.append({'human': line[len('Human:'):].strip()})
            elif line.startswith('AI:'):
                messages.append({'ai': line[len('AI:'):].strip()})

        return messages

    def save_memory_data_to_json(self, memory_data, filename="memory_data.json"):
        # Extract and separate chat history if it's a string
        if isinstance(memory_data.get('chat_history'), str):
            messages = self.separate_conversation(memory_data['chat_history'])
        elif 'chat_history' in memory_data:
            chat_history_serializable = [self.convert_to_dict(message) for message in memory_data['chat_history']]
            messages = []
            for msg in chat_history_serializable:
                if msg.get('type') == 'Human':
                    messages.append({'human': msg.get('content')})
                elif msg.get('type') == 'AI':
                    messages.append({'ai': msg.get('content')})
        else:
            messages = []

        # Create a serializable data structure
        serializable_data = {
            'messages': messages
        }

        # Save the serializable data to a JSON file
        with open(filename, "w") as json_file:
            json.dump(serializable_data, json_file, indent=4)

        print(f"Memory data saved to {filename}")


