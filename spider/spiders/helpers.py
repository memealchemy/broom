import re


class Invalids:
    RESEARCH = [
        "This submission is currently being researched and evaluated.",
        "You can help confirm this entry by contributing facts, media, and other evidence of notability and mutation.",
    ]
    NOTFOUND = "Page Not Found (404) - Know Your Meme"
    GALLERY = "Trending Videos Gallery"


class Utils:
    stopwords = [
        "Why Is",
        "Why Does",
        "Everyone",
        "EVERYONE",
        "Why",
        "Is The",
        "How",
        "What Are",
        "What's Up",
        "With",
        "?",
        ".",
        "Are",
        "FINISHED",
    ]

    trails = ("classic", "everywhere", "what")

    def chunkify(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]

    @classmethod
    def tokenize(self, text):
        _list = re.split(
            r"{}".format("|".join(self.trails)), "".join(text), flags=re.IGNORECASE
        )
        return "".join(_list)

    regex = re.compile("|".join(map(re.escape, stopwords)))
    QUESTION_MARK = "https://image.shutterstock.com/image-illustration/question-mark-symbol-on-isolated-260nw-795811507.jpg"
