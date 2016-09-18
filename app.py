from flask import Flask, request, render_template
import inventory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recon')
def recon():
    who = inventory.Who()
    instances = inventory.Instance().get_all_running()
    return render_template('recon.html', instances=instances, who=who)

# We only need this for local development.
if __name__ == '__main__':
    app.run()
