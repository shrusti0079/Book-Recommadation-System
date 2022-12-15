# building a basic app
from flask import Flask, render_template,request
import pickle
import numpy as np
# with open(pop.pkl, 'rb') as f:
#     popular_df = pickle.load(f)


popular_df= pickle.load(open("pop.pkl",'rb'))  
pt= pickle.load(open("pt.pkl",'rb'))  #pivot table
books= pickle.load(open("books.pkl",'rb')) #
similarity_scores= pickle.load(open("similarity_scores.pkl",'rb')) #similar books detials


app= Flask(__name__) # object of flask

@app.route('/')
def index():
    # return "hello World"
    # return render_template('index.html')
    return render_template('index.html', book_name=list(popular_df['Book-Title'].values), author=list(popular_df['Book-Author'].values), image=list(popular_df['Image-URL-M'].values), votes=list(popular_df['num_ratings'].values), rating=list(popular_df['avg_rating'].values))

@app.route('/rt')
def recommend_ui():
    return render_template('rt.html')
# for recommender page

@app.route('/rt_books', methods=['POST'])                           #for getting data from the form.
def recommend():
    user_input= request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data_list = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data_list.append(item) #succesfully copied the function code from jupyter file.
    print(data_list)
    # return str(user_input)
    return render_template('rt.html', data=data_list)

if __name__=='__main__':
    app.run(debug=True)

