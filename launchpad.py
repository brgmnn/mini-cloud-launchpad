#!/usr/bin/env python2
from flask import Flask, render_template, url_for, redirect, request, make_response, session
import boto.ec2

app = Flask(__name__)


# The index page.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["access_key"] = request.form["access_key"].encode("ascii", "ignore")
        session["secret_key"] = request.form["secret_key"].encode("ascii", "ignore")

    if "access_key" in session and "secret_key" in session:
        return render_template("index.html")
    return render_template("login.html")


# Api route to launch a Wordpress instance.
@app.route("/api/launch")
def launch_instance():
    if "access_key" in session and "secret_key" in session and "instance_ids" not in session:
        conn = boto.ec2.connect_to_region("eu-west-1",
                aws_access_key_id=session["access_key"],
                aws_secret_access_key=session["secret_key"])

        # wordpress stack
        res = conn.run_instances("ami-216df956")
        session["instance_ids"] = [i.id.encode("ascii","ignore") for i in res.instances]
        return ",".join(session["instance_ids"])
    return ""

# Api route to stop a wordpress instance.
@app.route("/api/terminate")
def stop_instance():
    if "access_key" in session and "secret_key" in session and "instance_ids" in session:
        conn = boto.ec2.connect_to_region("eu-west-1",
                aws_access_key_id=session["access_key"],
                aws_secret_access_key=session["secret_key"])

        iids = session["instance_ids"]
        conn.terminate_instances(instance_ids=iids)
        session.pop("instance_ids", None)
        return ",".join(iids)
    return ""

# Api route to return the status of instances.
@app.route("/api/status")
def status():
    if "access_key" in session and "secret_key" in session and "instance_ids" in session:
        conn = boto.ec2.connect_to_region("eu-west-1",
                aws_access_key_id=session["access_key"],
                aws_secret_access_key=session["secret_key"])

        iids = session["instance_ids"]
        res = conn.get_all_instances(instance_ids=iids)
        return ",".join([i.state for r in res for i in r.instances])
    return ""

# public_dns_name
# Api route to get the public DNS name of the instance.
@app.route("/api/url")
def url():
    if "access_key" in session and "secret_key" in session and "instance_ids" in session:
        conn = boto.ec2.connect_to_region("eu-west-1",
                aws_access_key_id=session["access_key"],
                aws_secret_access_key=session["secret_key"])

        iids = session["instance_ids"]
        res = conn.get_all_instances(instance_ids=iids)
        return "\n".join([i.public_dns_name for r in res for i in r.instances])
    return ""


# Log out of the application
@app.route("/logout")
def logout():
    session.pop("instance_ids", None)
    session.pop("access_key", None)
    session.pop("secret_key", None)
    return redirect(url_for("index"))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
