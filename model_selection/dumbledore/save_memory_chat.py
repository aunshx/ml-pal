import json

class MemoryDataSerializer:
    def __init__(self):
        pass

    def convert_to_dict(self, obj):
        if hasattr(obj, 'content'):
            return {
                'type': obj.__class__.__name__,
                'content': obj.content
            }
        return obj

    def save_memory_data_to_json(self, memory_data, filename="memory_data.json"):
        # Convert chat history to a list of dictionaries
        if 'chat_history' in memory_data:
            chat_history_serializable = [self.convert_to_dict(message) for message in memory_data['chat_history']]
        else:
            chat_history_serializable = []

        # Create a serializable data structure
        serializable_data = {
            'chat_history': chat_history_serializable
        }

        # Save the serializable data to a JSON file
        with open(filename, "w") as json_file:
            json.dump(serializable_data, json_file, indent=4)

        print(f"Memory data saved to {filename}")
