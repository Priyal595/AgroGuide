class ChatbotService:
    def __init__(self):
        self.data = {
            "system": {
                "questions": {
                    "How does crop prediction work?": {
                        "answer": "Crop prediction is based on analyzing inputs like soil data, weather conditions, and historical patterns to suggest suitable crops.",
                        "related": [
                            "How is confidence calculated?",
                            "How does weather affect recommendations?"
                        ]
                    },
                    "How is confidence calculated?": {
                        "answer": "Confidence represents how strongly the system supports a recommendation based on available input data.",
                        "related": [
                            "How does crop prediction work?",
                            "Why did I get multiple crop suggestions?"
                        ]
                    },
                    "How is feature importance determined?": {
                        "answer": "Feature importance shows which inputs like rainfall or soil type had the most influence on the recommendation.",
                        "related": [
                            "How does weather affect recommendations?",
                            "How should I interpret the results?"
                        ]
                    },
                    "How does weather affect recommendations?": {
                        "answer": "Weather conditions like rainfall and temperature influence crop suitability and recommendations.",
                        "related": [
                            "What does high rainfall impact mean?",
                            "How is feature importance determined?"
                        ]
                    },
                    "How should I interpret the results?": {
                        "answer": "Results should be used as guidance to support decision-making, not as a strict guarantee.",
                        "related": [
                            "Why did I get multiple crop suggestions?",
                            "What does high rainfall impact mean?"
                        ]
                    },
                    "What does high rainfall impact mean?": {
                        "answer": "High rainfall impact indicates rainfall plays a major role in determining crop suitability.",
                        "related": [
                            "How does weather affect recommendations?",
                            "How should I interpret the results?"
                        ]
                    },
                    "Why did I get multiple crop suggestions?": {
                        "answer": "Multiple crops may suit your conditions equally well, so the system provides several options.",
                        "related": [
                            "How is confidence calculated?",
                            "How should I interpret the results?"
                        ]
                    }
                }
            },
            "agriculture": {
                "questions": {
                    "What are important factors for crop cultivation?": {
                        "answer": "Soil quality, climate, water availability, and nutrient management are key factors for crop cultivation.",
                        "related": [
                            "How does soil pH affect crops?",
                            "Why is irrigation management important?"
                        ]
                    },
                    "How does soil pH affect crops?": {
                        "answer": "Soil pH affects nutrient availability and influences crop growth and yield.",
                        "related": [
                            "Why is NPK important?",
                            "What are important factors for crop cultivation?"
                        ]
                    },
                    "Why is NPK important?": {
                        "answer": "NPK provides essential nutrients required for plant growth and development.",
                        "related": [
                            "How does soil pH affect crops?",
                            "How can farmers improve yield?"
                        ]
                    },
                    "How does temperature impact farming?": {
                        "answer": "Temperature affects crop growth stages, productivity, and stress tolerance.",
                        "related": [
                            "How does climate change affect agriculture?",
                            "What are common farming challenges?"
                        ]
                    },
                    "Why is irrigation management important?": {
                        "answer": "Proper irrigation ensures crops receive adequate water without wastage or damage.",
                        "related": [
                            "How can farmers improve yield?",
                            "What are important factors for crop cultivation?"
                        ]
                    },
                    "What are common farming challenges?": {
                        "answer": "Pests, climate variability, soil degradation, and water scarcity are common challenges.",
                        "related": [
                            "How does climate change affect agriculture?",
                            "How can farmers improve yield?"
                        ]
                    },
                    "How can farmers improve yield?": {
                        "answer": "Using quality seeds, proper nutrient management, and efficient irrigation can improve yield.",
                        "related": [
                            "Why is NPK important?",
                            "Why is irrigation management important?"
                        ]
                    },
                    "How does climate change affect agriculture?": {
                        "answer": "Climate change alters weather patterns, impacting crop productivity and farming stability.",
                        "related": [
                            "How does temperature impact farming?",
                            "What are common farming challenges?"
                        ]
                    }
                }
            }
        }

    def get_categories(self):
        return list(self.data.keys())

    def get_questions(self, category):
        if category not in self.data:
            return None
        return list(self.data[category]["questions"].keys())

    def get_answer(self, category, question):
        if category not in self.data:
            return None
        questions = self.data[category]["questions"]
        return questions.get(question)