class ChatbotService:
    def __init__(self):
        self.data = {
            "system": {
                "questions": {
                    
                    "How is confidence calculated?": {
                        "answer": "Confidence represents how strongly the system supports a recommendation based on available input data.",
                        "related": [
                            "How does crop prediction work?",
                            "Why did I get multiple crop suggestions?"
                        ],
                        "links": []
                    },
                    "How is feature importance determined?": {
                        "answer": "Feature importance shows which inputs like rainfall or soil type had the most influence on the recommendation.",
                        "related": [
                            "How does weather affect recommendations?",
                            "How should I interpret the results?"
                        ],
                        "links": []
                    },
                    
                    "How should I interpret the results?": {
                        "answer": "Results should be used as guidance to support decision-making, not as a strict guarantee.",
                        "related": [
                            "Why did I get multiple crop suggestions?",
                            "What does high rainfall impact mean?"
                        ],
                        "links": []
                    },
                    "What does high rainfall impact mean?": {
                        "answer": "High rainfall impact indicates rainfall plays a major role in determining crop suitability.",
                        "related": [
                            "How does weather affect recommendations?",
                            "How should I interpret the results?"
                        ],
                        "links": []
                    },
                    "Why did I get multiple crop suggestions?": {
                        "answer": "Multiple crops may suit your conditions equally well, so the system provides several options.",
                        "related": [
                            "How is confidence calculated?",
                            "How should I interpret the results?"
                        ],
                        "links": []
                    },
                    "How does weather affect recommendations?": {
                            "answer": "Weather parameters such as rainfall and temperature influence crop suitability and prediction outcomes.",
                            "related": [
                                "How does crop prediction work?",
                                "What does high rainfall impact mean?"
                            ],
                        "links": [
                        {
                            "title": "Indian Meteorological Department",
                            "url": "https://mausam.imd.gov.in/"
                        },
                        {
                            "title": "FAO – Climate and Agriculture",
                            "url": "https://www.fao.org/climate-change/en/"
                        }
                        ]
                    },

                    "How does crop prediction work?": {
                        "answer": "Crop prediction analyzes soil nutrients and climate inputs to determine suitable crops using structured decision logic.",
                        "related": [
                            "How is confidence calculated?",
                            "How does weather affect recommendations?"
                        ],
                        "links": [
                            {
                                "title": "FAO – Digital Agriculture",
                                "url": "https://www.fao.org/e-agriculture/en/"
                            },
                            {
                                "title": "World Bank – Digital Agriculture Overview",
                                "url": "https://www.worldbank.org/en/topic/agriculture/brief/digital-agriculture"
                            }
                        ]
                    }
                }
            },
            "agriculture": {
    "questions": {

        "What are important factors for crop cultivation?": {
            "answer": "Successful crop cultivation depends on soil quality, climate conditions, water availability, nutrient balance, and proper farm management practices.",
            "related": [
                "How does soil pH affect crops?",
                "Why is irrigation management important?"
            ],
            "links": [
                {
                    "title": "FAO – Crop Production Resources",
                    "url": "https://www.fao.org/home/en"
                },
                {
                    "title": "ICAR – Indian Council of Agricultural Research",
                    "url": "https://icar.org.in/"
                }
            ]
        },

        "How does soil pH affect crops?": {
            "answer": "Soil pH influences nutrient availability and microbial activity in soil. Most crops grow best in slightly acidic to neutral soil (pH 6–7).",
            "related": [
                "Why is NPK important?",
                "What are important factors for crop cultivation?"
            ],
            "links": [
                {
                    "title": "FAO – Soil Management Portal",
                    "url": "https://www.fao.org/soils-portal/soil-management/en/"
                },
                {
                    "title": "USDA – Soil Health Information",
                    "url": "https://www.nrcs.usda.gov/conservation-basics/natural-resource-concerns/soils/soil-health"
                }
            ]
        },

        "Why is NPK important?": {
            "answer": "Nitrogen (N), Phosphorus (P), and Potassium (K) are essential nutrients required for plant growth, root development, and overall crop productivity.",
            "related": [
                "How does soil pH affect crops?",
                "How can farmers improve yield?"
            ],
            "links": [
                {
                    "title": "FAO – Plant Nutrition and Fertilizers",
                    "url": "https://www.fao.org/3/y5031e/y5031e05.htm"
                },
                {
                    "title": "ICAR – Indian Institute of Soil Science",
                    "url": "https://iiss.icar.gov.in/"
                }
            ]
        },

        "How does temperature impact farming?": {
            "answer": "Temperature affects seed germination, crop growth stages, flowering, and yield. Extreme heat or cold can stress crops and reduce productivity.",
            "related": [
                "How does climate change affect agriculture?",
                "What are common farming challenges?"
            ],
            "links": [
                {
                    "title": "FAO – Climate Change & Agriculture",
                    "url": "https://www.fao.org/climate-change/en/"
                },
                {
                    "title": "IPCC – Climate Change Reports",
                    "url": "https://www.ipcc.ch/reports/"
                }
            ]
        },

        "Why is irrigation management important?": {
            "answer": "Proper irrigation ensures crops receive adequate water while preventing overwatering, soil erosion, and nutrient loss.",
            "related": [
                "How can farmers improve yield?",
                "What are important factors for crop cultivation?"
            ],
            "links": [
                {
                    "title": "FAO – Irrigation and Water Management",
                    "url": "https://www.fao.org/land-water/water/water-management/en/"
                },
                {
                    "title": "ICAR – Water Management Research",
                    "url": "https://icar.org.in/"
                }
            ]
        },

        "What are common farming challenges?": {
            "answer": "Farmers face challenges such as climate variability, pest attacks, soil degradation, water scarcity, and market fluctuations.",
            "related": [
                "How does climate change affect agriculture?",
                "How can farmers improve yield?"
            ],
            "links": [
                {
                    "title": "FAO – Agricultural Publications",
                    "url": "https://www.fao.org/publications/en/"
                },
                {
                    "title": "World Bank – Agriculture & Food Security",
                    "url": "https://www.worldbank.org/en/topic/agriculture"
                }
            ]
        },

        "How can farmers improve yield?": {
            "answer": "Farmers can improve yield through balanced fertilization, quality seeds, pest management, efficient irrigation, and modern farming practices.",
            "related": [
                "Why is NPK important?",
                "Why is irrigation management important?"
            ],
            "links": [
                {
                    "title": "FAO – Sustainable Crop Production",
                    "url": "https://www.fao.org/agriculture/crops/thematic-sitemap/theme/spi/en/"
                },
                {
                    "title": "ICAR – Agricultural Extension Services",
                    "url": "https://icar.org.in/"
                }
            ]
        },

        "How does climate change affect agriculture?": {
            "answer": "Climate change alters rainfall patterns, increases extreme weather events, and affects crop productivity and food security.",
            "related": [
                "How does temperature impact farming?",
                "What are common farming challenges?"
            ],
            "links": [
                {
                    "title": "IPCC – Climate Change Reports",
                    "url": "https://www.ipcc.ch/"
                },
                {
                    "title": "FAO – Climate Change Impact",
                    "url": "https://www.fao.org/climate-change/en/"
                }
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