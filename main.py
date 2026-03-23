# # # # # import requests
# # # # #
# # # # # WIKI_API = "https://en.wikipedia.org/w/api.php"
# # # # #
# # # # # # Words that indicate non-useful / maintenance categories
# # # # # USELESS_KEYWORDS = [
# # # # #     "articles",
# # # # #     "wikipedia",
# # # # #     "pages",
# # # # #     "short description",
# # # # #     "wikidata",
# # # # #     "cs1",
# # # # #     "use dmy",
# # # # #     "use mdy",
# # # # #     "maintenance",
# # # # #     "stubs",
# # # # #     "template",
# # # # #     "infobox"
# # # # # ]
# # # # #
# # # # #
# # # # # def is_useful(category):
# # # # #     category = category.lower()
# # # # #     return not any(word in category for word in USELESS_KEYWORDS)
# # # # #
# # # # #
# # # # # def get_categories(term):
# # # # #     params = {
# # # # #         "action": "query",
# # # # #         "prop": "categories",
# # # # #         "titles": term,
# # # # #         "format": "json",
# # # # #         "cllimit": "max"
# # # # #     }
# # # # #
# # # # #     headers = {
# # # # #         "User-Agent": "WikiCategoryFetcher/1.0 (student project)"
# # # # #     }
# # # # #
# # # # #     try:
# # # # #         response = requests.get(WIKI_API, params=params, headers=headers, timeout=10)
# # # # #
# # # # #         if response.status_code != 200:
# # # # #             print("Request failed with status:", response.status_code)
# # # # #             return []
# # # # #
# # # # #         data = response.json()
# # # # #
# # # # #     except Exception as e:
# # # # #         print("Error while fetching data:", e)
# # # # #         return []
# # # # #
# # # # #     pages = data.get("query", {}).get("pages", {})
# # # # #
# # # # #     categories = []
# # # # #
# # # # #     for page_id in pages:
# # # # #         page = pages[page_id]
# # # # #
# # # # #         if "missing" in page:
# # # # #             print("No Wikipedia page found for this term.")
# # # # #             return []
# # # # #
# # # # #         if "categories" in page:
# # # # #             for cat in page["categories"]:
# # # # #                 name = cat["title"].replace("Category:", "")
# # # # #                 if is_useful(name):
# # # # #                     categories.append(name)
# # # # #
# # # # #     return categories[:3]
# # # # #
# # # # #
# # # # # # ------------------- MAIN -------------------
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     term = input("Enter a word: ").strip()
# # # # #
# # # # #     result = get_categories(term)
# # # # #
# # # # #     if result:
# # # # #         print("\nTop Categories:")
# # # # #         for r in result:
# # # # #             print("•", r)
# # # # #     else:
# # # # #         print("\nNo useful categories found.")
# # # #
# # # #
# # # #
# # # # import requests
# # # # from collections import Counter
# # # #
# # # # WIKI_API = "https://en.wikipedia.org/w/api.php"
# # # #
# # # # USELESS_KEYWORDS = [
# # # #     "articles", "wikipedia", "pages", "short description",
# # # #     "wikidata", "cs1", "use dmy", "use mdy",
# # # #     "maintenance", "stubs", "template", "infobox"
# # # # ]
# # # #
# # # #
# # # # def is_useful(category):
# # # #     category = category.lower()
# # # #     return not any(word in category for word in USELESS_KEYWORDS)
# # # #
# # # #
# # # # def search_pages(term):
# # # #     params = {
# # # #         "action": "query",
# # # #         "list": "search",
# # # #         "srsearch": term,
# # # #         "format": "json",
# # # #         "srlimit": 5
# # # #     }
# # # #
# # # #     headers = {"User-Agent": "WikiCategoryFetcher/1.0"}
# # # #
# # # #     res = requests.get(WIKI_API, params=params, headers=headers).json()
# # # #
# # # #     return [item["title"] for item in res["query"]["search"]]
# # # #
# # # #
# # # # def get_categories(title):
# # # #     params = {
# # # #         "action": "query",
# # # #         "prop": "categories",
# # # #         "titles": title,
# # # #         "format": "json",
# # # #         "cllimit": "max"
# # # #     }
# # # #
# # # #     headers = {"User-Agent": "WikiCategoryFetcher/1.0"}
# # # #
# # # #     res = requests.get(WIKI_API, params=params, headers=headers).json()
# # # #
# # # #     pages = res["query"]["pages"]
# # # #
# # # #     cats = []
# # # #
# # # #     for page_id in pages:
# # # #         page = pages[page_id]
# # # #         if "categories" in page:
# # # #             for cat in page["categories"]:
# # # #                 name = cat["title"].replace("Category:", "")
# # # #                 if is_useful(name):
# # # #                     cats.append(name)
# # # #
# # # #     return cats
# # # #
# # # #
# # # # def get_top_categories(term):
# # # #     titles = search_pages(term)
# # # #
# # # #     all_categories = []
# # # #
# # # #     for title in titles:
# # # #         all_categories.extend(get_categories(title))
# # # #
# # # #     counter = Counter(all_categories)
# # # #
# # # #     return [cat for cat, _ in counter.most_common(3)]
# # # #
# # # #
# # # # # ---------------- MAIN ----------------
# # # #
# # # # if __name__ == "__main__":
# # # #     term = input("Enter a word: ")
# # # #
# # # #     result = get_top_categories(term)
# # # #
# # # #     print("\nTop Relevant Categories:")
# # # #     for r in result:
# # # #         print("•", r)
# # #
# # #
# # #
# # # import requests
# # # from collections import Counter
# # # import re
# # #
# # # WIKI_API = "https://en.wikipedia.org/w/api.php"
# # #
# # # STOPWORDS = {
# # #     "of", "and", "in", "the", "by", "for", "with",
# # #     "from", "on", "at", "to", "an", "a"
# # # }
# # #
# # # NOISE_PATTERNS = [
# # #     "articles", "wikipedia", "pages", "short description",
# # #     "wikidata", "cs1", "use dmy", "use mdy",
# # #     "maintenance", "stubs", "template", "infobox",
# # #     "philosophy of", "history of", "concepts in", "theory of"
# # # ]
# # #
# # #
# # # def clean_text(text):
# # #     text = text.lower()
# # #     text = re.sub(r'[^a-zA-Z ]', '', text)
# # #     return text
# # #
# # #
# # # def is_useful(category):
# # #     category = category.lower()
# # #     return not any(pattern in category for pattern in NOISE_PATTERNS)
# # #
# # #
# # # def extract_keywords(category):
# # #     category = clean_text(category)
# # #     words = category.split()
# # #
# # #     return [w for w in words if w not in STOPWORDS and len(w) > 2]
# # #
# # #
# # # def search_pages(term):
# # #     params = {
# # #         "action": "query",
# # #         "list": "search",
# # #         "srsearch": term,
# # #         "format": "json",
# # #         "srlimit": 5
# # #     }
# # #
# # #     headers = {"User-Agent": "WikiCategoryFetcher/1.0"}
# # #
# # #     res = requests.get(WIKI_API, params=params, headers=headers).json()
# # #
# # #     return [item["title"] for item in res["query"]["search"]]
# # #
# # #
# # # def get_categories(title):
# # #     params = {
# # #         "action": "query",
# # #         "prop": "categories",
# # #         "titles": title,
# # #         "format": "json",
# # #         "cllimit": "max"
# # #     }
# # #
# # #     headers = {"User-Agent": "WikiCategoryFetcher/1.0"}
# # #
# # #     res = requests.get(WIKI_API, params=params, headers=headers).json()
# # #
# # #     pages = res["query"]["pages"]
# # #
# # #     cats = []
# # #
# # #     for page_id in pages:
# # #         page = pages[page_id]
# # #         if "categories" in page:
# # #             for cat in page["categories"]:
# # #                 name = cat["title"].replace("Category:", "")
# # #                 if is_useful(name):
# # #                     cats.append(name)
# # #
# # #     return cats
# # #
# # #
# # # def get_top_domains(term):
# # #     titles = search_pages(term)
# # #
# # #     keyword_counter = Counter()
# # #
# # #     for title in titles:
# # #         categories = get_categories(title)
# # #
# # #         for cat in categories:
# # #             keywords = extract_keywords(cat)
# # #             keyword_counter.update(keywords)
# # #
# # #     return [word for word, _ in keyword_counter.most_common(3)]
# # #
# # #
# # # # ---------------- MAIN ----------------
# # #
# # # if __name__ == "__main__":
# # #     term = input("Enter a word: ")
# # #
# # #     result = get_top_domains(term)
# # #
# # #     print("\nTop Relevant Domains:")
# # #     for r in result:
# # #         print("•", r)
# #
# #
# #
# # import requests
# # from collections import Counter
# # import re
# #
# # WIKI_API = "https://en.wikipedia.org/w/api.php"
# #
# # # ---------------- CONFIG ---------------- #
# #
# # STOPWORDS = {
# #     "of", "and", "in", "the", "by", "for", "with",
# #     "from", "on", "at", "to", "an", "a"
# # }
# #
# # GENERIC_BAN = {
# #     "american", "canadian", "british", "people", "men", "women",
# #     "births", "deaths", "living", "establishments", "english"
# # }
# #
# # NOISE_PATTERNS = [
# #     "articles", "wikipedia", "pages", "short description",
# #     "wikidata", "cs1", "use dmy", "use mdy",
# #     "maintenance", "stubs", "template", "infobox",
# #     "philosophy of", "history of", "concepts in", "theory of"
# # ]
# #
# # IMPORTANT_DOMAINS = {
# #     "technology", "business", "space", "physics", "chemistry",
# #     "biology", "mathematics", "computer", "engineering",
# #     "cricket", "sports", "ai", "entrepreneur",
# #     "finance", "thermodynamics", "information", "statistics"
# # }
# #
# # HEADERS = {"User-Agent": "WikiSemanticDomainExtractor/1.0"}
# #
# # # ---------------- UTILS ---------------- #
# #
# # def clean_text(text):
# #     text = text.lower()
# #     text = re.sub(r'[^a-zA-Z ]', '', text)
# #     return text
# #
# #
# # def extract_keywords(category):
# #     category = clean_text(category)
# #     words = category.split()
# #     return [w for w in words if w not in STOPWORDS and len(w) > 2]
# #
# #
# # def is_useful(category):
# #     category = category.lower()
# #     return not any(pattern in category for pattern in NOISE_PATTERNS)
# #
# #
# # def is_person(categories):
# #     for cat in categories:
# #         c = cat.lower()
# #         if "living people" in c or "births" in c:
# #             return True
# #     return False
# #
# #
# # # ---------------- API CALLS ---------------- #
# #
# # def search_pages(term):
# #     params = {
# #         "action": "query",
# #         "list": "search",
# #         "srsearch": term,
# #         "format": "json",
# #         "srlimit": 5
# #     }
# #
# #     res = requests.get(WIKI_API, params=params, headers=HEADERS).json()
# #     return [item["title"] for item in res["query"]["search"]]
# #
# #
# # def get_categories(title):
# #     params = {
# #         "action": "query",
# #         "prop": "categories",
# #         "titles": title,
# #         "format": "json",
# #         "cllimit": "max"
# #     }
# #
# #     res = requests.get(WIKI_API, params=params, headers=HEADERS).json()
# #
# #     pages = res["query"]["pages"]
# #
# #     cats = []
# #
# #     for page_id in pages:
# #         page = pages[page_id]
# #
# #         if "categories" in page:
# #             for cat in page["categories"]:
# #                 name = cat["title"].replace("Category:", "")
# #                 if is_useful(name):
# #                     cats.append(name)
# #
# #     return cats
# #
# #
# # # ---------------- DOMAIN ENGINE ---------------- #
# #
# # def score_keywords(all_categories):
# #
# #     person = is_person(all_categories)
# #
# #     scores = Counter()
# #
# #     for cat in all_categories:
# #         words = extract_keywords(cat)
# #
# #         for word in words:
# #
# #             if word in GENERIC_BAN:
# #                 continue
# #
# #             if person and word.endswith("n"):
# #                 continue
# #
# #             score = 1
# #
# #             if word in IMPORTANT_DOMAINS:
# #                 score += 3
# #
# #             scores[word] += score
# #
# #     return scores
# #
# #
# # def get_top_domains(term):
# #
# #     try:
# #         titles = search_pages(term)
# #     except:
# #         return []
# #
# #     all_categories = []
# #
# #     for title in titles:
# #         try:
# #             all_categories.extend(get_categories(title))
# #         except:
# #             pass
# #
# #     keyword_scores = score_keywords(all_categories)
# #
# #     return [word for word, _ in keyword_scores.most_common(3)]
# #
# #
# # # ---------------- MAIN LOOP ---------------- #
# #
# # if __name__ == "__main__":
# #
# #     print("🔎 Wikipedia Semantic Domain Extractor")
# #     print("Type 'exit' to quit\n")
# #
# #     while True:
# #
# #         term = input("Enter a word: ").strip()
# #
# #         if term.lower() == "exit":
# #             print("👋 Exiting...")
# #             break
# #
# #         if not term:
# #             print("⚠️ Please enter a valid term.\n")
# #             continue
# #
# #         result = get_top_domains(term)
# #
# #         if result:
# #             print("\nTop Relevant Domains:")
# #             for r in result:
# #                 print("•", r)
# #         else:
# #             print("No relevant domains found.")
# #
# #         print()  # spacing
#
#
#
#
# import requests
# from collections import Counter
# import re
#
# WIKI_API = "https://en.wikipedia.org/w/api.php"
# HEADERS = {"User-Agent": "WikiSemanticDomainExtractor/2.0"}
#
# STOPWORDS = {"of", "and", "in", "the", "by", "for", "with", "from", "on", "at", "to", "an", "a"}
#
# GENERIC_BAN = {
#     "american","canadian","british","male","female","people","men","women",
#     "births","deaths","living","about","chart","usages","factors","single",
#     "united","states","characters","companies","inventions","clubs"
# }
#
# DOMAIN_MAP = {
#     "films":"film","film":"film","actors":"film","cinema":"film",
#     "cricketers":"cricket","cricketer":"cricket",
#     "computing":"computer science","software":"computer science",
#     "medical":"medicine","pathology":"medicine","neoplasms":"medicine",
#     "wireless":"networking","wifi":"networking"
# }
#
# IMPORTANT_HINTS = {"science","technology","engineering","field","study","branch"}
#
# NOISE_PATTERNS = ["articles","wikipedia","pages","short description","stubs","template"]
#
# # ---------------- CLEANING ---------------- #
#
# def clean_text(text):
#     return re.sub(r'[^a-zA-Z ]', '', text.lower())
#
#
# def extract_keywords(category):
#     words = clean_text(category).split()
#     return [w for w in words if w not in STOPWORDS and len(w) > 2]
#
#
# def normalize(word):
#     return DOMAIN_MAP.get(word, word)
#
#
# # ---------------- API ---------------- #
#
# def search_pages(term):
#     params = {
#         "action":"query",
#         "list":"search",
#         "srsearch":term,
#         "format":"json",
#         "srlimit":5
#     }
#     res = requests.get(WIKI_API, params=params, headers=HEADERS).json()
#     return [item["title"] for item in res["query"]["search"]]
#
#
# def get_categories(title):
#     params = {
#         "action":"query",
#         "prop":"categories",
#         "titles":title,
#         "format":"json",
#         "cllimit":"max"
#     }
#     res = requests.get(WIKI_API, params=params, headers=HEADERS).json()
#
#     cats = []
#     for page in res["query"]["pages"].values():
#         if "categories" in page:
#             for cat in page["categories"]:
#                 name = cat["title"].replace("Category:","")
#                 if not any(n in name.lower() for n in NOISE_PATTERNS):
#                     cats.append(name)
#     return cats
#
#
# # ---------------- ENGINE ---------------- #
#
# def score_keywords(categories, query):
#
#     query = query.lower()
#     scores = Counter()
#
#     for cat in categories:
#
#         words = extract_keywords(cat)
#
#         for w in words:
#
#             if w in GENERIC_BAN:
#                 continue
#
#             if w in query:
#                 continue
#
#             w = normalize(w)
#
#             score = 1
#
#             if any(hint in cat.lower() for hint in IMPORTANT_HINTS):
#                 score += 2
#
#             scores[w] += score
#
#     return scores
#
#
# def get_top_domains(term):
#
#     titles = search_pages(term)
#
#     if not titles:
#         return []
#
#     # Prefer exact title match
#     titles = sorted(titles, key=lambda x: term.lower() not in x.lower())
#
#     categories = []
#
#     for t in titles[:3]:
#         categories.extend(get_categories(t))
#
#     scores = score_keywords(categories, term)
#
#     return [d for d, _ in scores.most_common(3)]
#
#
# # ---------------- LOOP ---------------- #
#
# print("🔎 Wikipedia Semantic Domain Extractor (Optimized)")
# print("Type 'exit' to quit\n")
#
# while True:
#
#     term = input("Enter a word: ").strip()
#
#     if term.lower() == "exit":
#         break
#
#     if not term:
#         continue
#
#     result = get_top_domains(term)
#
#     if result:
#         print("\nTop Relevant Domains:")
#         for r in result:
#             print("•", r)
#     else:
#         print("No relevant domains found.")
#
#     print()


import requests
from collections import Counter
import re

WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "WikiSemanticDomainExtractor/Final"}

# ---------------- CONFIG ---------------- #

STOPWORDS = {
    "of", "and", "in", "the", "by", "for", "with",
    "from", "on", "at", "to", "an", "a"
}

SYSTEM_NOISE = {
    "use", "doi", "maint", "pages", "articles", "template",
    "short", "description", "cs1", "date", "format", "tracking"
}

VERB_LIKE = {
    "using", "used", "based", "including", "featuring",
    "containing", "given", "related", "about"
}

NOISE_PATTERNS = [
    "articles", "wikipedia", "pages", "short description",
    "stubs", "template", "cs1", "date format", "tracking",
    "maintenance"
]

DOMAIN_MAP = {
    "films": "film",
    "film": "film",
    "actors": "actor",
    "actresses": "actor",
    "cricketers": "cricket",
    "cricketer": "cricket",
    "computing": "computer science",
    "software": "computer science",
    "medical": "medicine",
    "pathology": "medicine",
    "neoplasms": "medicine",
    "wifi": "networking",
    "wireless": "networking"
}

# ---------------- TEXT UTILS ---------------- #

def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())


def extract_keywords(category):
    words = clean_text(category).split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def normalize(word):
    return DOMAIN_MAP.get(word, word)


def is_valid_token(word, query):
    if len(word) < 4:
        return False
    if word in SYSTEM_NOISE:
        return False
    if word in VERB_LIKE:
        return False
    if word in query:
        return False
    if word.isnumeric():
        return False
    return True

# ---------------- API ---------------- #

def search_pages(term):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": term,
        "format": "json",
        "srlimit": 5
    }

    res = requests.get(WIKI_API, params=params, headers=HEADERS).json()
    titles = [item["title"] for item in res["query"]["search"]]

    # Prefer exact/strong match
    titles = sorted(titles, key=lambda x: term.lower() not in x.lower())

    return titles[:3]


def get_categories(title):
    params = {
        "action": "query",
        "prop": "categories",
        "titles": title,
        "format": "json",
        "cllimit": "max"
    }

    res = requests.get(WIKI_API, params=params, headers=HEADERS).json()

    cats = []

    for page in res["query"]["pages"].values():
        if "categories" in page:
            for cat in page["categories"]:
                name = cat["title"].replace("Category:", "")

                if not any(n in name.lower() for n in NOISE_PATTERNS):
                    cats.append(name)

    return cats

# ---------------- DOMAIN ENGINE ---------------- #

def score_domains(categories, query):

    query = query.lower()
    freq = Counter()

    for cat in categories:

        if any(n in cat.lower() for n in SYSTEM_NOISE):
            continue

        words = extract_keywords(cat)

        for w in words:

            if not is_valid_token(w, query):
                continue

            w = normalize(w)

            freq[w] += 1

    # keep only meaningful domains (frequency threshold)
    filtered = {k: v for k, v in freq.items() if v >= 2}

    return Counter(filtered)


def get_top_domains(term):

    try:
        titles = search_pages(term)
    except:
        return []

    all_categories = []

    for t in titles:
        try:
            all_categories.extend(get_categories(t))
        except:
            pass

    scores = score_domains(all_categories, term)

    return [d for d, _ in scores.most_common(3)]

# ---------------- MAIN LOOP ---------------- #

print("🔎 Wikipedia Semantic Domain Extractor (Final)")
print("Type 'exit' to quit\n")

while True:

    term = input("Enter a word: ").strip()

    if term.lower() == "exit":
        print("👋 Exiting...")
        break

    if not term:
        print("⚠️ Please enter a valid term.\n")
        continue

    result = get_top_domains(term)

    if result:
        print("\nTop Relevant Domains:")
        for r in result:
            print("•", r)
    else:
        print("No relevant domains found.")

    print()
