from falsk import Flask, render_template

app= Flask(__name__)

@app.route('/')
@app.route('/avaleht')
def avaleht():
    return render_template('avaleht.html')

if __name__=='__main__':
    app.run(debug=True)