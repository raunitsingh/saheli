import unicodedata


def normalize_text(text):

    text = text.lower()

    text = unicodedata.normalize("NFKD", text)

    return text


def detect_symptoms(text: str):

    text = normalize_text(text)

    detected = []

    SYMPTOMS = {

        "fever": [
            "fever",
            "bukhar",
            "बुखार",
            "बुख़ार"
        ],

        "cough": [
            "cough",
            "khansi",
            "खांसी"
        ],

        "vomiting": [
            "vomit",
            "vomiting",
            "ulti",
            "उल्टी"
        ],

        "diarrhea": [
            "loose motion",
            "diarrhea",
            "dast",
            "दस्त"
        ]

    }

    for symptom, keywords in SYMPTOMS.items():

        for word in keywords:

            if word in text:
                detected.append(symptom)
                break

    return list(set(detected))


if __name__ == "__main__":

    test = "मुझे बहुत ज़्यादा बुख़ार है 3 दिनों से"

    print(detect_symptoms(test))