from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from utils.data import load_matrix_from_local,convert_to_matrix,load_csv
import json


def search_products(product_names: str) -> str:
    """
    Meathod to get the products as per user query
    a tool for
    :param product_names: comma(,) seperated names of products for ex shirt, pant
    
    """
    

    product_names = product_names.split(",")
    no_of_product_response=5
    final_result=[]
    df = load_csv()
    tfidf_matrix,tfidf_vectorizer= load_matrix_from_local()

    
    
    for product in product_names:
        print(f'searching for {product}')
        query_vec = tfidf_vectorizer.transform([product.lower()])
        cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
        relevant_indices = cosine_similarities.argsort()[-no_of_product_response:][::-1]

        results = df.iloc[relevant_indices].copy()
        results['similarity_score'] = cosine_similarities[relevant_indices]
        results=results[["Product_name","product_url","image_link","similarity_score"]]
        results = results.to_dict(orient="records")
        final_result.append({product:results})
    
    return json.dumps(final_result)
