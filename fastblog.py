from flask import Flask,render_template,url_for
app = Flask(__name__)
posts = [
    {
        'author':'Corey',
        'title':'Blog Post 1',
        'content':"First Post content",
        'date_posted': '29 May 2021'
    },
    {
        'author': 'Jane',
        'title': 'Blog Post 2',
        'content': "Second Post content",
        'date_posted': '30 May 2021'
    }
]

@app.route('/home')
def hello_world():
    return render_template('home.html',posts = posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

if __name__ == '__main__':
    app.run(debug=True)

