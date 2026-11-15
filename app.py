import os
import socket
from datetime import datetime
from string import Template

from flask import Flask

app = Flask(__name__)

PAGE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jenkins to Kubernetes</title>
<style>
  body { margin:0; font-family: system-ui, Arial, sans-serif; background:#0b1220; color:#e8edf7; }
  .wrap { max-width:760px; margin:0 auto; padding:56px 20px; text-align:center; }
  h1 { font-size:38px; margin:0 0 8px; }
  h1 span { color:#4f9dff; }
  p { color:#93a1bd; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin-top:32px; }
  .card { background:#131c2e; border:1px solid #243049; border-radius:14px; padding:18px; text-align:left; }
  .card small { color:#93a1bd; text-transform:uppercase; letter-spacing:.08em; font-size:12px; }
  .card div { font-family: ui-monospace, Consolas, monospace; font-size:18px; margin-top:6px; color:#3ddc97; word-break:break-all; }
  footer { margin-top:40px; color:#93a1bd; font-size:14px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Deployed by <span>Jenkins</span> on <span>Kubernetes</span></h1>
  <p>A Docker image built by the pipeline is running as pods in a Kubernetes cluster.</p>
  <div class="grid">
    <div class="card"><small>Build number</small><div>$version</div></div>
    <div class="card"><small>Pod name</small><div>$pod</div></div>
    <div class="card"><small>Server time</small><div>$time</div></div>
  </div>
  <footer>Arjun V and Kanikshaa K | Essentials in Cloud and DevOps | SRM Institute</footer>
</div>
</body>
</html>""")


@app.route("/")
def home():
    return PAGE.substitute(
        version=os.environ.get("APP_VERSION", "0"),
        pod=socket.gethostname(),
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
