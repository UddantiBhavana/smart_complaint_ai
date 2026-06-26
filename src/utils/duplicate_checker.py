from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_complaints(new_complaint, existing_complaints):

    if not existing_complaints:
        return None, 0

    texts = [new_complaint]

    for complaint in existing_complaints:
        texts.append(str(complaint))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(texts)

    similarity_scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    max_score = max(similarity_scores)

    index = similarity_scores.argmax()

    return existing_complaints[index], round(max_score * 100, 2)